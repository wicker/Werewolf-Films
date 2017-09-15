import os,webbrowser
import urllib.request
import json

movies = []
movies_json_file = 'topthirteen.json'

index_head = """ <!DOCTYPE html>
<html lang="en">
<head>

  <meta charset="utf-8">
  <title>Werewolf Films</title>
  <meta name="description" content="An incomplete but giant list of werewolf films">
  <meta name="author" content="Jenner Hanni">

  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link rel="stylesheet" href="css/normalize.css">
  <link rel="stylesheet" href="css/skeleton.css">
  <link rel="stylesheet" href="css/custom.css">

</head>
<body>

  <div class="container">
    <div class="row">
      <div class="twelve columns">
        <h2>Werewolf Films</h2>
        <hr>
      </div>
    </div>"""

index_foot = """    <div class="row">
      <div class="twelve columns">
        <hr>
        <h4>Credits</h4>
        <ul>
          <li><a href="http://www.omdbapi.com/">OMDB API</a> for the movie information and posters</li>
          <li><a href="https://codepen.io/ibrahimjabbari/pen/ozinB">Ibrahim Jabbari</a> for the horizontal rule examples</a></li>
          <li><a href="http://clipart-library.com/">Clip Art Library</a> for the clipart wolf</li>
        </ul>
      </div>
    </div>
  </div>

</body>
</html>
"""

class Movie():

  def __init__(self,movie):

    self.title = movie['Title']
    self.year = movie['Year']
    self.plot = movie['Plot']
    self.poster = movie['Poster']
    self.trailer = movie['Trailer']

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

  #for m in movies:
    #m.print_movie_info()

  return movies

def create_html_page(movie_list):

  html_file = 'dist/index.html'

  with open(html_file, 'w') as f:
    f.write(index_head+'\n')
    count = 1

    for m in movie_list:
      if count in [1,4,7,10]:
        f.write('    <div class="row">\n')

      f.write('      <div class="four columns movie">\n')
      f.write('      <h3>'+m.title+'</h3>\n')
      f.write('      <div class="plot">('+m.year+')')
      f.write('      '+m.plot+'</div>')
      f.write('      <img src="img/'+m.poster+'">\n')
      f.write('      <a href="'+m.trailer+'"><div class="button button-primary">Trailer</div></a>\n')
      f.write('      </div>\n')
      count += 1

      if count in [4,7,10,13]:
        f.write('    </div><div style="clear:both;">&nbsp;</div>\n')

    f.write(index_foot)
  url = os.path.abspath(f.name)
  webbrowser.open('file://'+url,new=2)

movie_list = populate_movies_list_from_json()
create_html_page(movie_list)

