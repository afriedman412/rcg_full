<!-- <h2><a href="https://rcg-live.appspot.com/">RAP CAVIAR GENDER TRACKER</a></h2>  -->
<em>note: the app is temporarily offline while I get some hosting issues sorted out!</em>

Streaming music is the dominant form of music consumption in the modern era. Fans can listen to almost anything they want anywhere they have an internet connection (or not, given many platforms' options to download songs to stream while offline). The economics of this model are still in flux: another round of negotiations between labels and streaming services looms, and artists frequently vent about paltry payouts. But it seems unlikely that purchasing to download or physical media will take the power back any time in the near future.
<br>  

This isn't anything new, but an underappreciated aspect of streaming dominance is the extent to which playlists now fill the role which radio once did. While anyone can theoretically stream anything whenever, people don't actually want unlimited options. Music is as much about community and shared experiences as it is the art itself, and that means knowing what songs are coming out of people's cars, what tracks get rewinds from popular DJ's, etc. Popular playlists increasingly play a simlar role.   

Spotify's [RapCaviar](https://open.spotify.com/user/spotify/playlist/37i9dQZF1DX0XUsuxWHRQd?si=FhuE4m2IREWgQZ520vumvA) is one of these influential playlists. I don't have much non-anecdotal evidence to base that claim on, but at this moment it has 10.3 million followers. Spotify promotes it as a brand in and of itself, running billboards in the subways and live events. And while holding up popular songs on a playlist to show its influence is an extremely circular argument, RapCaviar does have its finger on the pulse of mainstream rap.   

Sort of.   

The problem is RapCaviar has a huge blind spot when it comes to women. We are in a golden era for women rapping. In no particular order, the likes of City Girls, Rico Nasty, CupCakke, Asian Doll, Cuban Doll, Molly Brazy, Saweetie, Princess Nokia, Stefflon Don and Tommy Genesis are all fixtures in the world of hip-hop. And that is not an exhaustive list. These are not fringe artists: they are popular, successful rappers by any modern metric, co-signed by big names. And yet the only women who ever seem to crack RapCaviar are Cardi B and Nicki Minaj, give or take a Rihanna and a Beyoncé. Which is not to knock any of those extremely talented women in their own right or to pit them against each other. It's just a notable trend: in the few weeks I have been working on this project, the playlist has featured somewhere between 60 and 70 male credits, while never clocking more than like 5 female credits.   

To the uninitiated, Spotify playlists are interally curated by highly-paid professionals. RapCaviar is a part of the music industry machinery. It's not the result of some highly calibrated algorithms: it's a collaboration between album release schedules, legitimate up-and-coming artists, and the whims of its authors. And that's fine. I'm not here to rail against small-timers squeezed out of the process. But while women have been an integral part of hip-hop since it began, it's hard to think of a time when this many female artists were legitimately holding their own. And while the rap community has always struggled to acknowledge the contributions of the women in its midst, the gap has never seemed so glaring.   

Thanks to [Ian Meyer](https://github.com/imeyer) for the help.
<br>

This is a [Django](https://www.djangoproject.com/) app written in Python, with the help of [this really rad Django tutorial](https://docs.djangoproject.com/en/2.1/intro/tutorial01/), deployed on the Google Cloud Flex App Engine with the help of [this really rad tutorial](https://codeburst.io/beginners-guide-to-deploying-a-django-postgresql-project-on-google-cloud-s-flexible-app-engine-e3357b601b91).  

It uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping, [Spotipy](https://spotipy.readthedocs.io/en/latest/) for accessing Spotify data, and [Unidecode](https://pypi.org/project/Unidecode/) for parsing stylized names.
