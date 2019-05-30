import pandas as pd
import numpy as np
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
import gensim
from gensim.corpora import Dictionary
from gensim import corpora, models
from gensim.models.ldamodel import LdaModel

def prepare_corpus(df):
    '''Tokenize and lemmatize lyrics'''
    corpus = []
    s = stopwords.words('english')
    s.extend(['don', 'like', 'ain', 'oh', 'll', 'ooh', 'na', 'just', 've', 'tha', 'yeah', 'gon', 'gonna', 'every',
    'wanna', 'much', 'would', 'could', 'doin', 'ever', 'uh', 'uhh', 'huh', 'yeah', 'gotta', 'bout'])
    tokenizer = RegexpTokenizer(r'\w\w+')
    lemmatizer = WordNetLemmatizer()
    for lyric in df['lyrics']:
        token = tokenizer.tokenize(str(lyric).lower())
        lemmatized_token = []
        for word in token:
            if word not in s and len(word) > 3:
                lemmatized_word = lemmatizer.lemmatize(word)
                lemmatized_token.append(lemmatized_word)
        corpus.append(lemmatized_token)
    return corpus

def model_topic(artist):
    '''Extract predominant themes from a given artists' lyrics'''
    artist = artist.replace(' ', '')
    df = pd.read_csv(f'data/{artist}.csv')
    corpus = prepare_corpus(df)
    dictionary = Dictionary(corpus)
    dictionary.filter_extremes(no_below=10, no_above=0.75, keep_n=10000)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in corpus]
    tfidf = models.TfidfModel(doc_term_matrix)
    corpus_tfidf = tfidf[doc_term_matrix]
    lda_model = gensim.models.LdaMulticore(corpus_tfidf, num_topics=5, id2word=dictionary, passes=5, workers=4)
    topics = []
    for i, topic in lda_model.print_topics(-1):
        topics.append({'topic no': i+1, 'words': topic})
    topics = pd.DataFrame(topics)
    topics.to_csv(f'topics_data/{artist}.csv')
    return topics

def model_topic_year(df, year):
    '''Extract predominant themes from lyrics of a specific year'''
    corpus = prepare_corpus(df)
    dictionary = Dictionary(corpus)
    dictionary.filter_extremes(no_below=20, no_above=0.75, keep_n=200000)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in corpus]
    tfidf = models.TfidfModel(doc_term_matrix)
    corpus_tfidf = tfidf[doc_term_matrix]
    lda_model = gensim.models.LdaMulticore(corpus_tfidf, num_topics=3, id2word=dictionary, passes=5, workers=4)
    topics = []
    for i, topic in lda_model.print_topics(-1):
        topics.append({'topic no': i+1, 'words': topic})
    topics = pd.DataFrame(topics)
    return topics

def topics_per_year():
    df = pd.read_csv('sentiment_data/filtered_grand_df.csv')
    for year in df.release_year.unique().tolist():
        filtered_df = df[df.release_year == year]
        year_df = model_topic_year(filtered_df, year)
        year_df.to_csv(f'topics_data/{str(year)[0:4]}.csv')
        print(f'Completed {year}')

if __name__ == '__main__':
    artists = pd.read_csv(f'data/list_of_artists.csv')
    for artist in artists.name.tolist():
        topics = model_topic(artist)
        topics.to_csv(f'topics_data/{artist}.csv')
        print(f'Completed topic modelling for {artist}')
