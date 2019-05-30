from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import random

def generate_word_cloud(artist):
    '''Creates a word cloud for the given artist and saves the file as png'''
    artist = artist.replace(' ', '')
    df = pd.read_csv(f'data/{artist}.csv')
    df = df.dropna()
    s = stopwords.words('english')
    s.extend(['don', 'like', 'ain', 'oh', 'll', 'ooh', 'na', 'just', 've', 'tha', 'yeah', 'gon', 'gonna', 'every',
    'wanna', 'much', 'would', 'could', 'doin', 'ever', 'uh', 'uhh', 'huh', 'yeah', 'gotta', 'bout', 'got', 'way'])
    cv = CountVectorizer(min_df=0, stop_words="english", max_features=200)
    counts = cv.fit_transform(df['lyrics'])
    words_freq = pd.DataFrame(counts.todense(), columns = cv.get_feature_names())
    words_dict = {}
    for word in words_freq.columns:
      if word not in s:
        words_dict[word] = words_freq[word].sum()
    x, y = np.ogrid[:300, :300]
    mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)
    wc = WordCloud(max_words=200,
                   scale=5,
                   height=300,
                   width=600,
                   max_font_size=80,
                   min_font_size=5,
                   relative_scaling=0,
                   colormap='gist_yarg',
                   mask=mask,
                   background_color='white').fit_words(words_dict)
    wc.to_file(f"static/images/word_clouds/{artist}.png")
    print(f'Created word cloud for {artist}')

def word_clouds_per_year():
    df = pd.read_csv('sentiment_data/filtered_grand_df.csv')
    for year in df.release_year.unique().tolist():
        filtered_df = df[df.release_year == year]
        year_df = generate_word_cloud(filtered_df, year)
        print(f'Completed {str(year)[0:4]}')

if __name__ == '__main__':
    artists = pd.read_csv('data/list_of_artists.csv')
    for artist in artists.name.tolist():
      word_cloud_generator(artist)
