# Copyright 2015 Jason T Clark
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import urllib2
import json
import argparse
import hammock


class Config(object):
    """
    Class definition for Rotten Tomatoes API site config
    """
    BASE_URI = 'http://api.rottentomatoes.com/api/public/v1.0'

    API_ENDPOINTS = {
        'box_office': 'lists/movies/box_office.json',
        'lists': 'lists/movies.json',
        'in_theaters': 'lists/movies/in_theaters.json',
        'opening': 'lists/movies/opening.json',
    }

class Brandywine(object):
    """
    Class definition for Brandywine
    """
    API = hammock.Hammock(Config.BASE_URI)
    
    def __init__(self):
        """ Constructor """
        self.API_KEY = os.environ.get('ROTTEN_API_KEY')
    
    def return_api_key(self):
        return self.API_KEY
        
    def return_list_directory_json(self):
        """
        returns the URLs in JSON for the list directories
        """
        response = urllib2.urlopen(self.get_list_url())
        jsdata = json.load(response)
        return jsdata

    def fetch_box_office_titles(self):
        """
        returns json data about box office movies
        """
        #print Config.API_ENDPOINTS.box_office
        boxoffice = self.API(Config.API_ENDPOINTS['box_office']).GET(params={'apikey': self.API_KEY})
        print boxoffice.json()
        
    def fetch_in_theaters_titles(self):
        """
        returns json data about in theaters movies
        """
        intheaters = self.API.lists.movies('in_theaters.json').GET(params={'apikey': self.API_KEY})
        self.format_json_response(intheaters.json(), infotype='title')
    
    def fetch_opening_movies(self):
        """
        returns json data about current opening movies
        """
        opening = self.API.lists.movies('opening.json').GET(params={'apikey': self.API_KEY})
        self.format_json_response(opening.json(), infotype='title')
        
    def movie_search(self, title):
        """
        performs a search for movies by name
        """
        results = []
        jsdata = self.fetch_data(category='search', query=title)
        self.format_json_response(jsdata, infotype='score')

    def fetch_movie_data(self, movie_id):
        """
        returns all information about the requested movie
        """
        url = self.MOVIE_URL + '%s.json?apikey=%s' % (movie_id, str(self.key))

        return json.load(urllib2.urlopen(url))

    def fetch_data(self, **kwargs):
        """
        a better way to fetch the json data from rotten tomatoes api
        """
        for key in kwargs.keys():
            if kwargs['category'] == 'movies':
                url = self.BASE_URL + '%s.json?apikey=%s' % \
                ('movies', str(self.key))
            elif kwargs['category'] == 'search':
                url = self.SEARCH_URL + '%s.json?apikey=%s&q=%s' % \
                ('movies', str(self.key), kwargs['query'])
            elif kwargs['category'] == 'intheatres':
                print 'in theatres'
                url = self.SEARCH_URL + '%s.json?apikey=%s&q=%s' % \
                ('in_theatres', str(self.key))
            else:
                url = self.BASE_URL + 'movies/%s.json?apikey=%s' % \
                (kwargs['category'], str(self.key))

        return json.load(urllib2.urlopen(url))

    def format_json_response(self, response, infotype):
        """
        format the json response from the Rotten Tomatoes API call
        """
        if infotype == 'title':
            movies = []
            for movie in response['movies']:
                movies.append('==> ' + movie['title'] + \
                    ', ID: ' + str(movie['id']) + \
                    ', Rating: ' + str(movie['ratings']['critics_rating']) + \
                    ', Score: ' + str(movie['ratings']['critics_score']))

            # Removes unicode
            movie_titles = [title.encode('utf-8') for title in movies]
            for movie in movie_titles: print movie
        elif infotype == 'score':
            movies = []
            for movie in response['movies']:
                movies.append('==> ' + str(movie['title']) + ', Score: ' + \
                    str(movie['ratings']['critics_score']))
            for mov in movies:
                print mov
        else:
            for movie in response['movies']:
                for entry in movie:
                    print entry + ': ' + str(movie[entry])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rotten Tomatoes cli')
    parser.add_argument('-b', '--boxoffice', \
        action='store_true', help='lists current box office movies.')
    parser.add_argument('-t', '--intheaters', \
        action='store_true', help='lists movies currently in theaters.')
    parser.add_argument('-s', '--search', \
        metavar='movie', help='query the movie database')
    # TODO: Need to add subparsers for each argument
    args = parser.parse_args()
    brw = BrandyWine(vars(args))
