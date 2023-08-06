## Data Interface


> Explore online datasets (or your own) and load dataframes, all with one line of code, without leaving your python notebook. Either use the default library to explore and load sample data, or define your own `Library` so you never have to store or organize csv data locally.

<br>

[Documentation](#documentation)

[Instructions & Examples](#instructions-and-examples)

<br>

### Designed for Python notebooks

- Interactive tools for exploring and loading datasets from online Github repositories.
- Real-time access to see the file structure of any Github repository as a cell output.
- Pre-defined `Library` of repositories to load data from, with a single line of code.
- Robust caching system, useful for working with large data files, making your notebook perform as if the files were stored locally

<br>


# Documentation
---
**Functions to interact with pre-defined Library**

-  [`load_data`](#load_data)
-  [`df`](#df)
-  [`set_library`](#set_library)
-  [`reset_library`](#reset_library)
-  [`default_lib`](#default_lib)
-  [`default_lib_url`](#default_lib_url)
-  [`library_help`](#library_help)

**Classes**
-  [`DataSource`](#datasource)
-  [`Library`](#library)
-  [`Source`](#source)


<br>

# Interact with pre-defined Library

### `load_data()`

-> pd.DataFrame, or None

---

> The quickest way to get sample data into your notebook. It also caches all loaded datasets into memory. You could call this function by itself at the top of your notebook for each dataset needed, passing any desired keyword arguments to customize format and columns needed (such as `index_col` or `names`), and then have quick access to a copy of this dataframe later using `ct.df("filename")`. The cache tracks the keyword arguments you used when loading, so calling this function again with different kwargs will re-download it. See [instructions](#instructions-and-examples)

**Required Parameters**
- None. Passing no parameters will output a quick-start guide and a list of default DataSources (github repositories) to choose from.

**Optional Parameters**
- `source`: *str*: Nickname of the DataSource where files are located. If accessing files in the "main" DataSource, you can pass just the filename here to quickly load it. Default: None
- `file`: *str*: Csv file name. In DataSources that contain subdirectories - where the filename might be "animals/tiger", you can try to pass just the base filename, "tiger", and if no duplicates are found, the load will be successful. Default: None
- `save`: *bool*: Whether to cache the loaded data in memory. If you choose False, and a cache for the file already exists, it will be removed. Default: True
- **kwargs: This function is ultimately a wrapper for `pd.read_csv()`. Use any additional pandas keyword arguments, such as `index_col=0`, to change how the data is loaded.

<br>

### `df()`

-> pd.DataFrame

---

> Quickly load a cached dataframe by name. Any data that's been loaded with `ct.load_data()`, regardless of whether it was assigned to a variable, is accessible. Unlike `load_data`, it doesn't take pandas keyword arguments, and only returns the originally loaded df. It's more reliable than the common practice of declaring `raw_data = pd.read_...` at the top of your notebook, because the cached dataframe is immutable and always returns a *copy* of the data, so you won't deal with the annoying "*value is trying to be set on a copy of a slice from a ...*" warnings from pandas.

**Required Parameters**
- `filename`: *str*: Name of the cached dataframe being accessed

<br>

### `set_library()`

---

> Change the default library. You have three options: 1. Pass a url to a json file stored online, 2. Pass a path to a json file stored locally, or 3. pass a dictionary containing the library info. For instructions on formatting, see [`Library`](#library).

**Required Parameters**
- `url`: *str or dict*: Web url, local filepath, or dict that defines a [`Library`](#library)

<br>

### `reset_library()`

> Reset the default library to the chart-tools pre-defined one. Only needed if you've changed the default using `set_library()`

<br>

### `default_lib()`

-> Library

> Returns the current default library object

<br>

### `default_lib_url()`

-> str

> Returns the url to the current default library

<br>

### `library_help()`

> Outputs a quick explanation and example of how to format a library definition, a structure which is needed to quickly create a `Library` or change the default library.

<br>
<br>

# Classes

### `DataSource`
- Inherits from: `Source`

---
> The class upon which the chart-tools data interface is built. It defines a Github repository, and provides a variety of functions for fetching and displaying its file structure, loading and caching dataframes, and the ability to download the entire repository (csv files only) or a sub-directory inside the repository, to your local file system. `Library` stores a dictionary of DataSources.

**Declared in 3 ways:**

1. Provide url to a Github repository home page or sub-directory. If home page url, optionally include `branch=...`. (See note below)
2. (fastest, most tedious) Provide username, repo, branch, and (optional) a sub-directory within the repo
3. Provide just the username and repository name. Default branch will be used. (See note below)

> Note: The *home page* url of a repo won't contain the name of a branch, but a url to a sub-directory will. If the branch is unknown, a request to Github's api will automatically be made upon declaration, to determine the default branch. This will take an extra ~1 second to complete. If you're constructing using a url, you can speed up your code by specifying a branch name as a keyword argument. Example: `ct.DataSource("some_url", branch="main")`

**Constructor Arguments**
- `user`: *str*: Github username. Default: None
- `repo`: *str*: Repository name. Default: None
- `branch`: *str*: Repository branch name. Default: None
- `path`: *str*: (optional) sub-dir in repo. Makes for easier file access (load data with "filename" instead of "path/filename"). Default: ""
- `name`: *str*: Nickname for data source. Used when stored in a `Library`, used as the dict key. Default: `repo` if `repo`, else None
- `url`: *str*: Url to Github repository home page or sub-directory. Default: None

#

### Methods
- Access to all methods in [`Source`](#source), the parent class of `DataSource`

#### `display_datasets()`

> Displays names of data files (`self.datasets`) in a tree format, preserving directory structure. Note: the `datasets` property will request a live status of the repository's contents once this variable is **first** accessed. This should take <1 second.

**Optional Parameters**
- `header`: *bool*: Displays descriptive header with repository info. Default: False
- `trunc`: *int*: Max number of files to display. Default: 1000.

<br>

#### `display_subdirs()`

> Displays the subdirectories (`self.subdirs`) inside repository (excluding `self.path`)

**Optional Parameters**
- `header`: *bool*: Displays descriptive header with repository info. Default: False

<br>

#### `__repr__()`

> Executed when you `print()` this object. Displays repository info and url to page on Github

#

<br>

### `Library`
---

> Stores a dictionary of `DataSource`s, with nicknames as keys. Has interactive functions for exploring one or all of its sources at once.
>
> - A library can be defined from either: an online json file, locally stored json file, or a dictionary.
> - In most cases, instead of creating a new Library object, just change the global `default_library` by calling `ct.set_library()`. That way, it can be accessed using global functions like `ct.load_data()`, which is much simpler than calling those methods on a separate Library object.

#### Default Library
> Upon importing chart-tools, `default_library` is pre-defined from a url to the raw contents of [this file](https://github.com/ryayoung/datasets/blob/main/chart-tools-default-library.json), so you can easily find and load sample data. `default_library` is unique in that it can be directly accessed using [these functions](#documentation), without referencing the object itself, and is easy to change.

**Construction**

Before creating a `Library`, make a json file or dict with the following format:
<details>
  <summary>Click here to view format:</summary>

  ```text
  {
      "some_nickname": {
          "u": "some-github-username",
          "r": "some-github-repo",
          "b": "some-branch",
          "p": "some-subdirectory" (optional. Use empty str if none)
      },
      "other_nickname": {
          . . .
      },
      etc..
  }
  ```
</details>

**Constructor Arguments**
- `url`: *str or dict*: Can be one of the following: 1. Url to online json file, 2. Path to local json file, 3. Dict with needed information

#

### Methods

#### `display_sources()`

> Displays each source's name and url

#### `display_all()`

> Displays all sources and all their files, truncated at 15 files per source

#### `load_data()`

-> pd.DataFrame

> Same as the global `ct.load_data()` described [here](#documentation), but called as an instance method instead of global function for the `default_library`.

**`df()`**

-> pd.DataFrame

> Same as the global `ct.df()` described [here](#documentation), but called as an instance method instead of global function for the `default_library`.

<br>

# 

<br>

# Instructions and Examples
---

```py
import chart_tools as ct
```

#

### Pre-defined Data Sources

> As explained [here](#default-library), chart-tools pre-defines the `default_library` making it easy to explore and load sample data with only one line of code

#### How do we know what's available?

```py
ct.load_data()
```

Output:

```
Use load_data(source_name, filename) to load dataframe
Use load_data(source_name) to see all datasets in a source.
Use load_data('all') to see all datasets.
---------
SOURCES:
 'main':      https://github.com/ryayoung/datasets/tree/main/data
 'covid':     https://github.com/datasets/covid-19/tree/main/data
 'football':  https://github.com/datasets/football-datasets/tree/master/datasets
 'sp500':     https://github.com/datasets/s-and-p-500-companies/tree/master/data
 'openml':    https://github.com/datasets/openml-datasets/tree/master/data
```

#### Let's see what's in 'covid', and find the 'countries-aggregated' set

```py
ct.load_data('covid')
```

```
Datasets for 'covid':
---------------------------
  countries-aggregated
  key-countries-pivoted
  reference
  time-series-19-covid-combined
  us_confirmed
  us_deaths
  us_simplified
  worldwide-aggregate
```

#### Or we can see files available, by source & sub-directory

```py
ct.load_data('all')
```

```
(Use load_data(source_name, filename) to load data)
(Use load_data(source_name) to see available datasets in source)

'main'  -  https://github.com/ryayoung/datasets/tree/main/data
---------------------------------
  ames_engineered
  ames_full
  ames_mini
  stock-tweets

'covid'  -  https://github.com/datasets/covid-19/tree/main/data
---------------------------------
  countries-aggregated
  key-countries-pivoted
  reference
```
> (The above output is truncated to save page space here)

#### Let's load one

```py
ct.load_data('covid', 'countries-aggregated')
```

<img width="469" alt="Screen Shot 2022-04-23 at 10 36 10 PM" src="https://user-images.githubusercontent.com/90723578/164956857-b1834946-7f2f-4c1f-970c-a6bc072229f3.png">

> All loaded dataframes get cached in memory even if you don't assign them to a variable. You *could* execute the above code again and receive the data instantly, but instead, call `ct.df('countries-aggregated')` to pull a copy straight from the cache. See explanation [here](#df).

#

#### What about larger sources with sub-directories?

```py
ct.load_data('football')
```

```
Datasets for 'football':
(refer files inside folders using the full path. Ex: 'folder/file')
---------------------------
  la-liga/
    season-0809
    season-0910
    season-1011
    season-1112
    season-1213
    season-1314
    season-1415
    season-1516
    season-1617
    season-1718
    season-1819
  premier-league/
    season-0910
    season-1011
```
> (This output is also truncated. There are a lot of files in football!)

#### To get one of these, use the full path

> In a source with sub-directories, you ONLY need to specify the whole path if there are multiple files with the same name in different directories. Otherwise, just use the base name and we'll figure out where it's located.

```py
ct.load_data('football', 'la-liga/season-0809')
```

<img width="642" alt="Screen Shot 2022-04-23 at 10 51 59 PM" src="https://user-images.githubusercontent.com/90723578/164957212-1288a9b3-e1d0-4ec4-a75e-c4ee89687901.png">

#

#### Keyword arguments!

> `load_data` takes the **same** keyword arguments as `pd.read_csv`. For example, let's set `header=None`

```py
ct.load_data('covid', 'countries-aggregated', header=None)
```

<img width="459" alt="Screen Shot 2022-04-23 at 11 43 37 PM" src="https://user-images.githubusercontent.com/90723578/164958366-381d38a3-3268-4294-a250-6fabf1c354ea.png">

Yes, the cache is smart enough to know exactly which of `pd.read_csv`'s keyword arguments you passed, and each of their values, so you'll never receive a cached dataframe that doesn't match the format you're requesting.

#### Then what?

> Although you *could* use `ct.load_data` every time to get the cached file, that would be annoying because you'd have to pass the same kwargs over and over again. Instead:

```py
ct.df('countries-aggregated')
```

<img width="459" alt="Screen Shot 2022-04-23 at 11 43 37 PM" src="https://user-images.githubusercontent.com/90723578/164958366-381d38a3-3268-4294-a250-6fabf1c354ea.png">

#

### Best practice for managing datasets and the cache

You might ask, *what's the point of caching dataframes if I'm just going to assign them to a variable upon loading them?*

A common bug in large python notebooks comes from managing the original data you loaded in, avoiding a.) accidentally altering it, and b.) the infamous *"a value is trying to be set on a copy of a slice of a ...* warning or error from pandas. So then, you take the time to declare a `df_raw_data = pd.read_...`, and then have to remember to use `df_raw_data.copy()` when referencing it to avoid warnings/errors. You're probably in the habit of assigning your `pd.read_csv` straight to a new dataframe, but chart-tools offers a safer option:

**Call `load_data` at the top of your notebook as a standalone function without assigning any variables, passing any pandas keyword arguments necessary (such as `index_col` or `names`) to get the desired format. Retrieve it later with `ct.df('name')`.**

Why?

- Dataframes cached in chart-tools are effectively immutable.
- Calling `ct.df('name')` will always return a duplicate of the cached file, as if you had loaded it fresh all over again to make sure you're getting the original data.
- This not only prevents the bugs mentioned above, but it simplifies your code because you never had to declare a 'df_raw_data' or equivalent.
- It also makes your code easier to read when working with multiple source files, since it's absolutely clear: 1.) that you're retrieving unaltered source data. 2.) exactly which data you're retrieving. 'df_raw_data', however, is less descriptive or strict.

Example:

```py
import chart_tools as ct
ct.load_data("animals", "tiger", index_col=0, names=['some col', 'other col', 'third col'])
```

Later...

```py
df = ct.df('tiger') # Do this as many times as you like
```

#

---

<br>

# Create your own `DataSource`

Let's build a source for my [`/datasets`](https://github.com/ryayoung/datasets) repository.

#

Option 1: url to sub-directory inside repo

> Notice this link includes the branch since we copied it while in a sub-directory

```py
s = ct.DataSource('github.com/ryayoung/datasets/tree/main/data')
```

#

Option 2: url to repository home page

> This url won't contain a branch, so chart-tools will make a request to figure out what the default branch is

```py
s = ct.DataSource('github.com/ryayoung/datasets')
```

> We can speed things up (prevent that additional request) by specifying a branch

```py
s = ct.DataSource('github.com/ryayoung/datasets', branch='main')
```

#

Option 3: Define explicitly

> This code will run slightly faster since we didn't have to validate or parse a url string
  
```py
s = ct.DataSource('ryayoung', 'datasets', 'main', 'data')
print(s.datasets)
```
```
['ames_engineered', 'ames_full', 'ames_mini', 'stock-tweets']
```

> The sub-path isn't necessary, but without it, files will have longer names

```py
s = ct.DataSource('ryayoung', 'datasets', 'main')
print(s.datasets)
```
```
['data/ames_engineered', 'data/ames_full', 'data/ames_mini', 'data/stock-tweets']
```

#

Option 4: Just the user and repo

> Just like the short url in Option 2 above, the branch will be unknown, so chart-tools will make a request to find the default branch

```py
s = ct.DataSource('ryayoung', 'datasets')
```

#

Let's load `data/ames_mini`

> Since there's only one file in all our sub-directories called 'ames_mini', we can leave out the 'data/' and the file will be found.

```py
s.load("ames_mini")
```

<img width="451" alt="Screen Shot 2022-04-23 at 11 46 43 PM" src="https://user-images.githubusercontent.com/90723578/164958463-8621bc79-562b-4d91-8222-d684e3cccb3c.png">

#

#### Let's take a closer look at our DataSource

```py
print(s.subdirs)
print(s.datasets)
print(s.datasets_base)
```
```
['data']
['data/ames_engineered', 'data/ames_full', 'data/ames_mini', 'data/stock-tweets']
['ames_engineered', 'ames_full', 'ames_mini', 'stock-tweets']
```

Since we're only working inside `data/`, why not update our path?

```py
s.path = 'data'
# chart-tools notices the path change, and updates file structure accordingly
print(s.subdirs)
print(s.datasets)
print(s.datasets_base)
```
```
[]
['ames_engineered', 'ames_full', 'ames_mini', 'stock-tweets']
['ames_engineered', 'ames_full', 'ames_mini', 'stock-tweets']
```

#

#### Remember, the `load` and `load_data` functions can take any keyword arguments you'd use with `pd.read_csv()`

```py
s.load("ames_mini", index_col=0, usecols=['Id', 'OverallCond', 'LotArea'])
```

<img width="210" alt="Screen Shot 2022-04-23 at 11 59 39 PM" src="https://user-images.githubusercontent.com/90723578/164958838-2c1bf900-63c3-4d87-b29e-99ac852f078b.png">

#### And just to recap how caching works...

```py
# This works, even though we never assigned the s.load() above to a variable
s.df('ames_mini') 
```

<img width="210" alt="Screen Shot 2022-04-23 at 11 59 39 PM" src="https://user-images.githubusercontent.com/90723578/164958838-2c1bf900-63c3-4d87-b29e-99ac852f078b.png">

#

#### Let's use a more complex source, [`/football-datasets`](https://github.com/datasets/football-datasets/tree/master/datasets) in github's `datasets` account

```py
s = ct.DataSource("datasets", "football-datasets", "master", "datasets")

s.display_datasets(trunc=14, header=False) # truncate to show 14 results max
```
```
  la-liga/
    season-0809
    season-0910
    season-1011
    season-1112
    season-1213
    season-1314
    season-1415
    season-1516
    season-1617
    season-1718
    season-1819
  serie-a/
    season-0809
      (38 more files in datasets/football-datasets)
```

> View sub-directories that contain one or more csv files
```py
s.subdirs
```
```
['la-liga', 'serie-a', 'ligue-1', 'premier-league', 'bundesliga']
```

> See all the files in a sub-directory

```py
s.dir_contents('serie-a')
```
```
['season-0809', 'season-0910', 'season-1011', 'season-1112', 'season-1213', 'season-1314', 'season-1415', 'season-1516', 'season-1617', 'season-1718', 'season-1819']
```

> In the football source, files share the same names across directories. So we need to use the full path when loading them

```py
s.load("serie-a/season-0809")
```

<img width="472" alt="Screen Shot 2022-04-24 at 12 19 39 AM" src="https://user-images.githubusercontent.com/90723578/164959543-69abf757-1eff-4a36-9d94-f5c463b00ea8.png">

#

#### View the api request urls that have been making all the magic happen

> URL used to get repository file structure from Github's api

```py
s.req_url
```
```
https://api.github.com/repos/datasets/football-datasets/git/trees/master?recursive=1
```

> URL to an individual file's raw contents

```py
s.file_url('la-liga/season-0809')
```
```
https://raw.githubusercontent.com/datasets/football-datasets/master/datasets/la-liga/season-0809.csv
```

> URL you can paste in your browser to visit source

```py
s.root
```
```
https://github.com/datasets/football-datasets/tree/master/datasets
```

<br>

---

<br>

# Define your own [`Library`](#library) of data sources

The pre-defined sources in chart-tools are _NOT_ defined in the source code. Only a _url_ defining a `Library` is stored. When you use `ct.load_data()`, the library configuration gets downloaded and used to create a `Library`: a default collection of DataSources for you to interact with and load data from. The default can be changed!

### What's a library?

- A library is a simple JSON structure that defines DataSources, and assigns a custom name to each. Here's an example:

```
{
    "main": {
        "u": "ryayoung",
        "r": "datasets",
        "b": "main",
        "p": "data"
    },
    "covid": {
        "u": "datasets",
        "r": "covid-19",
        "b": "main",
        "p": "data"
    }
}
```

1. This defines two DataSources, 'main' and 'covid', and specifies a `u`: Github user, `r`: repository, `b`: branch, `p`: path.
2. Chart-tools has a pre-defined `default_library`, but you can change it.
3. You can use `ct.load_data()` to interact directly with the default Library without the need to define or reference one.

### How to define a Library

> The examples below alter the `default_library` using global functions (recommended). If you want to create a separate Library object, modify the examples below to the format, `my_library = Library("stuff")` instead of `ct.set_library("stuff")`.

#### _Option 1: cloud_

- Upload a json file to one of your repositories, go to the RAW file, and copy the url
  
```py
ct.set_library("https://raw.githubusercontent.com/[USER]/[REPO]/[BRANCH]/[FILENAME].json")
```

#### _Option 2: local_

```py
ct.set_library("my_sources.json")
```

#### _Option 3: dict_

```py
my_lib_info = {
    # Paste the example template from above
}
ct.set_library(my_lib_info)
```

#

More details coming soon. For now, read the source code for `Library` [here](https://github.com/ryayoung/chart-tools/blob/main/src/chart_tools/data/library.py), where it's up-to-date and well-documented with comments.
