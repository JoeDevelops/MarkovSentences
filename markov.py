from random import randint
import json
import re

class Markov():
    def __init__(self):
	# These characters mark the end of the sentence
        self.END_CHARS = ['.','!','?']

	# word_dict is the general dictionary for creating chains
        self.word_dict = {} 
	# starting_words is a list of words that come at the beginning of a sentence
        self.starting_words = []

    def build_dictionary(self):
        #bible is a .txt file containing an HTML bible.
        with open('bible','r') as bible:
            line_no = 0
            previous_word = None
            for line in bible:
                # Some lines in source file are not paragraph text.  Check for this
                # The d+:d+ format is used to remove verse numbers
		# The <p> tags are removed from the HTML format
                words = re.sub('<p>|</p>|[0-9]+:[0-9]+|<hr />','',line).split()
                
                for word in words:
		    # Update word_dict for new word
                    if word not in self.word_dict:
                        self.dict_update(str(word))

	   	    # If preceding word exists add word to word_dict follow set for that entry
                    if previous_word is not None:
                        self.add_to_follow_set(previous_word, word)
                    # Else word comes at beginning of a sentence.  Append it to follow set
                    else:
                        self.starting_words.append(word)

		    # If last character contains a terminal character, reset previous word.
                    if word[-1] in self.END_CHARS:
                        previous_word = None
                    else:
                        previous_word = word
                line_no += 1
            print('Dict. Built in {} lines.'.format(line_no))

    def dict_update(self, word):
        self.word_dict.update({word:[]})

    def add_to_follow_set(self, word, follow):
        self.word_dict[word].append(follow)

    def markov_sentence(self):
        markov = ""
	# Pick word from set of sentence starters
        word = self.starting_words[randint(0, len(self.starting_words)-1)]
        markov = markov + word
        while word[-1] not in self.END_CHARS:
	# Loop until we reach a word that ends in a terminal character      
            word = self.word_dict[word][randint(0,len(self.word_dict[word])-1)]
            markov = markov + " " + word
        return markov
 
    # Stores word_dict as a json string.  This is for use by the JoeDevelops Django app.
    def persist(self):
        with open('word_dict','w') as wd:
            word_dict=[self.starting_words, self.word_dict, self.END_CHARS]
            json.dump(word_dict, wd)

# Example program that outputs an example sentence
#	For this program to run, there must be an existing json dictionary in
#	the same format as above.
#
#	Consider taking a .txt argument from sys.argv so that somebody else can build
#	a dictionary by passing the program a file name in terminal.
if __name__ == '__main__':
    with open('word_dict', 'r') as wd:
        word_dict = json.load(wd)
        m = Markov()
        m.starting_words = word_dict[0]
        m.word_dict = word_dict[1]
        m.END_CHARS = word_dict[2]
        print(m.markov_sentence())


