from dataclasses import dataclass
from operator import countOf
import pandas as pd
import requests
import json
import os
from hashlib import md5

from chart_tools.data.dfcache import DFCache

# TODO:
# load() function won't find base filenames when subdirectories
# go more than 1 layer deep


def check_internet():
    """ Don't do internet stuf if no internet """
    try:
        request = requests.get("https://www.google.com/", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout) as e:
        return False


@dataclass
class Source:
    """
    Defines a location in a Github repository that stores csv files.
    ---
    This is the 'backend' for DataSource and Library. Handles everything
    EXCEPT constructor logic, user input validation, neatly formatted
    outputs of the source's contents, and Library compatibility.
    ---
    - Only requests the contents (file structure) of the repository
      once that information is accessed as a property.
    - Loaded dataframes are cached based on keyword args (those passed
      to pd.read_csv()). See DFCache for more info
    - Ability to write entire datasource, preserving its file structure,
      to computer with one function. This is different from cloning the
      repo. It downloads only csv files, and any pandas kwargs
      passed (for pd.read_csv()) get applied to all datasets.
    """
    __user: str
    __repo: str
    __branch: str
    __path: str

    __datasets = [] # Names of all csv files in repository. Our github
    # api request returns full filepath starting at root, so our optional
    # 'path' variable should be trimmed away from the prefix

    __datasets_full = [] # Full filepath from root, as returned from
    # github api request, trimmed only of the .csv at the end. This
    # is used only for validation purposes, to correct user mistakes
    # and make sure we build a valid url before loading data.

    cache = DFCache() # DFs cached after user loads them. See DFCache

    # Getters
    @property
    def user(self):
        return self.__user.strip("/")
    @property
    def repo(self):
        return self.__repo.strip("/")
    @property
    def branch(self):
        return self.__branch.strip("/")
    @property
    def path(self):
        return self.__path.strip("/")

    @property
    def datasets(self) -> list:
        """
        Load datasets only when we try to access them
        """
        if self.__datasets == []:
            self.refresh_datasets()
        return self.__datasets

    @property
    def datasets_full(self) -> list:
        """
        Load datasets only when we try to access them
        """
        if self.__datasets_full == []:
            self.refresh_datasets()
        return self.__datasets_full

    # Getters - calculated
    @property
    def subdirs(self) -> list:
        """
        First layer of sub-directories in datasource.
        """
        return list(set([
                f.split('/')[0] for f in self.datasets if "/" in f
            ]))

    @property
    def datasets_base(self) -> list:
        """
        Base filenames, without path
        """
        return [f.rsplit('/', 1)[-1] for f in self.datasets]

    @property
    def root(self) -> str:
        """
        User-friendly url to visit the source on Github.com
        """
        return f"https://github.com/{self.user}/{self.repo}/tree/{self.branch}/{self.path}"
    
    @property
    def req_url(self) -> str:
        """
        Url to Github API for getting all files in repo and branch
        """
        return f"https://api.github.com/repos/{self.user}/{self.repo}/git/trees/{self.branch}?recursive=1"

    # Setters - include validation logic
    @user.setter
    def user(self, value):
        if "/" in value:
            raise ValueError("Github username can't have slashes")
        self.__user = value

    @repo.setter
    def repo(self, value):
        if "/" in value:
            raise ValueError("Github repository name can't have slashes")
        self.__repo = value

    @branch.setter
    def branch(self, value):
        if "/" in value:
            raise ValueError("Github branch name can't have slashes")
        self.__branch = value

    @path.setter
    def path(self, value):
        if value.endswith("/"):
            raise ValueError("Path must not end with a slash")
        self.__path = value
        # Update datasets since path changed, but only if we have valid data
        if self.user != "" and self.repo != "" and self.branch != "":
            self.refresh_datasets()


    def file_url(self, filename) -> str:
        """
        Url to raw, downloadable file
        """
        path = f"{self.path}/" if len(self.path) > 0 else self.path
        return f"https://raw.githubusercontent.com/{self.user}/{self.repo}/{self.branch}/{path}{filename}.csv"


    def req_files(self) -> list:
        """ Request files """
        if check_internet():
            return requests.get(self.req_url).json()
        return None
    

    def dir_contents(self, dir) -> list:
        """ Get filenames in directory """
        return [f.removeprefix(f"{dir}/") for f in self.datasets if f.startswith(dir)]


    def load(self, fname, save=True, **kwargs) -> pd.DataFrame:
        """
        Given a filename, return a dataframe!
        ---
        Idiot-proof user input for different ways of referring to files.
        - If they pass filename 'cool-data' and we find a file called
          'data/cool-data', AND no other sub-dir contains a file with that name,
          then let's load it for em!
        - If they accidentally put their defined source path, redundantly, in
          the filename, then let's be nice and figure it out
        ---
        About cache, and the 'save' argument:
        - Add to cache only when save is true
        - If save is false, remove an existing cache if exists for
          that file, but only if dataframes match (same kwargs)
        """

        # -------- IMPORTANT --------------
        # THIS IF-ELSE BLOCK NEEDS TO MOVE TO DATASOURCE CLASS.
        # THEN, DATASOURCE CLASS NEEDS A "LOAD()" FUNCTION
        # ----------------------------------
        # Validate dataset name exists, and modify as necessary
        # This also validates that datasets are loaded and connection to GH works
        name = None
        if countOf(self.datasets, fname) == 1:
            name = fname

        elif countOf(self.datasets, fname.split('/')[-1]) == 1:
            name = fname.split('/')[-1]

        elif countOf(self.datasets_full, fname) == 1:
            name = fname.removeprefix(f"{self.path}/")

        else:
            raise ValueError(
                "Either the file doesn't exist, or your query matched more than one file.\n"
                "If the latter is true, make sure to use the full subpath.\n"
                "Hint: Here's the url that would have been used, but it was detected as invalid:\n"
                f"{self.file_url(fname)}"
                )

        # Cache
        if self.cache.df_matches(name, **kwargs):
            df = self.cache.get(name)
            if not save:
                # Pop existing cache for that version of the data if exists
                self.cache.pop(name)
            return df

        # Load new data, cache, and return
        df = pd.read_csv(self.file_url(name), **kwargs)
        if save:
            self.cache.add(fname, df, **kwargs)

        return self.cache.get(name)
        

    def save_all(self, dir="", **kwargs):
        # Make directory for custom path
        if dir != "":
            p = ""
            for d in dir.split("/"):
                if p != "":
                    p = f"{p}/{d}"
                else:
                    p = d
                if not os.path.exists(p):
                    os.mkdir(p)

        # Make directories for all sub-paths
        for name in self.datasets:
            fullpath = name.split("/")
            if dir != "":
                fullpath = [dir] + fullpath
            p = None
            if len(fullpath) > 1:
                path = fullpath[:-1]
                p = ""
                for d in path:
                    if p != "":
                        p = f"{p}/{d}"
                    else:
                        p = d
                    if not os.path.exists(p):
                        os.mkdir(p)

        # Save datasets.
        for name in self.datasets:
            # Pass save argument false if it's not already cached,
            # because we don't want to cache everything. But if it is
            # cached, overwrite it with the new kwargs
            save = False if not self.cache.has_key(name) else True
            df = self.load(name, save=save, **kwargs)
            if dir != "":
                df.to_csv(f"{dir}/{name}.csv", **kwargs)
            else:
                df.to_csv(f"{name}.csv", **kwargs)
        

    def refresh_datasets(self):
        res = self.req_files()
        if not res:
            return []

        if res.get("message") == "Not Found":
            raise ValueError("No files found. Likely an invalid data source")

        full_paths = [f['path'].removesuffix('.csv')
                        for f in res['tree'] if ".csv" in f['path']]
        
        self.__datasets_full = full_paths
        
        self.__datasets = [f.removeprefix(f"{self.path}/") for f in full_paths]






