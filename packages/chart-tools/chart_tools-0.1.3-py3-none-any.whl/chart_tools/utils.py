# Maintainer:     Ryan Young
# Last Modified:  Apr 21, 2022
import seaborn as sns

def set_style(size=12, palette='pastel', style='whitegrid', font_scale=1.5, **kwargs):

    if type(size) == tuple:
        sns.set(rc={'figure.figsize':size})
    elif type(size) == int:
        sns.set(rc={'figure.figsize':(size,size)})

    sns.set_theme(style=style, palette=palette, font_scale=font_scale, **kwargs)

