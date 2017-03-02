import os
import sys
from random import choice
import twitter
api = twitter.Api(consumer_key= os.environ['TWITTER_CONSUMER_KEY'],
                  consumer_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'],
                  access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['TWITTER_CONSUMER_SECRET'])

chains = {}  # dictionary for all the texts going through

# print api.VerifyCredentials()
# {"id": 16133, "location": "Philadelphia", "name": "bear"}



def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.
    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    open_file = open(file_path)
    return open_file.read()


def make_chains(text_string, chains):
    """Takes input text as string; returns _dictionary_ of markov chains.
    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.
    For example:
        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    words = text_string.split()

    # Solution 2
    for index in range(0, len(words)-2):
        key = tuple([words[index], words[index+1]])
        chains.setdefault(key, []).append(words[index+2])
    chains.setdefault((words[-2], words[-1]), []).append(None)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    output_text = ""

    # made key list and then choise the first key random
    keys = chains.keys()
    new_key = choice(keys)

    # add the first tuple key to the output_text
    output_text = output_text + new_key[0] + " " + new_key[1]

    # from index 2 to end which is none, the code runs
    while True:
        random_value = choice(chains[new_key])
        if random_value is None:
            break
        output_text += " %s" % random_value
        new_key = tuple([new_key[1], random_value])

    return output_text


def combine_texts(argv):
    """Reads in arbitrary number of texts files and adds them to our dictionary."""

    # split the argv
    texts_to_add = sys.argv[1:]

    for text in texts_to_add:
        input_text = open_and_read_file(text)
        make_chains(input_text, chains)

def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    combine_texts(sys.argv)
    random_text = make_text(chains)
    tweet_text = random_text[:(140-16)]+" #changeTheRatio"
    status = api.PostUpdate(tweet_text)
    print status.text


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

# Your task is to write a new function tweet, that will take chains as input
# tweet(chains)
