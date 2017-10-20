'''
Created on 18 oct. 2017

@author: tecuapan
'''
# from imdb import IMDb
ia = IMDb()
from lxml import html
import requests
#
movie['synopsis'] = ''
movie['storyline'] = ''
movie['description']= ''
movie['text'] = ''
# Looping over movies
for index, row in movie.iterrows():
    if (row['IMDb url'] != 'unknown'):
        # Get the html content 
        page = requests.get(row['IMDb url'])
        tree = html.fromstring(page.content)
        try:
            # Get the movie id 
            idm = tree.xpath('/html/head/meta[6]')[0].get('content')[2:]
            # Get the story line
            movie.loc[index, 'storyline'] = tree.xpath('//*[@id="titleStoryLine"]/div[1]/p/text()')[0]
            # Get the movie using the IMDB library based on the movie id
            m = ia.get_movie(idm)
            # Get the descreption 
            movie.loc[index, 'description'] = m.get('plot outline')
            # Get the synopsis
            ia.update(m, 'synopsis')
            if m.get('synopsis') is not None:
                movie.loc[index, 'synopsis'] = m.get('synopsis')
        except IndexError:
            pass
    # Create a text field to concatenate all existing summaries
    movie.loc[index, 'text'] = movie.loc[index, 'description'] + ' ' + movie.loc[index, 'storyline'] + ' '+ movie.loc[index, 'synopsis']
When the URL doesn't redirect to the right page, we can use the IMDb library to get information about a movie based on its title using the search_movie(title) function. However, this function is a simple search action which returns a list of movies sorted by relevance. In the following code, we ensure that the first element of the search list is the expected movie title. We then get its description and synopsis using its IMDb id.

In [ ]:
import collections
compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
In [ ]:
for index, row in movie.iterrows():
    if row.text.strip() == '':
        title = row.title
        title = title.replace('(', '')
        title = title.replace(')', '')
        title = title.replace(',', '')
        ia = IMDb('http')
        m = ia.search_movie(row.title)
        if len(m) !=0:
            m = m[0]
            try:
                title_found = m['title']+ ' ' +str(m['year'])
                if compare(title.split(), title_found.split()):
                    m = ia.get_movie(m.movieID)
                    movie.loc[index, 'description'] = m.get('plot outline')
                    ia.update(m, 'synopsis')
                    movie.loc[index, 'synopsis'] = m.get('synopsis')
                    movie.loc[index, 'text'] = movie.loc[index, 'description'] + ' ' + movie.loc[index, 'synopsis']
            except:
                pass