# Werewolf-Films

This one-page website is dynamically generated by the Python module in [movies.py](https://github.com/wicker/Werewolf-Films/blob/master/movies.py) from the [toptwelve.json](https://github.com/wicker/Werewolf-Films/blob/master/toptwelve.json) file which contains the title, year of release, plot summary, poster art, and trailer link of my top twelve favorite werewolf films. 

### View the Site

The finished site is public at [jennerhanni.net/werewolf-films](http://jenenrhanni.net/werewolf-films/) and the source code is available in the [dist folder](https://github.com/wicker/Werewolf-Films/tree/master/dist).

### View the Site Locally

Fork and/or clone the repository to your local machine: 

```
git clone https://github.com/wicker/Werewolf-Films.git
```

Open your browser of choice and use its version of `File > Open` to view the page in `Werewolf-Films/dist/index.html`.

### Rebuild and View the Site Locally

Fork and/or clone the repository to your local machine and change directory:

```
git clone https://github.com/wicker/Werewolf-Films.git
cd Werewolf-Films
```

The site is serving static images locally from the `dist/img` folder and it uses the Skeleton files in `dist/css`. Running the following command will update the `dist/index.html` file and open a web browser to view the page. 

```
python movies.py
```

To change the list of movies, edit the `toptwelve.json` file and re-run that command.

The movies.py module looks for each JSON entry to have a Title, Year, Plot, Poster, and Trailer entry. The poster images are sourced from `dist/img/` but you can change the Poster string to be a web address so it will be served from the web. 
