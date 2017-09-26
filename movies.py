import os, webbrowser, json

# The following JSON file should contain entries for the following:
# - Title
# - Year
# - Plot
# - Poster
# - Trailer

movies_json_file = 'toptwelve.json'

# The webpage will be composed of data from a dynamically generated movie list
# stored in 'movies' between the 'index_head' and 'index_foot' strings

movies = []

index_head = """ <!DOCTYPE html>
<html lang="en">
<head>

  <meta charset="utf-8">
  <title>My Favorite Werewolf Films</title>
  <meta name="description" content="My favorite werewolf films.">
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
        <h2>My Favorite Werewolf Films</h2>
        <hr>
      </div>
    </div>"""

index_foot = """      <div class="row">
        <div class="twelve columns"><hr></div>
      </div>
      <div class="row">
        <div class="two columns">&nbsp;</div>
        <div class="eight columns footer">
          <p>Built by <a href="http://jennerhanni.net/">Jenner Hanni</a> with 
          images from the <a href="http://clipart-library.com/">Clip Art 
          Library</a>,<br />poster art and movie info from the 
          <a href="http://www.omdbapi.com/">OMDB API</a>,<br />and horizontal 
          rule inspiration from 
          <a href="https://codepen.io/ibrahimjabbari/pen/ozinB">Ibrahim 
          Jabbari</a> on CodePen.</p>
      </div>
      <div class="two columns">&nbsp;</div>
    </div>
  </div>

</body>
</html>
"""

# Each movie from the JSON file will be an object of the Movie class

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


# Load the JSON and append each entry to the movies list 
def populate_movies_list_from_json():

  # open json, load first item
  with open(movies_json_file,'r') as f:
    movie_json = json.load(f)

  for entry in movie_json:
    m = Movie(entry)
    movies.append(m)

  # uncomment this to view the contents of the movies list
  #for m in movies:
    #m.print_movie_info()

  return movies

# Compose the page using the global variables for movies and the 
# webpage header and footer. Add extra spaces in f.write() as appropriate
# so the source of the HTML is readable.
def create_html_page(movie_list):

  html_file = 'dist/index.html'

  with open(html_file, 'w') as f:
    f.write(index_head+'\n')
    count = 1

    for m in movie_list:
      if count in [1,4,7,10]:
        f.write('    <div class="row clearfix">\n')

      f.write('      <div class="four columns movie">\n')
      f.write('      <h3>'+m.title+'</h3>\n')
      f.write('      <div class="plot">('+m.year+') ')
      f.write(m.plot+'</div>\n')
      f.write('      <img class="poster" src="img/'+m.poster)
      f.write('" alt="'+m.title+' poster">\n')
      f.write('      <a href="'+m.trailer+'">')
      f.write('<div class="button button-primary">')
      f.write('Trailer (YouTube)</div></a>\n')
      f.write('      </div>\n')
      count += 1

      # End the row after every third column entries 
      if count in [4,7,10,13]:
        f.write('    </div>\n')

    f.write(index_foot)

  # open the local page in the user's browser
  url = os.path.abspath(f.name)
  webbrowser.open('file://'+url,new=2)

# main
if __name__ == "__main__":

  movie_list = populate_movies_list_from_json()
  create_html_page(movie_list)

