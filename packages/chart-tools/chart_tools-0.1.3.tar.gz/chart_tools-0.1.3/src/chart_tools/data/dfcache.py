import pandas as pd
import os
from dataclasses import dataclass


@dataclass
class DFCache:
    """
    Stores cached dataframes for a Source.
    ---
    Ensures dataframes are kept unique NOT just by their
    key (filename), but by the keyword arguments used when
    loading the data from pd.load_csv(). For instance, if a
    user loads a file by passing 'index_col=1', the cached
    dataframe will be missing its first column. If the user
    tries to load it again, without this keyword argument,
    we DO NOT want to return the cached data, and instead
    must download it again and replace the cache. To do this,
    we cast kwargs to a string, and store it beside the df.
    For a given filename, two dataframes are considered equal
    if their kwargs are the same.
    ---
    Structure of self.__cache:
    {
        "some-filename": {
            "df": pd.DataFrame(),
            "kwargs": str(**kwargs)
        },
        "other_filename": {
            . . .
        }
    }
    ---
    DataSource, Source, and Library are meant for Jupyter notebooks,
    where the biggest performance gain is to be had from caching. They should
    never be used in a production setting, as they would be very slow.
    """
    __cache = dict()

    @property
    def cache(self) -> dict:
        return self.__cache

    def has_key(self, key) -> bool:
        return key in self.__cache.keys()

    def df_matches(self, key, **kwargs) -> bool:
        if self.has_key(key):
            return self.cache[key]['kwargs'] == str(kwargs)
        return False

    def add(self, key, df, **kwargs):
        self.cache[key] = {'df':df, 'kwargs': str(kwargs)}

    def pop(self, key) -> bool:
        if self.has_key(key):
            self.cache.pop(key)
            return True
        return False

    def get(self, key) -> pd.DataFrame():
        if self.has_key(key):
            return self.cache[key]['df'].copy()
        return pd.DataFrame()


    def to_csv(self, dir="", **kwargs):
        """
        Saves all cached dfs to computer
        Kwargs are for pandas to_csv
        """
        if dir != "":
            if not os.path.exists(dir):
                os.mkdir(dir)
            dir = f"{dir}/"
        for name, item in self.cache.items():
            item['df'].to_csv(f"{dir}{name}.csv", **kwargs)


