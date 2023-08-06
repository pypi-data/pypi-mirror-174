import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def sig_corr(corr:pd.DataFrame, threshold:float) -> pd.DataFrame:
    df = corr.copy()
    df['mean'] = df.mean(axis=1)
    to_drop = set()
    for var in df.index:
        if abs(df.loc[var, 'mean']) < threshold:
            to_drop.add(var)
    df = df.drop(index=to_drop, columns=to_drop)
    df = df.drop(columns='mean')
    return df


def superheat(
        corr:pd.DataFrame,
        title=None,
        thresh_avg=None,
        thresh_mask=None,
        half_mask=True,
        self_mask=True,
        cbar=True,
        mark_scale=5,
        grid=True,
        palette=None,
        size=None,
        title_fontsize=None,
        marker='s',
        bar_ticks=5,
        n_colors=128,
        **kwargs
    ):

    if not len(corr.columns) == len(corr.index):
        raise ValueError("A correlation df needs the same length columns and index")

    # Chart size
    if size:
        sns.set(rc={'figure.figsize':(size, size)})

    # Data
    dfc = corr.copy()
    # Must fill null values with 0. Having any nulls in a df.corr() is
    # rare, and it's difficult for the user to fix the problem. This only
    # occurs when one of the input variables has the same numeric value for
    # the entire column. When that happens, the resulting correlation matrix
    # will have an entirely null column, AND an entirely null row. Calling
    # dropna() on either axis would delete all the data. So our only option
    # is to remove the variable from the matrix by iteration (slow, but better)
    # or just filling nulls with 0.
    dfc = dfc.fillna(0)

    # Remove vars whose absolute mean corr is below threshold
    if thresh_avg:
        dfc = sig_corr(dfc, thresh_avg)
    
    # Mask insignificant correlations, if requested
    if thresh_mask:
        dfc = dfc.mask(abs(dfc) < thresh_mask).fillna(0)
    
    # Reindex before masking, since reindexing will happen later on if we don't
    dfc = dfc.reindex(sorted(dfc.columns), axis=1)
    if half_mask:
        for i, c in enumerate(dfc.columns):
            # Remove duplicate correlations
            for col in list(dfc.columns[0:i]):
                dfc.loc[col, c] = 0
    if self_mask:
        for i, c in enumerate(dfc.columns):
            # Remove self-self correlations
            dfc.loc[c,c] = 0.0

    num_vars = len(dfc.columns)

    # Unpivot df to get paired x & y arrays
    dfc = pd.melt(dfc.reset_index(), id_vars='index')
    dfc.columns = ['x', 'y', 'value']
    x = dfc['x']
    y=dfc['y']
    size=dfc['value'].abs()

    # Plot setup
    fig, ax = plt.subplots()
    plot_grid = plt.GridSpec(1,30,hspace=0.2,wspace=0.1)
    ax = plt.subplot(plot_grid[:,:-1])
    # Title font size
    if title_fontsize:
        title_fsize = title_fontsize
    else:
        # Set title fontsize programmatically if no param given
        title_fsize = int(18 + num_vars / 2)
    ax.set_title(title, fontsize=title_fsize)

    # Color
    if palette == None:
        palette = sns.diverging_palette(20, 220, n=n_colors)
    else:
        n_colors = len(palette)
    
    color_min, color_max = [-1, 1]
    def value_to_color(val):
        val_position = float((val - color_min)) / (color_max - color_min) # position of value in the input range, relative to the length of the input range
        ind = int(val_position * (n_colors - 1)) # target index in the color palette
        return palette[ind]
    
    # Mapping from column names to integer coordinates
    x_labels = [v for v in sorted(x.unique())]
    y_labels = [v for v in sorted(y.unique())]
    x_to_num = {p[1]:p[0] for p in enumerate(x_labels)} 
    y_to_num = {p[1]:p[0] for p in enumerate(y_labels)} 
    xmap = x.map(x_to_num)
    ymap = y.map(y_to_num)
    
    # Draw
    size_scale = mark_scale * 100
    ax.scatter(
        x=kwargs.pop('x', xmap),
        y=kwargs.pop('y', ymap),
        s=kwargs.pop('s', (size * size_scale)), # Vector of square sizes, proportional to size parameter
        c=kwargs.pop('c', (dfc['value'].apply(value_to_color))),
        marker=marker, # Use square as scatterplot marker
        **kwargs,
    )
    
    # Show column labels on the axes
    ax.set_xticks([x_to_num[v] for v in x_labels])
    ax.set_xticklabels(x_labels, rotation=45, horizontalalignment='right')
    ax.set_yticks([y_to_num[v] for v in y_labels])
    ax.set_yticklabels(y_labels)
    ax.grid(False, 'major')

    if grid == True:
        ax.grid(True, 'minor')

    ax.set_xticks([t + 0.5 for t in ax.get_xticks()], minor=True)
    ax.set_yticks([t + 0.5 for t in ax.get_yticks()], minor=True)
    ax.set_xlim([-0.5, max([v for v in x_to_num.values()]) + 0.5])
    ax.set_ylim([-0.5, max([v for v in y_to_num.values()]) + 0.5])
    ax.invert_xaxis()

    # Color Bar
    if cbar == True:
        axb = plt.subplot(plot_grid[:,-1])

        col_x = [1]*len(palette)
        bar_y = np.linspace(color_min, color_max, n_colors)
        
        bar_height = bar_y[1] - bar_y[0]
        axb.barh(
            y=bar_y,
            width=[2]*len(palette), # make bars 5 units wide
            left=col_x, # Make bars start at 0
            height=bar_height,
            color=palette,
            linewidth=0
        )
        axb.set_xlim(1, 2) # Bars are going from 0 to 5, so lets crop the plot somewhere in the middle
        axb.grid(False) # Hide grid
        axb.set_facecolor('white') # Make background white
        axb.set_xticks([]) # Remove horizontal ticks
        axb.set_yticks(np.linspace(min(bar_y), max(bar_y), bar_ticks)) # Show vertical ticks for min, middle and max
        axb.yaxis.tick_right() # Show vertical ticks on the right

    return (fig, ax);
