from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random

def word_cloud_generator(df, artist):
    cv = CountVectorizer(min_df=0, stop_words="english", max_features=200)
    counts = cv.fit_transform(df['lyrics'])
    words_freq = pd.DataFrame(counts.todense(), columns = cv.get_feature_names())
    words_dict = {}
    for word in words_freq.columns:
        words_dict[word] = words_freq[word].sum()
    stopwords = set(STOPWORDS)
    x, y = np.ogrid[:300, :300]
    mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)
    wc = WordCloud(max_words=200,
                   stopwords=stopwords,
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

artists = pd.read_csv('data/list_of_artists.csv')
for artist in artists.name.tolist():
    df = pd.read_csv(f'data/{artist}.csv')
    df = df.dropna()
    word_cloud_generator(df, artist)
