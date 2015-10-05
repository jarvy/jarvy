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
__version__ = '1.3.0'
__build__ = 0x010300  # in the format of 00-00-00
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
        # ch = logging.StreamHandler()
        # ch.setFormatter(formatter)
        # self.logger.addHandler(ch)

        # Logfile handler
        directory = os.path.dirname(self.__LOG_LOCATION__)
        if not os.path.exists(directory):
            os.makedirs(directory)

        fh = logging.FileHandler(self.__LOG_LOCATION__)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    # starts jarvy
    def wakeup(self):

        welcome = self.hi()
        print '\n\n' + welcome + "."
        self.logger.info("Woke up.")

        while self.status:
            try:
                message = str(raw_input("What can I help you with?\n\n")).lower()

                if any(m in message for m in self.settings.farewell_messages) and any(m in message for m in self.settings.jarvy_name):
                    self.sleep()
                else:
                    answer = self.answer(message)
                    print answer
            except KeyboardInterrupt:
                self.sleep()

    # terminates jarvy
    def sleep(self):

        farewell = self.farewell()
        print farewell
        self.status = False

        self.logger.info("Slept.")

    # produce salutation message
    def hi(self):

        chance = random.uniform(0, 100)

        if chance <= 20:
            greeting = 'Hello ' + self.settings.master_name
        elif chance <= 30:
            greeting = 'Hi ' + self.settings.master_name
        elif chance <= 40:
            greeting = 'Hey'
        else:
            hour = int(time.strftime('%H', time.localtime()))
            if 0 <= hour < 5:
                greeting = 'Good night ' + self.settings.master_formal_address
            elif 5 <= hour < 12:
                greeting = 'Good morning ' + self.settings.master_formal_address
            elif 12 <= hour < 17:
                greeting = 'Good afternoon ' + self.settings.master_formal_address
            else:
                greeting = 'Good evening ' + self.settings.master_formal_address

        return greeting

    # produce farewell message
    def farewell(self):

        chance = random.uniform(0, 100)

        if chance <= 20:
            farewell = 'Good bye ' + self.settings.master_name
        elif chance <= 40:
            farewell = 'Farewell my friend'
        else:
            hour = int(time.strftime('%H', time.localtime()))
            if 0 <= hour < 5:
                farewell = 'Good night ' + self.settings.master_formal_address
            elif 5 <= hour < 12:
                farewell = 'Have a good day ' + self.settings.master_formal_address
            elif 12 <= hour < 17:
                farewell = 'Good afternoon ' + self.settings.master_formal_address
            else:
                farewell = 'Good evening ' + self.settings.master_formal_address

        return farewell

    # respond to the query message
    def answer(self, message):

        action = self.understand(message)
        responses = self.think(action, message)
        answer = self.explain(responses)

        return answer

    def understand(self, message):

        if any(m in message.split() for m in self.settings.personal_message_for_jarvy):    # it is something about the jarvy
            action = self.actions.about_jarvy
        elif message == self.settings.jarvy_name.lower():  # direct address to jarvy
            action = self.actions.direct_address
        elif any(m.lower() in message.split() for m in self.settings.personal_message_for_master):   # it is something about the master
            action = self.actions.about_master
        elif any(m.lower() in message.split() for m in self.settings.rudimentary_question_tags):     # rewrite message as a search query
            action = self.actions.search_google
        else:
            action = self.actions.say_sorry
        return action

    def think(self, action, message):

        if action == self.actions.about_jarvy:
            responses = self.respond('jarvy')
        elif action == self.actions.direct_address:
            responses = self.respond('direct_address')
        elif action == self.actions.about_master:
            responses = self.respond('master')
        elif action == self.actions.search_google:  # get results from google
            responses = self.make_search(message, 'google')
        elif action == self.actions.search_wolfram:  # get results from wolfram
            responses = self.make_search(message, 'wolfram')
        elif action == self.actions.search_wikipedia:  # get results from wikipedia
            responses = self.make_search(message, 'wikipedia')
        else:
            responses = []

        if not responses:
            rand = randint(0, len(self.settings.sorry_messages) - 1)
            responses = [self.settings.sorry_messages[rand]]

        return responses

    def make_search(self, query, source):

        query = self.rewrite_question(source, query)

        search_results = []
        trusted_results = []

        try:
            urls = search(query, stop=self.settings.number_of_search_results)  # make a search

            for i, url in enumerate(urls):
                search_results.append(url)
                if url.find('wikipedia') > 0 and i < self.settings.trusted_source_treshold:  # trusted source, skip if not in there
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

                    if len(matches) > self.settings.number_of_minimum_sentences:
                        text = ''.join(matches[0:self.settings.number_of_minimum_sentences])
                    else:
                        text = ''.join(matches[0:])  # TODO: what if the answer is = ''

                responses = [text]
            except:
                responses = []  # there is no proper response, but need to reconsider this
        except:
            responses = []  # no internet access

        return responses

    def explain(self, responses):

        if len(responses) >= 1:  # if there is only one response
            answer = responses[0]
        else:
            pass  # TODO: scoring might be done here!

        return answer

    def respond(self, about):

        if about == 'jarvy':
            responses = ['I am your friend.']
        elif about == 'direct_address':
            responses = ['Yes ' + self.settings.master_formal_address]
        elif about == 'master':
            responses = ['I\'m afraid, I can\'t answer that.']
        else:
            responses = ['']

        return responses

    def rewrite_question(self, source, message):

        query = message  # by default, set it to message

        if source == 'google':
            for r in self.settings.rudimentary_question_tags:
                query = query.replace(r, '')

            query = query.replace(' is ', ' ')
            query = query.replace(' are ', ' ')
            query = query.strip()

        return query


def start():

    j = Jarvy()
    return j

if __name__ == '__main__':
    start()

