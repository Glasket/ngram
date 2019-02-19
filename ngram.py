# Python 3.7.2 

import re
import argparse
import random

def generate_unigram_sentence():
    pass

def generate_unigram_table():
    pass

def generate_unigrams():
    pass

def generate_sentence(starts, standard, n):
    sentence = ''
    current_gram = ''
    rand = random.random()
    val_sum = 0
    for k,v in starts.items():
        val_sum += v
        if val_sum > rand:
            for token in k[1:]:
                if re.match(r'([\.\,\!\?\;\:\-\=\+\/\*\\]+)', token):
                    sentence += token
                else:
                    sentence += ' ' + token
            current_gram = k[1:]
            break
    while True:
        rand = random.random()
        val_sum = 0
        for k,v in standard.items():
            if k[:n-1] == current_gram:
                val_sum += v
                if v > rand:
                    if re.match(r'([\.\,\!\?\;\:\-\=\+\/\*\\]+)', k[n-1]):
                        sentence += k[n-1]
                    else:
                        sentence += ' ' + k[n-1]
                    current_gram = k[1:]
                    break
        if re.search(r'([\.\!\?]+)', sentence):
            break
    sentence = sentence.strip()
    sentence = sentence.capitalize()
    return sentence


def generate_ngram_tables(ngrams):
    """Generates relative frequency table for the n-gram"""
    ngram_tables = []
    for ngram in ngrams:
        ngram_table = dict()
        for sentence in ngram:
            for item in sentence:
                if item in ngram_table:
                    ngram_table[item] = ngram_table[item] + 1
                else:
                    ngram_table[item] = 1
        ngram_tables.append(ngram_table)
    for key, value in ngram_tables[0].items():
        w1 = tuple(w for w in key[:-1])
        ngram_tables[0][key] = value/ngram_tables[1].get(w1)
    return ngram_tables

def generate_ngrams(sentences, n):
    """Generates an n-gram for the given sentences"""
    ngram = []
    for i in range(0, 2):
        ngram.append([])
        for sentence in sentences:
            tokens = ['<start>'] + re.findall(r'[\w\']+|[\"\.\,\!\?\;\:\-\=\+\/\*\\]', sentence)
            if len(tokens) > n:
                ngram[i].append(zip(*[tokens[j:] for j in range(n-i)]))
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
    """Type definition for argparse"""
    value = int(val)
    if value <= 0:
        raise argparse.ArgumentTypeError('%s is not a positive value' % val)
    return value

def main():
    """Main Function"""
    # Defining arguments
    parser = argparse.ArgumentParser(description='Generates random sentences using an ngram model based on input files.')
    parser.add_argument('ngram', nargs=1, metavar='n', type=positive, 
                        help='an integer that represents the n-gram')
    parser.add_argument('output', nargs=1, metavar='m', type=int, 
                        help='an integer that represents the number of sentences to create (<= 0 is ignored)')
    parser.add_argument('input', nargs='+', 
                        help='list of files that will be processed for the n-gram model')
    args = parser.parse_args()

    if args.ngram[0] == 1: # Unigram
        # TODO Unique case for unigram
        pass
    else: # N-Gram greater than 1
        ngram_tables = generate_ngram_tables(generate_ngrams(get_sentences(
            read_files(args.input)), args.ngram[0]))
        starts = {k:v for k,v in ngram_tables[0].items() if '<start>' in k}
        start_sum = sum(starts.values())
        for k,v in starts.items():
            starts[k] = v/start_sum
        standard = {k:v for k,v in ngram_tables[0].items() if '<start>' not in k}

        for i in range(args.output[0]):
            print(generate_sentence(starts, standard, args.ngram[0]))

if __name__ == "__main__":
    main()
