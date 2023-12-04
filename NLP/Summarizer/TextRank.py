# Creating an Extractive Text Summarizer using TextRank Algorithm

import nltk
nltk.download('punkt')
nltk.download('stopwords')

import re # Regular Expression
import heapq # Heap Queue Algorithm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# load the text file
def read_text(file_name):
    with open(file_name, 'r') as f:
        file_data = f.read()
    # split the text into sentences
    text = file_data
    text = re.sub(r'\[[0-9]*\]', ' ', text) # remove numbers
    text = re.sub(r'\s+', ' ', text) # remove extra spaces
    clean_text = text.lower() # convert to lowercase
    regex_pattern = [r'\W',r'\d',r'\s+']
    for regex in regex_pattern:
        clean_text = re.sub(regex, ' ', clean_text) # remove special characters, digits, extra spaces

    return text, clean_text

def rank_sentences(text, clean_text):
    sentences = nltk.sent_tokenize(text) # split into sentences
    stop_words = nltk.corpus.stopwords.words('english')

    # create histogram of word frequency
    word_count = {}
    for word in nltk.word_tokenize(clean_text):
        if word not in stop_words:
            if word not in word_count.keys():
                word_count[word] = 1
            else:
                word_count[word] += 1

    sentence_score = {} # dictionary to store sentence score
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_count.keys():
                #only take sentences with less than 70 words
                if len(sentence.split(' ')) < 70:
                    if sentence not in sentence_score.keys():
                        sentence_score[sentence] = word_count[word]
                    else:
                        sentence_score[sentence] += word_count[word]
    
    return sentence_score

def generate_summary(file_name):
    text, clean_text = read_text(file_name)
    sentence_score = rank_sentences(text, clean_text)
    best_sentences = heapq.nlargest(5, sentence_score, key=sentence_score.get)

    summarized_text = []
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        if sentence in best_sentences:
            summarized_text.append(sentence)
    summarized_text = '\n'.join(summarized_text)
    return summarized_text

# function to find top 20 words
def plot_top_words(word_count_dict, show_top_n=20):
    word_count_table = pd.DataFrame.from_dict(word_count_dict, orient='index').rename(columns={0: 'score'})
    word_count_table = word_count_table.sort_values(by='score').tail(show_top_n).plot(kind='barh',figsize=(10,10))
    plt.show()


def main():
    file_name = input('1. Enter text file name: ')

    summary = generate_summary(file_name)
    # save smmary to txt file
    with open("summary.txt", 'w') as f:
        f.write(summary)
    f.close()

if __name__ == '__main__':
    main()