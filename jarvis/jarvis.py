import time

__author__ = 'semih'

import random
from random import randint
import logging
import os
from actions import *
from settings import *

class Jarvis:
    """ Core jarvis class
    """

    __LOG_LOCATION__ = "log/jarvis.log"

    def __init__(self):
        self.__setupLogger__()

        self.actions = Actions()
        self.settings = Settings()
        self.status = True

        self.wakeup()

    def __setupLogger__(self):

        self.logger = logging.getLogger('Jarvis')
        self.logger.setLevel(logging.DEBUG)

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
        print '\n\n' + welcome + ", what can I help you with?\n"
        self.logger.info("Woke up.")

        while self.status:
            try:
                message = str(raw_input(""))
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

        if any(m in message for m in self.settings.personal_message_for_jarvis):    # it is something about the jarvis
            action = self.actions.about_jarvis
        elif message == self.settings.jarvis_name:
            action = self.actions.direct_address
        elif any(m in message for m in self.settings.personal_message_for_master):   # it is something about the master
            action = self.actions.about_master
        elif any(m in message for m in self.settings.rudimentary_question_tags):     # we can rewrite the message as a search query
            action = self.actions.search_google
        else:
            action = self.actions.say_sorry
        return action

    def think(self, action, message):

        if action == self.actions.about_jarvis:
            options = self.get_options_for_personal_questions('jarvis', message)
        elif action == self.actions.direct_address:
            options = ['Yes ' + self.settings.master_formal_address]
        elif action == self.actions.about_master:
            options = self.get_options_for_personal_questions('master', message)
        elif action == self.actions.search_google:  # get results from google
            query = self.rewrite_question('google', message)
            options = self.research(query)
        elif action == self.actions.search_wolfram:  # get results from wolfram
            query = self.rewrite_question('wolfram', message)
            options = self.research(query)
        elif action == self.actions.search_wikipedia:  # get results from wikipedia
            query = self.rewrite_question('wikipedia', message)
            options = self.research(query)
        else:
            rand = randint(0, len(self.settings.sorry_messages) - 1)
            options = [self.settings.sorry_messages[rand]]
        return options

    def research(self, query):

        options = ['nothing yet...']
        return options

    def explain(self, options, message):

        if len(options) >= 1:
            answer = options[0]
        else:
            rand = randint(0, len(self.settings.sorry_messages) - 1)
            answer = self.settings.sorry_messages[rand]
        return answer

    def get_options_for_personal_questions(self, person, message):

        if person == 'jarvis':
            options = ['Let\'s not talk about me.']
        elif person == 'master':
            options = ['You know, I can\'t answer that']
        else:
            options = ['']

        return options

    def rewrite_question(self, source, message):

        query = message  # by default, set it to message

        if source == 'google':
            query = str(message).replace('', '')
        return query

def main(self):

    jarvis = Jarvis()
    return 0

if __name__ == '__main__':
    main(None)
