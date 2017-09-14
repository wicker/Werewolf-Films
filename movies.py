import config
import urllib.request

def get_omdb_api():

  imdb_id = 'tt3896198'
  omdb_request_url = 'http://www.omdbapi.com/?i='+imdb_id+'&apikey='+config.OMDB_API_KEY
  print(omdb_request_url)
  t = urllib.request.urlopen(omdb_request_url).read()
  print(t) 

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
