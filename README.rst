# ![jarvy](https://dl.dropboxusercontent.com/u/16169065/hal9000.jpg)
*Dave Bowman (inside EVA pod) trying to convince HAL to open the pod bay doors in “2001: A Space Odyssey” (1968).* 

<pre>Dave: Hello, HAL. Do you read me, HAL? 
HAL: Affirmative, Dave. I read you. 
Dave: Open the pod bay doors, HAL. 
HAL: I'm sorry, Dave. I'm afraid I can't do that. 
</pre>

Although there has been several attempts in making the machines intelligent, the early prototypes were still dumb. Until 2015. Then came Jarvy.

#### What is it?

Jarvy, aims to help humans by trying to understand them and figuring out best ways to respond to them. Jarvy is named after Tony Stark's 
artificially intelligent assistant in the Iron Man series. However, the inspiration is not restricted to the Iron Man series, but extends
 to a huge line of books, movies and projects which led to this dream. A dream of living with artificial intelligence.

By design Jarvy does not aim harm, but this is software. Who knows, what could go wrong. I will make it straight. I accept no liability, if one day Jarvy or alike overthrow humans and rule the world.

#### Why?

The goal is to have **a lot of fun**, and see where this goes. I want Jarvy to be **fully** customizable and expendable.

#### How?

.. code-block:: python

    > import jarvy
    > jarvy = Jarvy()
    ...

#### Usage

<pre>
> Jarvy
> Yes sir
> who is the director of ex machina?
> Ex Machina is a 2015 British science fiction thriller film written 
  and directed by Alex Garland, marking his directorial debut.
> who wrote iliad?
> Homer is best known as the author of the Iliad and the Odyssey.
</pre>

#### Installation

I am working on a setup, but for the time being you can install Jarvy via VCS.

<pre>
# install via git
$ pip install git+git://github.com/jarvy/jarvy.git

# install via git+https
$ pip install git+https://github.com/jarvy/jarvy.git

# install without git
$ pip install —upgrade https://github.com/jarvy/jarvy/tarball/master
</pre>

#### Contribution

There are several ways to improve Jarvy. If you have **any** suggestions, please let me know. Or better, fork the repository, play with Jarvy and contribute by just sending a pull request. 

I **accept** pull requests.

#### Roadmap

Jarvy is written in Python. There is also a [Django interface](https://github.com/semihyagcioglu/advocatus) in the making. The first 
prototype of Jarvy will be simple. Parse the query, gather information, evaluate findings and respond, that's all.

#### Ideas

- Need to write some unit tests, should use nose?
- Add Wolfram alpha as endpoint
- Integrate Travis CI for testing and deployment
- Add wikipedia as knowledge base. Maybe simple english?
- Cosine similarity. gensim might be a good idea.
- How about shallow parsing?
- A hook to production server for the web binding?
- How to score multiple sources, and rank them?
- Will probably need a database and an instantaneous search. Elasticsearch?
- How about using redis?
- How about heroku?
- Better logging mechanism
- How about using a cache mechanism?