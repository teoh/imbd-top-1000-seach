import pandas as pd
import numpy as np
from tqdm import tqdm
from functools import reduce
import itertools

from bs4 import BeautifulSoup
from requests import get
import re


class MovieIndex():
    def __init__(self, num_pages, base_url):
        self.num_pages = num_pages
        self.base_url = base_url
        self.titles = None
        self.keyword_to_indices = None

    def build(self):
        '''This builds the search index of the movies.

        Input: no input

        Returns: nothing, but the calling object will
            now have a list of movie titles, and dict
            mapping possible keywords to indices (in the
            movie title list) that are related to the
            keyword
        '''
        movie_info_list = []
        print('Getting info from IMDB pages and building index...')
        for i in tqdm(range(1, self.num_pages + 1)):
            page_url = self.base_url.format(i)
            movie_info_list += self.get_movie_info_from_page(page_url)

        self.titles = list(map(lambda d: d['title_pretty'], movie_info_list))
        self.keyword_to_indices = self.make_keyword_map(movie_info_list)

    def search(self, search_string):
        '''
        Finds the relevant movies given a search
        string query.

        Input:
            search_string: a space-separated string
                of keywords

        Returns:
            list of titles related to the search string

        '''
        list_of_terms = search_string.lower().split(' ')
        index_sets = list(filter(lambda idx_set: idx_set is not None,
            map(lambda term: self.keyword_to_indices.get(term,None),
                list_of_terms)))

        if not index_sets:
            return []

        relevant_indices = reduce(lambda set1,set2: set1 & set2, index_sets)

        return [self.titles[i] for i in relevant_indices]

    def make_keyword_map(self,movie_info_list):
        '''
        Creates a dictionary that maps keywords to
        relevant movies.

        Input:
            movie_info_list: a list of dicts with fields
                for genre, people, and title

        Output:
            keyword_map: {keyword -> {set of relevant movie
                                        indices} }

        '''

        keyword_map = {}
        for i, movie_info in enumerate(movie_info_list):
            for g in movie_info['genres']:
                self.add_to_dict(keyword_map,g,i)

            for name in movie_info['people']:
                for name_part in name.split(' '):
                    self.add_to_dict(keyword_map,name_part,i)

            for word in movie_info['title_lower'].split(' '):
                word = re.sub(r'[^\w\s]','',word)
                if word:
                    self.add_to_dict(keyword_map,word,i)
        return keyword_map

    def add_to_dict(self,k_map,itm,i):
        '''
        Simple function to check for key
        membership in a dict and add the value
        accordingly

        '''
        if itm not in k_map.keys():
            k_map[itm] = {i}
        else:
            k_map[itm].add(i)

    def get_movie_info_from_page(self, page_url):
        '''Gets info on movies from page_url

        Input:
            page_url: url of page that we'll get
                movies from

        Output:
            movies_info_from_page: list of dicts
                with fields for genre, movie, and
                title

        '''
        response = get(page_url)

        html_soup = BeautifulSoup(response.text,'html.parser')
        movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')

        movies_info_from_page = []

        for movie in movie_containers:
            print(type(movie))
            movies_info_from_page.append(self.extract_single_movie(movie))

        return movies_info_from_page

    def extract_single_movie(self, movie):
        '''Extracts info for one movie

        Input:
            movie: a bs4.element.Tag object
                describing information for one
                movie

        Output:
            movie_res: dictionary with fields
                describing genre, title, and
                people for the movie

        '''
        movie_res = {}

        # title
        movie_title = movie.h3.a.text
        movie_res['title_pretty'] = movie_title
        movie_res['title_lower'] = movie_title.lower()

        # genres
        raw_genre_list = movie.find('p', class_ = 'text-muted').\
            find('span', class_ = 'genre').text[1:].split(',')
        movie_res['genres'] = list(map(lambda x: x.lower().lstrip().rstrip(),raw_genre_list))


        director_stars_info = movie.findAll('p', class_='')[-1]
        if 'Director' not in director_stars_info.text or 'Stars' not in director_stars_info.text:
            print(f'''movie = {movie_title}. Could not find Directors or Stars''')

        # Get people info, no need to distinguish director from stars
        people = list(map(lambda x: x.text.lower(), director_stars_info.findAll('a')))

        movie_res['people'] = people

        return movie_res


