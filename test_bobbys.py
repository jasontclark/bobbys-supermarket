#!/usr/bin/env python
# -*- coding: utf8 -*-
#
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
""" test_bobbys.py - Tests for bobbys """
import os
import sys
import unittest

# This needs to be tweaked. The full path here will not work on all systems.
sys.path.insert(0, '/Users/jclark/Code/Repos/git/github/bobbys/bobbys')

from bobbys import bobbys
from bobbys import Config

class Testbobbys(unittest.TestCase):
    """ Test bobbys class."""
    def setUp(self):
        self.bobbys = bobbys()

    def tearDown(self):
        #self.bobbys.dispose()
        self.bobbys = None

    def test_api_key(self):
        """ Test if the API key is set. """
        self.assertIsNotNone(self.bobbys.return_api_key())

    def test_fetch_box_office_titles(self):
        self.assertIn(self.bobbys.fetch_box_office_titles(), 'movies')

    #def test_fetch_in_theaters_titles(self):
    #    self.assertTrue('movies' in self.bobbys.fetch_in_theaters_titles())

if __name__ == '__main__':
    unittest.main()

# create the bobbys object
#brw = bobbys(os.environ.get('ROTTEN_API_KEY'))

# fetch box office titles
#print 'Box Office Titles: '
#boxOfficeTitles = brw.fetch_box_office_titles()
#for title in boxOfficeTitles:
#  print title

#print '\n'

# fetch in theatres titles
#print 'In Theaters Titles: '
#inTheatersTitles = brw.fetch_intheaters_titles()
#for title in inTheatersTitles:
#  print title

#brw.fetch_movie_data('771317257')

# return the list directory json
#jsonlist = brw.return_list_directory_json()
#print jsonlist

#movieslist = brw.return_movies_list_json()

#for movie in movieslist['movies']:
#    print movie['title']
