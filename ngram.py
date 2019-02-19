# Python 3.7.2 

import re
import sys
import argparse

def generate_ngrams(sentences, n):
    """Generates an n-gram for the given sentences"""
    ngram = []
    for i in range(0, n):
        ngram.append([])
    for i in range(n, 0, -1):
        for sentence in sentences:
            tokens = ['<start>'] + re.findall(r'[\w\']+|[\"\.\,\!\?\;\:\-\=\+\/\*\\]', sentence)
            if len(tokens) > n:
                ngram[i-1].append(zip(*[tokens[j:] for j in range(i)]))

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
            input_text += input_file.read().replace('\n', ' ') + ' '
    return input_text.lower()

def main():
    """Main Function"""
    # Defining arguments
    parser = argparse.ArgumentParser(description='Generates random sentences using an ngram model based on input files.')
    parser.add_argument('ngram', nargs=1, metavar='n', type=int, 
                        help='an integer that represents the n-gram')
    parser.add_argument('output', nargs=1, metavar='m', type=int, 
                        help='an integer that represents the number of sentences to create')
    parser.add_argument('input', nargs='+', 
                        help='list of files that will be processed for the n-gram model')
    args = parser.parse_args()

    ngrams = generate_ngrams(get_sentences(read_files(args.input)), args.ngram[0])

    ngram_table = dict()
    for ngram in ngrams:
        for sentence in ngram:
            for item in sentence:
                key = " ".join(item)
                if key in ngram_table:
                    ngram_table[key] = ngram_table[key] + 1
                else:
                    ngram_table[key] = 1
    print(ngram_table)

if __name__ == "__main__":
    main()
