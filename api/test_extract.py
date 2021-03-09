import os
import json
import subprocess
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import dill
import pandas as pd
from sklearn.feature_extraction import text
from standard_extractor import find_standard_ref
from text_analysis import extract_prep

"""
TODO: 1) Run where ES is connected and do tests.
      2) exit()
"""
test = extract_prep.predict(in_text="test")
print(test)