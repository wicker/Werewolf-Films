import os,webbrowser
import urllib.request
import json

class Movie():

  movies = []

  def __init__(self, movie):
    self.title = movie.title
    self.year = movie.year
    self.plot = movie.plot
    self.poster = movie.poster
    self.trailer = ''

  def create_html_page():

    html_file = 'index.html'

    with open(html_file, 'w') as f:
      f.write('Test')

    url = os.path.abspath(f.name)
    webbrowser.open('file://'+url,new=2)

print("Test")
