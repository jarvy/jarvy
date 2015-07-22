# -*- coding: utf-8 -*-

import re
import random
from random import randint
import time
import logging
import os
import urllib2
from bs4 import BeautifulSoup

from packages.google import search

from actions import *
from settings import *

"""
Jarvy : Python Intelligent Assistant for Humans
=================

Jarvy, aims to help humans by trying to understand them and figuring out best ways to respond to them.

"""

__title__ = 'jarvy'
__version__ = '1.2.0'
__build__ = 0x012000
__author__ = 'Semih Yagcioglu'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015 Semih Yagcioglu'


class Jarvy:
    """ Jarvy : Python Intelligent Assistant for Humans
    """

    __LOG_LOCATION__ = "log/jarvy.log"

    def __init__(self):

        self.__setupLogger__()
        self.actions = Actions()
        self.settings = Settings()
        self.status = True

        self.wakeup()

    def __setupLogger__(self):

        self.logger = logging.getLogger('Jarvy')
        self.logger.setLevel(logging.INFO)

        # Log formatting
        formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Logfile handler
        directory = os.path.dirname(self.__LOG_LOCATION__)
        if not os.path.exists(directory):
            os.makedirs(directory)

        fh = logging.FileHandler(self.__LOG_LOCATION__)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def wakeup(self):

        welcome = self.hi()
        print '\n\n' + welcome + "."
        self.logger.info("Woke up.")

        while self.status:
            try:
                message = str(raw_input("What can I help you with?\n"))

                if message in self.settings.exit_messages:
                    self.sleep()
                else:
                    answer = self.answer(message)
                    print answer
            except KeyboardInterrupt:
                self.sleep()

    def sleep(self):

        farewell = self.farewell()
        print farewell
        self.status = False

        self.logger.info("Slept.")

    def hi(self):

        chance = random.uniform(0, 100)

        if chance <= 20:
            greeting = 'Hello'
        elif chance <= 40:
            greeting = 'Hi'
        else:
            hour = int(time.strftime('%H', time.localtime()))
            if 0 <= hour < 5:
                greeting = 'Good night'
            elif 5 <= hour < 12:
                greeting = 'Good morning'
            elif 12 <= hour < 17:
                greeting = 'Good afternoon'
            else:
                greeting = 'Good evening'

        return greeting

    def farewell(self):

        hour = int(time.strftime('%H', time.localtime()))
        if 0 <= hour < 5:
            farewell = 'Good night'
        elif 5 <= hour < 12:
            farewell = 'Have a good day'
        elif 12 <= hour < 17:
            farewell = 'See you again'
        else:
            farewell = 'Good night'

        return farewell

    def answer(self, message):

        action = self.understand(message)
        options = self.think(action, message)
        answer = self.explain(options, message)

        return answer

    def understand(self, message):

        if any(m in message for m in self.settings.personal_message_for_jarvy):    # it is something about the jarvy
            action = self.actions.about_jarvy
        elif message == self.settings.jarvy_name:
            action = self.actions.direct_address
        elif any(m in message for m in self.settings.personal_message_for_master):   # it is something about the master
            action = self.actions.about_master
        elif any(m in message for m in self.settings.rudimentary_question_tags):     # rewrite message as a search query
            action = self.actions.search_google
        else:
            action = self.actions.say_sorry
        return action

    def think(self, action, message):

        if action == self.actions.about_jarvy:
            options = self.get_options_for_personal_questions('jarvy', message)
        elif action == self.actions.direct_address:
            options = ['Yes ' + self.settings.master_formal_address]
        elif action == self.actions.about_master:
            options = self.get_options_for_personal_questions('master', message)
        elif action == self.actions.search_google:  # get results from google
            options = self.make_search(message, 'google')
        elif action == self.actions.search_wolfram:  # get results from wolfram
            options = self.make_search(message, 'wolfram')
        elif action == self.actions.search_wikipedia:  # get results from wikipedia
            options = self.make_search(message, 'wikipedia')
        else:
            rand = randint(0, len(self.settings.sorry_messages) - 1)
            options = [self.settings.sorry_messages[rand]]
        return options

    def make_search(self, query, source):

        query = self.rewrite_question(source, query)

        search_results = []
        trusted_results = []
        urls = search(query, stop=10)  # make a search

        for i, url in enumerate(urls):
            search_results.append(url)
            if url.find('wikipedia') > 0 and i < 3:  # trusted source, skip if not in the top 3
                trusted_results.append(url)
        try:

            if len(trusted_results) > 0:
                html = urllib2.urlopen(trusted_results[0]).read()
                soup = BeautifulSoup(html, 'html.parser')
                p = soup.find('div', id="bodyContent").p
                soup_p = BeautifulSoup(str(p), 'html.parser')
                text = soup_p.get_text()
            else:
                html = urllib2.urlopen(search_results[0]).read()
                soup = BeautifulSoup(html, 'html.parser')
                p = soup.find_all('p')
                soup_p = BeautifulSoup(str(p), 'html.parser')
                text = soup_p.get_text()
                pat = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)  # pattern to detect sentences
                matches = pat.findall(text)
                if len(matches) > 3:
                    text = ''.join(matches[0:3])
                else:
                    text = ''.join(matches[0:])
        except:
            text = ''

        options = [text]
        return options

    def explain(self, options, message):

        if len(options) >= 1:
            answer = options[0]
        else:
            rand = randint(0, len(self.settings.sorry_messages) - 1)
            answer = self.settings.sorry_messages[rand]
        return answer

    def get_options_for_personal_questions(self, person, message):

        if person == 'jarvy':
            options = ['Let\'s not talk about me.']
        elif person == 'master':
            options = ['You know, I can\'t answer that']
        else:
            options = ['']

        return options

    def rewrite_question(self, source, message):

        query = message  # by default, set it to message

        if source == 'google':
            for r in self.settings.rudimentary_question_tags:
                query = query.replace(r, '')

            query = query.replace('is', '')
            query = query.replace('are', '')
            query = query.strip()

        return query


def start():

    jarvyInstance = Jarvy()
    return jarvyInstance


def main(self):

    jarvy = Jarvy()
    return 0

if __name__ == '__main__':
    main(None)

