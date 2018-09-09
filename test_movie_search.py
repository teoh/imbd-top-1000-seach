import pandas as pd
import numpy as np
from tqdm import tqdm
from functools import reduce
import itertools

from bs4 import BeautifulSoup
from requests import get
import re

from movie_search import MovieSearch

print('Initializing MovieSearch object...')
imdb_search_1000 = MovieSearch()
print('Done initializing MovieSearch object!')


print('Generating the search index...')
imdb_search_1000.create_index()
print('Done generating search index!')

search_term_list = [
        'Nolan',
        'Nolan Bale',
        'Chris Pratt',
        'Lord of the',
        'spielberg',
        'spielberg hanks'
]
for search_term in search_term_list:
    print(f'''Search terms for '{search_term}': {imdb_search_1000.search(search_term)} ''')
