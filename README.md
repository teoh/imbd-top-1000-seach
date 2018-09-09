# imbd-top-1000-seach
In this project, I make a simple search index for the top 1000 movies on IMDB.

# How do I do it? 
For each of the top 1000 movies (you can find them [here](https://www.imdb.com/search/title?groups=top_1000&sort=user_rating&page=1)), I build an index using the title, genre(s), director(s), and starring actor(s). I map each keyword (a keyword can be any word appearing in the title or genre, or part of a director's/actor's name), to the set of movie titles that it appears in.

# How does the index get used?
For each word in your search string, the index finds the set of movie titles with metadata (including directors, genres, actors) containing those words. The index return the intersection of all these sets. 

For example, if you searched `'a b'` (`'a'` appears in movies `[1,2,3]` and `'b'` appears in movies `[2,3,4]`), the final result will be `[2,3]`. 

# Assumptions
My approach assumes that:
* The bulk of the information that users would search for is contained in the movie title, genres, directors, and actors
    * This greatly simplifies the problem so that we can use the keyword mapping as above. These seemed like common things someone would look up, rather than things like rating. 
* Each search term is equally important 
    * This was easier to implement. 
* Relevance and ranking is not a priority here


# How to use this API

Setup index for queries:
```
from movie_search import MovieSearch

imdb_search_1000 = MovieSearch()
imdb_search_1000.create_index()
```

If your search term is contained in `search_term`, run `imdb_search_1000.search(search_term)}`:
```
search_term_list = [
        'Nolan',
        'Nolan Bale',
        'spielberg',
        'spielberg hanks'
]
for search_term in search_term_list:
    print(f'''Search terms for '{search_term}': {imdb_search_1000.search(search_term)} ''')
```

This should output:
```
Search terms for 'Nolan': ['The Dark Knight', 'The Prestige', 'Dunkirk', 'Inception', 'Memento', 'Following', 'Batman Begins', 'Interstellar', 'The Dark Knight Rises']
Search terms for 'Nolan Bale': ['The Dark Knight', 'Batman Begins', 'The Dark Knight Rises', 'The Prestige']
Search terms for 'spielberg': ['Raiders of the Lost Ark', 'Catch Me If You Can', 'Munich', "Schindler's List", 'Empire of the Sun', 'Minority Report', 'Ready Player One', 'Bridge of Spies', 'Jurassic Park', 'Jaws', 'Close Encounters of the Third Kind', 'Indiana Jones and the Temple of Doom', 'Saving Private Ryan', 'E.T. the Extra-Terrestrial', 'Indiana Jones and the Last Crusade', 'The Color Purple']
Search terms for 'spielberg hanks': ['Bridge of Spies', 'Saving Private Ryan', 'Catch Me If You Can']
m
```

This code can be found in `test_movie_search.py`

# Opportunities for improvement:
* Remove common words like "the" from the index to save space
*

