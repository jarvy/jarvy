# ![jarvis](https://dl.dropboxusercontent.com/u/16169065/hal9000.jpg)
*Dave Bowman (inside EVA pod) trying to convince HAL to open the pod bay doors in “2001: A Space Odyssey” (1968).* 

<pre>Dave: Hello, HAL. Do you read me, HAL? 
HAL: Affirmative, Dave. I read you. 
Dave: Open the pod bay doors, HAL. 
HAL: I'm sorry, Dave. I'm afraid I can't do that. 
</pre>

Although there has been several attempts in making the machines intelligent, the early prototypes were still dumb. Until 2015. Then came Jarvis.

#### Introduction

Jarvis, aims to help humans by trying to understand them and figuring out best ways to respond to them. Jarvis is named after Tony Stark's artificially intelligent assistant in the Iron Man series. However, the inspiration is not restricted to the Iron Man series, but a huge line of books, movies and projects which led to this dream. A dream of living with artifical intelligence.

By design Jarvis does not aim harm, but this is software. Who knows, what could go wrong. I will make it straight. I accept no liability, if one day Jarvis or alike overthrow humans and rule the world.

#### Overview

Jarvis is written in Python. There is also a [Django interface](https://github.com/semihyagcioglu/advocatus) in the making, but you can use Jarvis standalone as a Python package.

The first prototype of Jarvis will be simple. Parse the query, gather information, evaluate findings and respond, that's all.

#### Goal

The goal is to have **a lot of fun**, and see where this goes. I want Jarvis to be **fully** customizable and extendible.

#### Installation

I am planning to make a setup, but for the time being you can install Jarvis via VCS.

<pre>
pip install git+git://github.com/jarvy/jarvis.git

or

pip install git+https://github.com/jarvy/jarvis.git

or without git

pip install —upgrade https://github.com/jarvy/jarvis/tarball/master
</pre>


#### Ideas

- Use google as source? We might need to rewrite the question. But when and how?
- Add wikipedia as knowledge base. Maybe simple english?
- Add Wolfram alpha as endpoint
- Cosine similarity. gensim might be a good idea.
- How about shallow parsing?
- Add CI and deployment to a production server for the web binding.
- How to score multiple sources, and rank them?
- Will probably need a database and an instantaneous search. Elasticsearch?
- Replace constant messages via redis?
- How about heroku?
- Better logging mechanism

#### Contribution

There are several ways to improve Jarvis. If you have **any** suggestions, please let me know. Or better, fork the repository, play with Jarvis and contribute by just sending a pull request. 

I **accept** pull requests.