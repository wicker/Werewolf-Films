# Werewolf-Films
Website collecting as many werewolf films as possible

## Step 1: Get the List of Movies

I'm on a quest to watch every werewolf film ever made, in any language, and I'd like to document it by creating a site to collect the list of movies in one place with my reviews. But where to get the data? 

I'm going to need the title, year of release, brief plot summary, the poster image, and a link to the trailer. I'm going to collect this data in a JSON file to use it on the webpage.

- RottenTomatoes (owned by Fandango) doesn't provide detailed movie metadata, posters, or images. 
- IMDB requires an AWS account
- Open Movie Database seems like the way to go. I paid $5 for one month of the Poster API.

Open Movie Database wants the exact title or IMDB ID number and then it will give me everything I need except for the trailer link. This may require being manually added later, but at least I can manually add it to my top ten.  

An OMDB API output returns: 

```
{"Title":"An American Werewolf in London","Year":"1981","Rated":"R","Released":"21 Aug 1981","Runtime":"97 min","Genre":"Comedy, Horror","Director":"John Landis","Writer":"John Landis","Actors":"Joe Belcher, David Naughton, Griffin Dunne, David Schofield","Plot":"Two American college students on a walking tour of Britain, are attacked by a werewolf, that none of the locals will admit exists.","Language":"English","Country":"UK, USA","Awards":"Won 1 Oscar. Another 2 wins & 3 nominations.","Poster":"https://images-na.ssl-images-amazon.com/images/M/MV5BZTk5NGQ0ZTktYWM2Yi00ZWQwLTg4NzItYzUxNjk1MDU5ODc5XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.6/10"},{"Source":"Rotten Tomatoes","Value":"89%"},{"Source":"Metacritic","Value":"60/100"}],"Metascore":"60","imdbRating":"7.6","imdbVotes":"71,463","imdbID":"tt0082010","Type":"movie","DVD":"09 Dec 1997","BoxOffice":"N/A","Production":"Universal Pictures","Website":"http://www.americanwerewolf.com","Response":"True"}
```

How many movies are we talking about? An IMDB Advanced Title search with "werewolf" in the plot summary and limited to `Documentaries/Feature Films/TV Movies/TV Specials/TV Mini-Series/Short Films/Videos` returned 389 hits. 

IMDB splits search results into pages of fifty results each; it seems like the easiest way to get the title and date is to copy and paste the list into a text document and modify it. The copy/paste gives me this format: 

```
Van Helsing
1. Van Helsing (2004)
6
RATE
An American Werewolf in London
2. An American Werewolf in London (1981)
7.6
RATE
The Monster Squad
3. The Monster Squad (1987)
7.2
RATE
Teen Wolf
4. Teen Wolf (1985)
6
RATE
```

There's an interesting ethical question here. 

IMDB's terms of use explicitly prohibit scraping but this isn't an automated crawl so I think I'm in the clear. I tried sorting by year or release date and realized a bunch of the films don't have dates. So I'm really just stuck with names.

Oh wait, that doesn't work. I need the IMDB ID.

I sorted by Alphabetical and saved each page to this folder. Then I ran the following command:

```
cat werewolf-search-results-* | grep http://www.imdb.com/title/tt > foo
```

Example output: 

```
Wolf Night <http://www.imdb.com/title/tt4806114/?ref_=adv_li_i>
378. Wolf Night <http://www.imdb.com/title/tt4806114/?ref_=adv_li_tt>
Wolf-in-law <http://www.imdb.com/title/tt6717208/?ref_=adv_li_i>
379. Wolf-in-law <http://www.imdb.com/title/tt6717208/?ref_=adv_li_tt>
```

So I need the string between `http://www.imdb.com/title/tt` and `/`. This calls for some regex... 

```
cat werewolf-search-results-* | grep -oP '(?<=imdb.com/title/tt).*(?=/)' > imdb_ids_list
```

Which gave me this in the imdb_ids_list file:

```
1266121
1266121
2315064
2315064
1979398
1979398
4531840
4531840
6769708
6769708
1478877
1478877
```

I can't assume there are two of each and it's time to read this into my Python program anyway, so we'll sort out the duplicates. Quickly, though, how many lines in the file? 

```
wc imdb-ids-list
 794  794 6352 imdb-ids-list
```

794 divided by two is 397, which is about nine more than the listed 389 in the "total search results" but it's good enough for now. 

That's the last we'll see of IMDB. 

## 2. Create a Sanitized List of IMDB IDs

I want to see if I can even use the OMDB API, so I'm going to read the `imdb-id-list` file into my Python program, create a list called `imdb_ids`, and clean it up so each ID only occurs once in the list.

A little parsing to remove '\n' from the line, and then I take the set of the list. The length is 390, which is off by one from the displayed search results. I wonder which one isn't displayed? 

A quick visual spot check seems to indicate all the IDs are valid:

```
imdb-ids-list
390
2140203
0118604
2106732
2315064
2308467
```

Here's the code:

```
def create_imdb_ids_list(ids_file):

  ids_list = []
  print(ids_file)

  with open(ids_file,'r') as f:

    for line in f:
      line = line.replace('\n','')
      ids_list.append(line)

    ids_list_set = set(ids_list)
    print(len(ids_list_set))

    for imdb_id in ids_list_set:
      print(imdb_id)

  return ids_list_set

imdb_ids_file = 'imdb-ids-list'
imdb_ids_list = create_imdb_ids_list(imdb_ids_file)
```

## 3. Query the OMDB API 

First order of business is to figure out how to hide my API key from the code, since I'll be pushing it to Github. I created a local config.py file that has my API key set to a variable. 

Then I add `config.py` to my .gitignore, added `import config` to my module, and used the `config.OMDB_API_KEY` variable throughout my module instead.

Now, to figure out how to actually do an API call. 

```
import config
import urllib.request

def get_omdb_api():

  imdb_id = 'tt3896198'
  omdb_request_url = 'http://www.omdbapi.com/?i='+imdb_id+'&apikey='+config.OMDB_API_KEY
  print(omdb_request_url)
  t = urllib.request.urlopen(omdb_request_url).read()
  print(t) 

get_omdb_api()
```

I worked out the string in the python console until it worked, then implemented it in the module. This code uses the hidden API key and an imdb_id to return the following:

```
http://www.omdbapi.com/?i=tt3896198&apikey=d407d12
b'{"Title":"Guardians of the Galaxy Vol. 2","Year":"2017","Rated":"PG-13","Released":"05 May 2017","Runtime":"136 min","Genre":"Action, Adventure, Sci-Fi","Director":"James Gunn","Writer":"James Gunn, Dan Abnett (based on the Marvel comics by), Andy Lanning (based on the Marvel comics by), Steve Englehart (Star-lord created by), Steve Gan (Star-lord created by), Jim Starlin (Gamora and Drax created by), Stan Lee (Groot created by), Larry Lieber (Groot created by), Jack Kirby (Groot created by), Bill Mantlo (Rocket Raccoon created by), Keith Giffen (Rocket Raccoon created by), Steve Gerber (character created by: Howard the Duck), Val Mayerik (character created by: Howard the Duck)","Actors":"Chris Pratt, Zoe Saldana, Dave Bautista, Vin Diesel","Plot":"The Guardians must fight to keep their newfound family together as they unravel the mystery of Peter Quill\'s true parentage.","Language":"English","Country":"USA, New Zealand, Canada","Awards":"4 wins & 10 nominations.","Poster":"https://images-na.ssl-images-amazon.com/images/M/MV5BMTg2MzI1MTg3OF5BMl5BanBnXkFtZTgwNTU3NDA2MTI@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.9/10"},{"Source":"Rotten Tomatoes","Value":"81%"},{"Source":"Metacritic","Value":"67/100"}],"Metascore":"67","imdbRating":"7.9","imdbVotes":"246,262","imdbID":"tt3896198","Type":"movie","DVD":"22 Aug 2017","BoxOffice":"$389,646,310","Production":"Walt Disney Pictures","Website":"https://marvel.com/guardians","Response":"True"}'
``` 

I've decided I want to create a movies.json file to store all of this. How do I get this in a JSON dump? StackOverflow [suggests you need a JSON list to start with](https://stackoverflow.com/questions/12994442/appending-data-to-a-json-file-in-python), so let's give that a shot.

The JSON needs to be decoded but otherwise, it's fairly straight-forward. I started with one ID, then tried it with iterating through a list of two IDs. 

```
import config
import urllib.request
import json

def get_omdb_api():

  movies_json_file = 'movies.json'
  imdb_ids = ['3896198','2140203']
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
```

I checked the output in movies.json in the [JSONLint Validator](https://jsonlint.com/) and it came up as Valid JSON, so we're in business.

```
[{"Title": "Wolvesbayne", "Country": "USA", "Runtime": "92 min", "Actors": "Mark Dacascos, Yancy Butler, Rhett Giles, Christy Carlson Romano", "Production": "Active Entertainment", "BoxOffice": "N/A", "imdbID": "tt1266121", "Website": "N/A", "Writer": "Leigh Scott", "Metascore": "N/A", "imdbRating": "3.8", "Type": "movie", "Poster": "https://images-na.ssl-images-amazon.com/images/M/MV5BMTM5ODg2ODYwOV5BMl5BanBnXkFtZTcwNTQ4MDQ4NA@@._V1_SX300.jpg", "Rated": "UNRATED", "Plot": "In 1887, the powerful vampire Lilith is vanquished by a vampire council and four amulets avoid her return to the world of living. In the present days, the greedy Realtor Russel Bayne is ...", "Language": "English", "Year": "2009", "Released": "12 Oct 2009", "DVD": "04 Jan 2011", "Genre": "Fantasy, Horror", "Response": "True", "imdbVotes": "920", "Ratings": [{"Value": "3.8/10", "Source": "Internet Movie Database"}], "Awards": "N/A", "Director": "Griff Furst"}, {"Title": "Wolf Children", "Country": "Japan", "Runtime": "117 min", "Actors": "Aoi Miyazaki, Takao Ohsawa, Haru Kuroki, Yukito Nishii", "Production": "N/A", "BoxOffice": "N/A", "imdbID": "tt2140203", "Website": "N/A", "Writer": "Mamoru Hosoda (story), Mamoru Hosoda (screenplay), Satoko Okudera (screenplay)", "Metascore": "71", "imdbRating": "8.2", "Type": "movie", "Poster": "https://images-na.ssl-images-amazon.com/images/M/MV5BMTUzNTUzMTA5OF5BMl5BanBnXkFtZTgwOTg0ODc1MTE@._V1_SX300.jpg", "Rated": "PG", "Plot": "After her werewolf lover unexpectedly dies, a young college student must move to another location to raise their also wolf son and daughter.", "Language": "Japanese", "Year": "2012", "Released": "21 Jul 2012", "DVD": "26 Nov 2013", "Genre": "Animation, Drama, Family", "Response": "True", "imdbVotes": "23,662", "Ratings": [{"Value": "8.2/10", "Source": "Internet Movie Database"}, {"Value": "94%", "Source": "Rotten Tomatoes"}, {"Value": "71/100", "Source": "Metacritic"}], "Awards": "19 wins & 6 nominations.", "Director": "Mamoru Hosoda"}]
```

## 4. Output the Bare Bones Webpage

Before wasting a pile of API calls, I want to be sure I can create a webpage with these two films from the JSON I have so far. I made a couple tiny tweaks to the provided sample code, mostly adding 'with open' so I don't have to remember to explicitly close the file when I'm done with it, and now I get a webpage with the word 'Test'.

## 6. Refactor into Two Python Files

It's pretty clear at this point that when a user runs the movies.py file, they should be starting with a complete and prepared movies.json file. There shouldn't be any further API calls once that movies.json file is ready to go. 

I created a new file called `prepare_movies_json_file.py` that will take care of 

1. Cleaning the IMDB IDs list
1. Getting the JSON data from the OMDB API
1. Building the movies.json file

## 5. Creating the Movie Class

The Movie() class will have the following class variables to start with:

- title
- year
- plot
- poster
- trailer

It will fill these variables from the movies.json file. 

```
class Movie():

  def __init__(self,movie):

    self.title = movie['Title']
    self.year = movie['Year']
    self.plot = movie['Plot']
    self.poster = movie['Poster']
    self.trailer = ''

  def print_movie_info(self):

    print(self.title+' ('+self.year+')')
    print(self.plot)
    print('')
```

I ended up with 337 usable movies after the API calls to the Open Movie Database. I took those and wrote them out to the `index.html` file. 

## 6. Serving the Site

I want to use grids and I've worked with the super lightweight [Skeleton CSS Grid Framework](http://getskeleton.com/) before, but I also want to serve the site on Github without having to constantly switch back and forth between the `master` and `gh-pages` branches. 

I found [instructions from cobyism](https://gist.github.com/cobyism/4730490) on how to serve it from a `dist` folder on the `master` branch, so I put the index.html and my Skeleton CSS files in that dist folder, removed the folder from `.gitignore` and pushed.

To push to `gh-pages` in the future:

```
git add dist && git commit -m "Put Commit Here"
git subtree push --prefix dist origin gh-pages
```

Then I realized my main site is jennerhanni.net, but my repo has capital letters so the full address would be `http://jennerhanni.net/Werewolf-Films/` and I don't like that. I did this before on another project: you can go into the `wicker.github.io` repo that serves `jennerhanni.net` and add a folder called `werewolf-films` that includes an HTML file called `index.html` that redirects to `Werewolf-Films`.

```
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="refresh" content="0; url=/Werewolf-Films/" />
  </head>
</html>
```

And voila, `http://jennerhanni.net/werewolf-films/` redirects to my Werewolf-Films site.

## 7. Revisit the Project Requirements

First, I went back to the Udacity project page to figure out my basic requirements so I can submit for this project. I'll be adding all the films and everything later, once I figure out how that works, but for now I'm going to serve the top ten werewolf films. I suspect my favorite (Brotherhood of the Wolf) might not even be on the list, since it's not *technically* a werewolf film, even though it totally is. 

I've definitely created a data structure to store the favorite movies. To make the site one page, I made a smaller JSON file just containing a few movies that I saw and either liked or were so terrible I loved them despite themselves. I hand-populated the JSON file `topthirteen.json` for these films:

  - American Werewolf in London
  - Romasanta: The Werewolf Hunt
  - When Animals Dream
  - Ginger Snaps
  - What We Do in the Shadows
  - Wilderness
  - Brotherhood of the Wolf
  - Dog Soldiers
  - The Howling
  - The Wolf Man
  - Wolfen
  - The Wolfman
  - Harry Potter and the Prisoner of Azkaban

My Python script loads these in from the JSON, decodes them, and creates a list of objects instantiated from the class Movie().

I ended up saving the posters locally, since I'd like the  think are coming right from IMDB. Not sure on the legality, but at the moment I expect it's under fair use since it's a recommendation site. Things to think about... 

I created a directory called `posters` in the `img` folder in `dist` so they're all now local. This may or may not be the right answer. 

## 8. Style the Page using Skeleton CSS

I ended up with an unhelpful number of movies at thirteen... not divisible by two, three, or four. I ideally want some sort of grid with cards showing the movie poster and the relevant movie information.

I styled things to have a grid of three rows by four cards. I removed one of the movies from the list, so it would be even. 

I created strings for the static html above and below the movie listings, then iterated through using a count variable to determine when to start and end rows and columns. 

## Thoughts


This would have been a different process if this needed to be an app that automatically updated when new werewolf films come out. 
