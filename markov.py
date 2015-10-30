  GNU nano 2.2.6                                                                                                                                     File: joe_develops/markov.py                                                                                                                                                                                                                                                                       Modified  

from random import randint
import json
import re

class Markov():
    def __init__(self):
        self.END_CHARS = ['.','!','?']
#       self.NO_SPACE_CHARS = [',','.','!','?',':',';']  Used when prototyping with Python NLTK

        self.word_dict = {}
        self.starting_words = []

    def build_dictionary(self):
        with open('bible','r') as bible:
            for line in bible:
                #Eliminiates html tags as well as verse numbers
                words = re.sub('<.*?>|[0-9]+:[0-9]+','',line).split()
                previous_word = None
                for word in words:
                    if word not in self.word_dict:
                        self.dict_update(str(word))

                    if previous_word is not None:
                        self.add_to_follow_set(previous_word, word)
                    else:
                        self.starting_words.append(word)

                    if word[-1] in self.END_CHARS:
                        previous_word = None
                    else:
                        previous_word = word

    def dict_update(self, word):
        self.word_dict.update({word:[]})

    def add_to_follow_set(self, word, follow):
        self.word_dict[word].append(follow)

    def markov_sentence(self):
        try:
            markov = ""
            word = self.starting_words[randint(0, len(self.starting_words)-1)]
            markov = markov + word
            while word[-1] not in self.END_CHARS:
                word = self.word_dict[word][randint(0,len(self.word_dict[word])-1)]
                markov = markov + " " + word
        except:
            markov =  self.markov_sentence()
        return markov

    def persist(self):
    	# Persist for future use.
        with open('word_dict','w') as wd:
            word_dict=[self.starting_words, self.word_dict, self.END_CHARS]
            json.dump(word_dict, wd)
            
    def set_up(self):
    	with open('word_dict', 'r') as wd:
            dictionary = json.load(wd)
            self.starting_words = dictionary[0]
            self.word_dict = dictionary[1]
