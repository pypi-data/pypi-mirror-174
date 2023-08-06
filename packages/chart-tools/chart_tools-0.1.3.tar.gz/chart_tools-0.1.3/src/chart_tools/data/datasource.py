from chart_tools.data.source import Source
import requests

# TODO:
# DataSource version of .load() should work like the
# load_data() in Library, to explore file structure

class DataSource(Source):
    """
    Similar to Source, but provides high level, user-friendly experience
    for initialization, displaying contents, and Library interaction.
    ---
    Has one extra property, 'name', which is ONLY needed or used when self is
    stored in a Library: it's the key used to access self from a Library
    ---
    Adds logic and validation to constructor:
        - Init from an existing datasource in default_lib by passing only name
        - Sets name to repo if no name provided
        - Idiot-proof declaration with validation
    ---
    DataSource, Source, and Library are meant for Jupyter notebooks,
    where the biggest performance gain is to be had from caching. They should
    never be used in a production setting, as they would be very slow.
    """

    def __init__(self,
            user=None,
            repo=None,
            branch=None,
            path="",
            *,
            name=None,
            url=None,
        ):

        if name:
            self.name = name
        else:
            self.name = repo

        # OPTION 1: url as positional in user, or url kwarg
        if "github.com/" in str(user) or url:
            if url:
                self.init_from_url(url, path)
            else:
                self.init_from_url(user, path)

        # OPTION 2
        elif user and repo and branch:
            super().__init__(user, repo, branch, path)

        # OPTION 3: Given user and repo, request default branch and init
        elif user and repo:
            branch = self.request_branch(user, repo)
            super().__init__(user, repo, branch, "") # Always empty path if branch unknown

        else:
            if user or repo or branch or name:
                raise ValueError(
                        "Invalid DataSource declaration. Either provide a name "
                        "of an existing datasource within the default library (name='...'), "
                        "or pass (user, repo, branch, path) defining a github repository "
                        )


    def init_from_url(self, url, path):
        """
        Constructs a Source, given only a url and optional
        sub-path. Validate the url and correct for errors first.
        """
        # Standardize format: 3 valid options: https, http, or none
        url = url.removeprefix("https://") \
                 .removeprefix("http://")

        if not url.startswith("github.com/"):
            err_url(url)

        items = url.removeprefix("github.com/") \
                   .removesuffix("/") \
                   .split("/")

        self.user = items[0]
        self.repo = items[1]

        if len(items) == 2:
            # If they link to root of repo, we don't know the branch. Go find it
            self.branch = self.request_branch(self.user, self.repo)
            self.path = path

        elif items[2] == "tree" and len(items) > 3:
            # Now we know it's a valid format. So we can create the datasource
            # successfully. Info gets validated later, once we access self.datasets
            self.branch = items[3]
            self.path = "/".join(items[4:])

        else:
            err_url(url)

        super().__init__(self.user, self.repo, self.branch, self.path)


    def err_url(url):
        """ Descriptive error for an invalid url used for construction """
        raise ValueError(
                f"Invalid url: {url}.\nValid formats:\n"
                "1. https://github.com/[USER]/[REPO]/tree/[BRANCH]/[DIR]\n"
                "2. https://github.com/[USER]/[REPO]"
                )


    def request_branch(self, user, repo):
        """
        Called from init when only name and repo are known.
        Called from init_from_url when ROOT link to repo is passed, in which
        case the branch is unknown.
        """
        req_url = f"https://api.github.com/repos/{user}/{repo}?recursive=1"
        res = requests.get(req_url).json()
        return res['default_branch']


    def display_datasets(self, header=False, trunc=1000):
        """
        Display datasets inside source, truncated if asked.
        Format differently if there are sub-directories.
        """
        if self.datasets == []:
            return
        if header:
            if self.name != None:
                print(f"Datasets for '{self.name}':")
            if self.name == None:
                print(f"Datasets in '{self.user}/{self.repo}/{self.path}':")
            if len(self.subdirs) > 0:
                print("(refer files inside folders using the full path. Ex: 'folder/file')")
            print("---------------------------")
        
        # Files in base directory
        for file in [f for f in self.datasets if "/" not in f]:
            print(f"  {file}")

        # Files in subdirectories
        count = 0
        for dir in self.subdirs:
            print(f"  {dir}/")
            count += 1
            for f in self.dir_contents(dir):
                count += 1
                if count > trunc: break
                print(f"    {f}")

            if count > trunc: break

        if count > trunc:
            name = self.name if self.name else f"{self.user}/{self.repo}"
            print(f"      ({len(self.datasets)-count} more files in {name})")
    

    def display_subdirs(self, header=False):
        if header:
            if self.name != None:
                print(f"Datasets for '{self.name}':")
            else:
                print(f"Sub-directories in '{self.user}/{self.repo}/{self.path}'")
            print("---------------------------------------")
            print("  ", end="")
            print(*self.subdirs, sep="\n  ")
        else:
            print(*self.subdirs, sep="\n")


    def __repr__(self):
        if self.name != None:
            return f"{self.name}:{(10-len(self.name))*' '}{self.root}"
        else:
            return (f"{self.user}/{self.repo}:"
                    f"{(20-(len(self.repo)+len(self.repo)))*' '}{self.root}")




