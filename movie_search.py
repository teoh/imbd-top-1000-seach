import pandas as pd
import numpy as np
from tqdm import tqdm
from functools import reduce
import itertools

from bs4 import BeautifulSoup
from requests import get
import re

from movie_index import MovieIndex

NUM_PAGES = 20
BASE_URL = 'https://www.imdb.com/search/title?groups=top_1000&sort=user_rating&page={0}'

class MovieSearch():
    def __init__(self):
        self.index = None

    def create_index(self):
        self.index = MovieIndex(NUM_PAGES, BASE_URL)
        self.index.build()

    def search(self, search_string):
        if not self.index:
            print('Index needs to be built. Please run the `.create_index()` method first.')
        else:
            return self.index.search(search_string)
