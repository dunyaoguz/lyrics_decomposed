import pandas as pd
import numpy as np
import re
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def prepare_lexicon():
    ''' Prepare a dictionary of words and their associated emotions from the NRC Lexicon'''
    lexicon = pd.read_csv('sentiment_lexicons/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt', delim_whitespace=True, header=None)
    rs_lexicon = lexicon.pivot(index=0, columns=1, values=2)
    rs_lexicon.drop(rs_lexicon.index[0], axis=0, inplace=True)
    vocabulary = list(rs_lexicon.index)
    emotions = {}
    for word in vocabulary:
        rs_lex_filtered = rs_lexicon.loc[[word]]
        values = [col for col in rs_lex_filtered.columns if int(rs_lex_filtered[col].values) == 1]
        if values != []:
            emotions[word] = values
    return emotions

def prepare_corpus(df):
    ''' Prepare the corpus from the artists lyrics by tokenizing and lemmatizing the words'''
    corpus = []
    tokenizer = RegexpTokenizer(r'\w\w+')
    lemmatizer = WordNetLemmatizer()
    for lyric in df['lyrics']:
        token = tokenizer.tokenize(str(lyric).lower())
        lemmatized_token = []
        for word in token:
            lemmatized_word = lemmatizer.lemmatize(word)
            lemmatized_token.append(lemmatized_word)
        corpus.append(lemmatized_token)
    return corpus

def song_sentiments(corpus, emotions):
    '''Get the frequency of each sentiment in the artists songs'''
    song_emotions = []
    for song in corpus:
        emotion_count = {'anger': 0,
                         'positive': 0,
                         'negative': 0,
                         'anticipation': 0,
                         'disgust': 0,
                         'fear': 0,
                         'joy': 0,
                         'sadness': 0,
                         'surprise': 0,
                         'trust': 0}
        for word in song:
            if word in emotions.keys():
                word_emotions = emotions[word]
                for emotion in word_emotions:
                    emotion_count[emotion] += 1
        song_emotions.append(emotion_count)
    return song_emotions

def song_polarity(df):
    '''Calculate the combound polarity score of the lyric using the VADER lexicon'''
    analyser = SentimentIntensityAnalyzer()
    polarity = []
    for lyric in df['lyrics']:
        score = analyser.polarity_scores(str(lyric))
        polarity.append(score['compound'])
    df['polarity'] = polarity
    return df

if __name__ == '__main__':
    artists = pd.read_csv('data/list_of_artists.csv')
    emotions = prepare_lexicon()
    for artist in artists.name.tolist():
        df = pd.read_csv(f'data/{artist}.csv')
        df = df.drop(df[df.release_date == 'None'].index, axis=0)
        df = df.reset_index().drop('index', axis=1)
        corpus = prepare_corpus(df)
        sentiments = song_sentiments(corpus, emotions)
        df = song_polarity(df)
        df = df.join(pd.DataFrame(sentiments), how='left')
        df.to_csv(f'sentiment_data/{artist}.csv')
        print(f'Completed analysing {artist}.')
