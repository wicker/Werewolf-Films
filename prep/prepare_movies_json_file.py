import urllib.request
import config
import json

def get_from_omdb_api(imdb_ids):

  movies_json_file = 'movies.json'
  movies = []

  with open(movies_json_file, mode='w', encoding='utf-8') as f:
    json.dump([], f)  # init the file with an empty list

    count = 0
    for imdb_id in imdb_ids:

      omdb_request_url = 'http://www.omdbapi.com/?i=tt'+imdb_id+'&apikey='+config.OMDB_API_KEY
      with urllib.request.urlopen(omdb_request_url) as page:
        movie_item = json.loads(page.read().decode())
        count += 1
        print(count)
      movies.append(movie_item)

  with open(movies_json_file, mode='w', encoding='utf-8') as f:
    json.dump(movies, f)

def create_imdb_ids_list(ids_file):

  ids_list = []

  with open(ids_file,'r') as f:

    for line in f:
      line = line.replace('\n','')
      ids_list.append(line)

    ids_list_set = set(ids_list)
    
  return ids_list_set

imdb_ids_file = 'imdb-ids-list'
imdb_ids_list = create_imdb_ids_list(imdb_ids_file)

get_from_omdb_api(imdb_ids_list)


