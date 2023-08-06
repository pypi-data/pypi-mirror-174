import chart_tools as ct
from dataclasses import dataclass
import time
import requests
from operator import countOf



# ct.load_data()

# print(ct.default_lib())
# dlib = ct.default_lib()
# ct.set_library("https://raw.githubusercontent.com/ryayoung/datasets/main/test-library.json")
# ct.load_data()

# print(dlib.values())

# for v in dlib.values():
    # print(v.datasets)

# football = dlib['football']

# print(football.root)

openml = ct.DataSource("github.com/datasets/football-datasets", path="datasets")
openml.display_datasets()

# s = ct.DataSource(name="main")
# print(s.datasets_base)


# ct.set_library("https://raw.githubusercontent.com/ryayoung/datasets/main/test-library.json")

# ct.library_help()
# print(s.load('ames_mini'))
# 
# 
# name = "data/ames"
