# Python 3.7.2
#
# Christian W Sigmon
# 2/19/2019 CMSC-416
#
# Problem: Sentences must be created from source texts using a model created based on clusters
#          of text that makeup sentences.
#
# Example:
# python ngram.py 3 3 1399.txt 2554-0.txt 2600-0.txt
# Generates random sentences based on a specified n-gram model and input files. Christian W. Sigmon CMSC-416
# Command Line Settings: ngram.py 3 3
# Soon after the conversation.
# Meaning when did you come?
# Easter came in to see her, and she was not a word to say, and that the husband and wife.
#
# Algorithm: Files are parsed, sentences are then generated from the input text. These sentences
#            are then tokenized and turned into n-grams. The n-grams and (n-1)-grams are then used
#            to create a n-gram table which provides probabilities that can be used to generate sentences
#

import re
import argparse
import random
import sys

def generate_unigram_sentence(word_list):
    """Generates a sentence using the unigram frequency table"""
    sentence = ''
    while True:
        rand = random.random()
        val_sum = 0
        for k, v in word_list.items():
            val_sum += v       # Words value is added to val_sum
            if val_sum > rand: # First word to surpass the random value is used
                if re.match(r'([\.\,\!\?\;\:\=\+\/\*\\]+)', k): # Prevent punct. spacing
                    sentence += k
                else:
                    sentence += ' ' + k
                break
        if re.search(r'([\.\!\?]+)', sentence): # Sentence is complete once it has proper punct.
            break
    sentence = sentence.strip()      # Strip whitespace for cleanliness
    sentence = sentence.capitalize() # Capitalize first letter
    return sentence

def generate_sentence(starts, standard, n):
    """Generates a sentence using a start-word list, a standard-word list, and the n-gram model"""
    sentence = ''
    current_gram = ''
    rand = random.random()
    val_sum = 0
    for k, v in starts.items():
        val_sum += v            # Key value is added to sum for checking if the key should be used
        if val_sum > rand:      # If value sum passes the random value, then the current key is used
            for token in k[1:]: # k[1:] used to ignore <start> token
                if re.match(r'([\.\,\!\?\;\:\=\+\/\*\\]+)', token): # Used to prevent punct. spacing
                    sentence += token
                else:
                    sentence += ' ' + token
            current_gram = k[1:] # Current gram is stored for lookup later
            break
    while True:
        rand = random.random()
        val_sum = 0
        for k, v in standard.items():
            if k[:n-1] == current_gram: # Matches the gram pattern to ensure correct chaining
                val_sum += v
                if v > rand:
                    if re.match(r'([\.\,\!\?\;\:\=\+\/\*\\]+)', k[n-1]):
                        sentence += k[n-1]
                    else:
                        sentence += ' ' + k[n-1]
                    current_gram = k[1:]
                    break
        if re.search(r'([\.\!\?]+)', sentence): # Once the sentence contains punctuation, it is done
            break
    sentence = sentence.strip()      # Strip whitespace for cleanliness
    sentence = sentence.capitalize() # Capitalizes first letter
    return sentence

def generate_unigram_table(ngram):
    """Generates a frequency table for a unigram model"""
    ngram_table = dict()
    for token in ngram:
        if token in ngram_table: # If token is already present, add one to value
            ngram_table[token] = ngram_table[token] + 1
        else:
            ngram_table[token] = 1        # Add token if not present
    ngram_sum = sum(ngram_table.values()) # Sums the total occurrences of all tokens
    for k, v in ngram_table.items():
        ngram_table[k] = v/ngram_sum      # Changes frequency to probability
    return ngram_table

def generate_ngram_tables(ngrams):
    """Generates relative frequency table for the n-gram"""
    ngram_tables = []
    for ngram in ngrams:
        ngram_table = dict()
        for sentence in ngram:
            for token in sentence:
                if token in ngram_table: # If token is already present, add one to value
                    ngram_table[token] = ngram_table[token] + 1
                else:
                    ngram_table[token] = 1 # Add token if not present
        ngram_tables.append(ngram_table)
    for key, value in ngram_tables[0].items():
        w1 = tuple(w for w in key[:-1]) # Gets the w1 value of the ngram
        # Use the frequency of w1 to get relative frequency
        ngram_tables[0][key] = value/ngram_tables[1].get(w1) 
    return ngram_tables

def generate_unigrams(sentences):
    """Generates the ngrams for a unigram model"""
    ngram = []
    for sentence in sentences:
        # Captures words (incl. contractions) and punctuation as tokens
        tokens = re.findall(r'[\w\']+|[\.\,\!\?\;\:\=\+\/\*\\]', sentence)
        if len(tokens) > 1: # Ignores single word sentences
            ngram += tokens
    return ngram

def generate_ngrams(sentences, n):
    """Generates n-grams for the given sentences"""
    ngram = []
    for i in range(0, 2): # Generates 2 n-grams (N-gram and (N-1)-Gram)
        ngram.append([])
        for sentence in sentences:
            # Captures words and punctuation as tokens, alongside generating <start> token
            tokens = ['<start>'] + re.findall(r'[\w\']+|[\.\,\!\?\;\:\=\+\/\*\\]', sentence)
            if len(tokens) > n:
                ngram[i].append(zip(*[tokens[j:] for j in range(n-i)])) # Packages n-grams as tuples
    return ngram

def get_sentences(input_text):
    """Splits the input into sentences based on punctuation"""
    sentences = []
    tokens = re.split(r'([\.\!\?]+)', input_text)       # Splits on and captures punctuation marks
    for i, token in enumerate(tokens):
        if i > 0 and re.match(r'([\.\!\?]+)', token):   # For each token, check if it is punctuation
            sentences.append(tokens[i-1] + tokens[i])   # Create full sentence and add to sentences
    return sentences

def read_files(inputs):
    """Parses the input files and returns a single large input string for later processing"""
    input_text = ''
    for input_ in inputs:
        with open(input_, 'r') as input_file:
            input_text += input_file.read().replace('\n', ' ').replace('"', '').replace('-', '') + ' '
    return input_text.lower()

def positive(val):
    """Type definition for argparse that guarantees positive inputs"""
    value = int(val)
    if value <= 0:
        raise argparse.ArgumentTypeError('%s is not a positive value' % val)
    return value

def main():
    """Main Function"""
    # Defining arguments for CLI
    parser = argparse.ArgumentParser(description='Generates random sentences using an n-gram model based on input files.')
    parser.add_argument('ngram', nargs=1, metavar='n', type=positive, 
                        help='a positive integer that represents the n-gram')
    parser.add_argument('output', nargs=1, metavar='m', type=positive, 
                        help='a positive integer that represents the number of sentences to create')
    parser.add_argument('input', nargs='+', 
                        help='list of files that will be processed for the n-gram model')
    args = parser.parse_args()

    # Print Details
    print('Generates random sentences based on a specified n-gram model and input files.' +
          ' Christian W. Sigmon CMSC-416')
    print('Command Line Settings: ' + sys.argv[0] + ' ' + str(args.ngram[0]) + ' ' + str(args.output[0]))

    # N-Gram code
    if args.ngram[0] == 1: # Unigram
        # Reads in files, gets the sentences, generates grams, and generates the table.
        ngram_table = generate_unigram_table(generate_unigrams(get_sentences(
            read_files(args.input))))
        for i in range(args.output[0]): # Print as many sentences as requested
            print(generate_unigram_sentence(ngram_table))
    else: # N-Gram greater than 1
        ngram_tables = generate_ngram_tables(generate_ngrams(get_sentences(
            read_files(args.input)), args.ngram[0]))
        # Separate the 'starts' from the regular grams
        starts = {k:v for k,v in ngram_tables[0].items() if '<start>' in k}
        start_sum = sum(starts.values())
        for k, v in starts.items():
            starts[k] = v/start_sum # Average the start frequency in order to keep the sum ~1
        # Remove starts from regular grams
        standard = {k:v for k, v in ngram_tables[0].items() if '<start>' not in k}

        for i in range(args.output[0]): # Print sentences for ngram model > 1
            print(generate_sentence(starts, standard, args.ngram[0]))

if __name__ == "__main__":
    main()
