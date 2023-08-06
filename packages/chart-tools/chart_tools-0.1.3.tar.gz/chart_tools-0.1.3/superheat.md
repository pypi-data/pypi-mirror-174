# `superheat()`

### A "super" correlation heatmap you can't find elsewhere

[Documentation](#documentation)

[Instructions & Examples](#instructions)

#

> Traditional correlation heatmaps generated from Seaborn or Plotly are good at using color to distinguish positive from negative correlations. However, they _aren't_ very good at drawing your eyes towards the _strongest_ correlations. Especially with large datasets containing many variables, the chart gets cluttered with weak correlations that you don't care about.

Dynamically sized marks make large heatmaps like the one below far easier to read. Your eyes go straight to the most significant correlations.

```py
import chart_tools as ct
df = ct.load_data('ames_mini')
ct.set_style(15)
ct.superheat(df.corr(), half_mask=False, mark_scale=8, grid=False);
```

<img width="1000" alt="Screen Shot 2022-04-24 at 3 09 06 AM" src="https://user-images.githubusercontent.com/90723578/164969119-f7950d5a-f40c-4a6e-b6d6-cc1067dec474.png">

<!-- <img width="1027" alt="Screen Shot 2022-04-24 at 1 16 21 AM" src="https://user-images.githubusercontent.com/90723578/164964749-ee0cfb9e-1774-49c9-830c-eeaf41848dc4.png"> -->

Unfortunately, this chart is impossible to build with the "heatmap" or equivalent function provided in most popular graphing libraries, so instead, we have to build a scatterplot that looks and works like a heatmap. This is extremely awkward to do, and requires more code than anyone would normally want to write in their typical visualization workflow. Source code can be found [here](/src/chart_tools/heatmaps/superheat.py).

<br>

<a name="documentation"></a>

# Documentation

_Important:_ Remember to place a semicolon at the end of the function call to avoid the "Figure size ..." annotation printout.

Required Parameters

- `corr`: Correlation dataframe (use `df.corr()`). Must have equal number of rows and columns.

Optional Parameters

- `title` - _str_: Chart title. Default: None
- `thresh_avg` - _float_: Removes any variable whose _average_ correlation to all others is below threshold. Default: None
- `thresh_mask` - _float_: Masks any _individual_ correlations that are below threshold. Default: None
- `half_mask` - _bool_: Masks half the chart, hiding duplicate correlations. Default: True
- `self_mask` - _bool_: Masks correlations between variables and themself. Default: True
- `cbar` - _bool_: Include colorbar. Default: True
- `mark_scale` - _int_: Change the scale of all marks. Default: 5
- `grid` - _bool_: Show grid. Default: True
- `palette` - _sns.diverging_palette_: Color palette to use on marks. Default: `(20, 220, n_colors)`
- `size` - _int_: Set chart height and width. Default: None
- `marker` - _char_: Marker shape. Default 's'. Click [here](https://python-graph-gallery.com/41-control-marker-features) for a list of all marker shapes.
- `bar_ticks` - _int_: Number of tick marks on color bar. Default: 5
- `n_colors` - _int_: Number of colors to include in color palette. Default: 128
- **kwargs: Any additional keyword arguments will go to the matplotlib `plt.scatter` function

<br>

### `set_style()`
> Wrapper for `seaborn.set_theme()` that applies defaults to save you time

Required Parameters - *None*

Optional Parameters
- `size` - *int* or *tuple*: Declares chart size. *Int* will set width and height to the same value. Use *tuple*, `(width, height)` to set custom values. Default: 12

Parameters passed to `sns.set_theme()`, but with defaults
- `palette`: *str*: Default: "pastel"
- `style`: *str*: Default: "whitegrid"
- `font_scale`: *float*: Default: 1.5
- **kwargs: Any additional keyword arguments will go into `sns.set_theme()`

<br>

<a name="instructions"></a>

# Instructions & Examples

All of the following examples will start with this code:

```py
import chart_tools as ct
df = ct.load_data('ames_mini').drop(columns=['YrSold', 'Id', 'GarageCars', 'Fireplaces', 'ScreenPorch', 'BsmtUnfSF', 'Bathrooms'])
```

`set_style()`: Easiest way to set chart size and apply a color preset. Pass an integer (like in the above example) to create a square, or pass a tuple, `(width, height)` for custom dimensions. 

### Default

```py
ct.set_style(10) # Sets charts to 10x10 square, with chart-tools defualt styling
ct.superheat(df.corr());
```

<img width="500" alt="Screen Shot 2022-04-24 at 2 56 01 AM" src="https://user-images.githubusercontent.com/90723578/164968660-447bf0e5-68d7-47ad-b29c-2b3cff254a53.png">

### Remove variables who average below threshold

```py
ct.set_style(6) # Decrease chart size to keep proportions
ct.superheat(df.corr(), thresh_avg=0.19);
```

<img width="500" alt="Screen Shot 2022-04-24 at 2 58 45 AM" src="https://user-images.githubusercontent.com/90723578/164968692-54844fca-f36e-49e5-b6b2-cfb18681caeb.png">

### Mask individual correlations below threshold

```py
ct.superheat(df.corr(), thresh_mask=0.19);
```

<img width="500" alt="Screen Shot 2022-04-24 at 2 59 27 AM" src="https://user-images.githubusercontent.com/90723578/164968718-29fcb91f-7ba1-431b-8069-ff420d9c12dd.png">

### Include all real correlations

```py
ct.superheat(df.corr(), half_mask=False);
```

<img width="500" alt="Screen Shot 2022-04-24 at 3 00 13 AM" src="https://user-images.githubusercontent.com/90723578/164968741-495f4fba-b0b3-4601-9fa6-77b93f39336c.png">

### Include self on self correlations

```py
ct.superheat(df.corr(), self_mask=False);
```

<img width="500" alt="Screen Shot 2022-04-24 at 3 00 52 AM" src="https://user-images.githubusercontent.com/90723578/164968757-7b1c713a-7f5a-4751-af30-70cfc7630a49.png">

### Change marker type

```py
ct.superheat(df.corr(), marker='o');
```

<img width="500" alt="Screen Shot 2022-04-24 at 3 01 40 AM" src="https://user-images.githubusercontent.com/90723578/164968794-2f0616e3-e58f-4f0c-90f5-a5e15e2d9d69.png">

### Change marker scale

```py
ct.superheat(df.corr(), mark_scale=8); # Notice the marks are slightly larger. Default was 5
```

<img width="500" alt="Screen Shot 2022-04-24 at 3 02 22 AM" src="https://user-images.githubusercontent.com/90723578/164968825-2679e57e-4df1-44fd-9465-6cca60c211ce.png">

### Use fewer colors

```py
ct.superheat(df.corr(), n_colors=12); # Look at colorbar to see what's changed
```

<img width="500" alt="Screen Shot 2022-04-24 at 3 02 57 AM" src="https://user-images.githubusercontent.com/90723578/164968842-49fab0e9-fd13-4606-afb4-df35eb56615e.png">

### Hide grid

```py
ct.superheat(df.corr(), grid=False, marker='o');
```

<img width="500" alt="Screen Shot 2022-04-24 at 3 03 29 AM" src="https://user-images.githubusercontent.com/90723578/164968882-efbce738-9b95-4ade-a899-fc01262f2c53.png">

### Why is superheat great for large datasets?

Because with a dataset this large, the less you see, the better

<img width="1000" alt="Screen Shot 2022-04-24 at 3 09 06 AM" src="https://user-images.githubusercontent.com/90723578/164969119-f7950d5a-f40c-4a6e-b6d6-cc1067dec474.png">

<br/><br/>

This function is based on Drazen Zaric's "Better Heatmaps" in [this](https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec) article, and his [heatmaps](https://pypi.org/project/heatmapz/) package.
