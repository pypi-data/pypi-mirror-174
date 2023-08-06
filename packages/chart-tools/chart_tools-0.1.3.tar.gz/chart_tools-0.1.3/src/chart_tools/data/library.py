from chart_tools.data.datasource import DataSource
from operator import countOf
import pandas as pd
import requests

class Library:
    """
    Designed for use with Jupyter notebooks. Stores a list of DataSources,
    and interactive functions for exploring and loading data.
    ---
    Created by passing EITHER:
        - A url to a json file in the cloud
        - A path to a local json file
        - A dict with the necessary format
    ---
    File must follow a specific format: It must be a dict
    of dicts, where each sub-dict has keys 'u', 'r', 'b', 'p'.
    For example:
    ---
    {
        "some_nickname": {
            "u": "some-github-username",
            "r": "some-github-repo",
            "b": "some-branch",
            "p": "some-subdirectory" (optional - use empty str if none)
        },
        "other_nickname": {
            . . .
        }
    }
    ---
    A default instance, 'default_lib' is declared immediately at import,
    linking to a library stored at: ryayoung/datasets/chart-tools-default-library.json
    """
    load_help = True
    load_help_all = True

    def __init__(self, url):
        self.url = url
        self.data = None
        self.sources = None

        self.set(self.url)

    def __repr__(self):
        if self.sources != None:
            string = ""
            for s in self.sources.values():
                string += s.__repr__() + "\n"
            return string
        
    def set(self, url):
        # Dict
        if type(url) == dict:
            self.data = url

        # Online library
        elif url.startswith("https"):
            try:
                self.data = dict(requests.get(url).json())
            except Exception as e:
                print("Error getting library data")
                self.data = None
        # Local library
        else:
            try:
                with open(url) as f:
                    self.data = json.load(f)
            except Exception as e:
                print(e)
                self.data = None
        
        if self.data:
            # Make sure library follows correct structure
            for key in list(self.data.keys()):
                if not sorted(list(self.data[key].keys())) == sorted(['u', 'r', 'b', 'p']):
                    raise ValueError("Wrong library structure. Keys must be ['u', 'r', 'b', 'p']")

            self.url = url
            self.sources = { k: DataSource(v['u'], v['r'], v['b'], v['p'], name=k) for k, v in self.data.items() }

    
    def display_sources(self) -> None:
        """ Just source names and github links """
        if self.sources:
            for s in self.sources.values():
                print(f" '{s.name}':{(10-len(s.name))*' '}{s.root}")


    def display_all(self) -> None:
        """
        Dispays all files in all sources, truncated at
        15 files per source
        """
        if not self.sources:
            return
        
        for s in self.sources.values():
            if s.datasets == []:
                continue
            print(f"'{s.name}'  -  {s.root}")
            print("---------------------------------")
            s.display_datasets(header=False, trunc=15)
            print()
    

    def load_data(self, source:str=None, file:str=None, save=True, **kwargs) -> pd.DataFrame:
        """
        Loads data in a user-friendly way
        ---
        No params:
        - Provides help on loading data
        One positional argument:
        - If 'all', display all sources and files in default library
        - If name is in default lib datasets, load it
        Two positional arguments:
        - Simply look for the file in provided source
        """
        if not self.sources:
            return
        
        if not source and not file:
            if Library.load_help:
                print("Use load_data(source_name, filename) to load dataframe")
                print("Use load_data(source_name) to see all datasets in a source.")
                print("Use load_data('all') to see all datasets.")
                Library.load_help = False
            print("---------\nSOURCES:")
            self.display_sources()
            return ""
        
        if source == 'all' and not file:
            if Library.load_help_all:
                print("(Use load_data(source_name, filename) to load data)")
                print("(Use load_data(source_name) to see available datasets in source)")
                print("")
                Library.load_help_all = False
            self.display_all()
            return ""
        
        if not file:
            if source in self.sources.keys():
                self.sources[source].display_datasets(header=True)
                return None
            if "main" in self.sources:
                # Shorthand: access contents of 'main' datasource
                # by providing only the filename!
                if source in self.sources.get("main", {}).datasets:
                    return self.sources['main'].load(source, save, **kwargs)

            print(f"Unknown source, '{source}'")
            return
    
        if source not in self.sources:
            print(f"Unknown source, '{source}'")
            return
        
        if self.sources[source].datasets != []:
            return self.sources[source].load(file, save, **kwargs)


    def df(self, filename) -> pd.DataFrame:
        """
        Looks for filename in the cache of EACH datasource
        in the library, and returns the first match.
        ---
        The intended workflow for this function would be to run
        'ct.load_data(...)' at the top of your notebook with the import
        statements, and then assign it to a variable later on, when needed
        """
        if not self.sources:
            return

        for s in self.sources.values():
            # This time, DO NOT access the source's datasets property.
            # That will force us to request file structure for each source
            # we loop through. That's not good.
            name = None
            if s.cache.has_key(filename):
                name = filename
            elif s.cache.has_key(filename.split('/')[-1]):
                name = filename.split('/')[-1]
            else:
                continue

            return s.cache.get(name)

        raise ValueError(
                f"Unable to find '{filename}' cached in any of the library's sources.\n"
                f"Try ct.load_data(source_name, 'ames_mini') instead. "
                )



# --------------------------------------------------------------------------------
default_library = Library("https://raw.githubusercontent.com/ryayoung/datasets/main/chart-tools-default-library.json")


def default_lib_url():
    return default_library.url


def reset_library():
    default_library.set("https://raw.githubusercontent.com/ryayoung/datasets/main/chart-tools-default-library.json")


def default_lib():
    return default_library.sources


def set_library(url):
    default_library.set(url)


def load_data(source=None, file=None, save=True, **kwargs) -> pd.DataFrame:
    return default_library.load_data(source, file, save, **kwargs)


def df(fname) -> pd.DataFrame:
    return default_library.df(fname)


def library_help():
    print("""Library: Create a json file containing a dict of dicts,
where each sub-dict is keyed with a string nickname for a DataSource,
and contains the following keys: 'u', 'r', 'b', 'p', which represent a
github user, repository, branch, and sub-path where all the datasets
and other sub-directories are stored. Path ('p') should be left as an
empty string if not needed.
---------
{
    "some_nickname": {
        "u": "some-github-username",
        "r": "some-github-repo",
        "b": "some-branch",
        "p": "some-subdirectory" (optional - use empty str if none)
    },
    "other_nickname": {
        . . .
    }
}
---------
""")
