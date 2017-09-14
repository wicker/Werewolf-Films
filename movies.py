import config
import urllib.request
import json

def get_omdb_api():

  movies_json_file = 'movies.json'
  imdb_ids = ['1266121','2140203']
  movies = []

  with open(movies_json_file, mode='w', encoding='utf-8') as f:
    json.dump([], f)  # init the file with an empty list

    for imdb_id in imdb_ids:

      omdb_request_url = 'http://www.omdbapi.com/?i=tt'+imdb_id+'&apikey='+config.OMDB_API_KEY
      with urllib.request.urlopen(omdb_request_url) as page:
        movie_item = json.loads(page.read().decode())
      movies.append(movie_item)

  with open(movies_json_file, mode='w', encoding='utf-8') as f:
    json.dump(movies, f)

def create_imdb_ids_list(ids_file):

  ids_list = []
  print(ids_file)

  with open(ids_file,'r') as f:

    for line in f:
      line = line.replace('\n','')
      ids_list.append(line)

    ids_list_set = set(ids_list)
    print(len(ids_list_set))
    
  #  for imdb_id in ids_list_set:
  #    print(imdb_id)

  return ids_list_set

imdb_ids_file = 'imdb-ids-list'
imdb_ids_list = create_imdb_ids_list(imdb_ids_file)

get_omdb_api()
