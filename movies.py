import os,webbrowser
import urllib.request
import json

movies = []
movies_json_file = 'movies.json'

class Movie():

  def __init__(self,movie):

    print(movie['Title'])
    if movie['Title']:
      self.title = movie['Title']
    else:
      self.title = ''
    self.year = movie['Year']
    self.plot = movie['Plot']
    self.poster = movie['Poster']
    self.trailer = ''

  def print_movie_info(self):

    print(self.title+' ('+self.year+')')
    print(self.plot)
    print('')

def populate_movies_list_from_json():

  # open json, load first item
  with open(movies_json_file,'r') as f:
    movie_json = json.load(f)

  for entry in movie_json:
    m = Movie(entry)
    movies.append(m)

  for m in movies:
    m.print_movie_info()

  return movies

def create_html_page(movie_list):

  html_file = 'index.html'

  with open(html_file, 'w') as f:
    for m in movie_list:
      f.write(m.title+' ('+m.year+')<br />')
      f.write(m.plot+'<br /><br />')

  url = os.path.abspath(f.name)
  webbrowser.open('file://'+url,new=2)

movie_list = populate_movies_list_from_json()
create_html_page(movie_list)

