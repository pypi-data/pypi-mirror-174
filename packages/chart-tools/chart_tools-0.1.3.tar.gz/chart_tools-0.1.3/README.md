<h1> chart-tools &nbsp;&nbsp;&nbsp; <a href="https://pypi.org/project/chart-tools/" alt="Version"> <img src="https://img.shields.io/pypi/v/chart-tools.svg" /></a> </h1>

<!-- **View Full Documentation [Here](https://github.com/ryayoung/chart-tools)** -->

<br>

## Install & Use

Must have python 3.9+

```
pip install chart-tools
```

```py
import chart_tools as ct
ct.load_data() # outputs available pre-defined data sources
```

<br>

# [Data Interface](https://github.com/ryayoung/chart-tools/blob/main/sampledata.md)

#### Easily load datasets and explore available sources with one line of code

- The [`load_data()`](https://github.com/ryayoung/chart-tools/blob/main/sampledata.md) function and [`DataSource`](https://github.com/ryayoung/chart-tools/blob/main/sampledata.md) object use Github's API to explore file structures in repositories containing `.csv` files, and easily load files into dataframes. Chart-tools has a pre-defined library (collection of repositories) for you to explore within your notebook and load data from.

#### Robust caching system designed for Python notebooks, performing great with large datasets.

- Any dataframe you load gets cached in memory, remembering which pandas keyword arguments you used when loading the file. Next time you load it, you'll get a _copy_ of the cached dataframe, unless you pass different keyword arguments. Not only is this great for performance with large datasets, but it also eliminates the common need to declare a `df_raw = ...` and then use `df = df_raw.copy()` to get your original data again. 

#### Has a pre-defined library of data sources to explore, and lets you easily define your own library

- Save an entire Github repository file structure (csv files only) to your desktop

# 

# [Charts & Visualization](https://github.com/ryayoung/chart-tools/blob/main/superheat.md)

### [`superheat`](https://github.com/ryayoung/chart-tools/blob/main/superheat.md)

- A "super" correlation heatmap you can't find elsewhere, designed for speed and ease of use.
- Marks are sized dynamically based on correlation strength, drawing your eyes straight to the most important relationships.
- Easily filter out variables whose coefficients average below a threshold, or simply mask/hide marks below a threshold.

#### Examples

<img width="450" alt="Screen Shot 2022-04-24 at 3 02 22 AM" src="https://user-images.githubusercontent.com/90723578/164968825-2679e57e-4df1-44fd-9465-6cca60c211ce.png">

<img width="1000" alt="Screen Shot 2022-04-24 at 3 09 06 AM" src="https://user-images.githubusercontent.com/90723578/164969119-f7950d5a-f40c-4a6e-b6d6-cc1067dec474.png">
