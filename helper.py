import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import random
from sklearn.decomposition import PCA

def read_data(df):
    '''Prepare the data for the sentiment plot'''
    df_normalized = df.groupby('release_date')[['anger', 'positive', 'negative', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']].sum()
    sums = df_normalized['anger'] + df_normalized['positive'] + df_normalized['negative'] + df_normalized['anticipation'] + df_normalized['disgust'] + df_normalized['fear'] + df_normalized['joy'] + df_normalized['sadness'] + df_normalized['surprise'] + df_normalized['trust']
    df_normalized['sum'] = sums
    for col in df_normalized.columns:
        df_normalized[col] = df_normalized[col].apply(int)
    df_normalized.index = pd.to_datetime(df_normalized.index, errors='coerce')
    df_normalized = df_normalized.resample('Y').sum()
    cols = list(df_normalized.columns)
    zeros = (df_normalized.anger == 0) & (df_normalized.positive == 0) & (df_normalized.negative == 0) & (df_normalized.anticipation == 0) & (df_normalized.disgust == 0) & (df_normalized.fear == 0) & (df_normalized.joy == 0) & (df_normalized.sadness == 0) & (df_normalized.surprise == 0) & (df_normalized.trust == 0)
    df_normalized.drop(df_normalized[zeros].index, axis=0, inplace=True)
    df_normalized = df_normalized.reset_index()
    cols.remove('sum')
    for col in cols:
        df_normalized[col] = df_normalized[col] / df_normalized['sum']
    df_normalized['release_year'] = df_normalized['release_date'].dt.year
    return df_normalized

def cluster_data(df):
    '''Cluster songs based on their sentiments'''
    pca = PCA(n_components=2)
    pca = pca.fit_transform(df[['anger', 'anticipation', 'disgust', 'fear', 'joy', 'surprise', 'trust', 'positive', 'negative']])
    pca = pd.DataFrame(pca, columns = ['Component1', 'Component2'])
    KMeans_3 = KMeans(n_clusters=3)
    KMeans_3.fit(pca)
    pca['cluster_3'] = KMeans_3.labels_
    KMeans_4 = KMeans(n_clusters=4)
    KMeans_4.fit(pca)
    pca['cluster_4'] = KMeans_4.labels_
    KMeans_5 = KMeans(n_clusters=5)
    KMeans_5.fit(pca)
    pca['cluster_5'] = KMeans_5.labels_
    colors_3 = ["#D1E5f0", "#2166AC", "#F46197"]
    colors_4 = ["#D1E5f0", "#2166AC", "#F46197", "#FE7F2D"]
    colors_5 = ["#D1E5f0", "#2166AC", "#F46197", "#FE7F2D", "#2CA58D"]
    pca['color_3'] = pca['cluster_3'].map(lambda x: colors_3[x])
    pca['color_4'] = pca['cluster_4'].map(lambda x: colors_4[x])
    pca['color_5'] = pca['cluster_5'].map(lambda x: colors_5[x])
    return pca

def albums_data(df):
    '''Get albums for the discography plot'''
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year
    df = df.drop(df[df.album == 'None'].index, axis=0)
    albums = df.groupby('album')[['release_year']].min().reset_index().sort_values(by='release_year')
    return albums

def all_artists_data():
    '''Filter all artists data to only include maximum 200 songs from each artist'''
    df = pd.read_csv('sentiment_data/grand_df.csv', index_col=0)
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['release_year'] = df['release_date'].dt.year
    df = df.drop_duplicates()
    df = df.drop(df[df['release_year'] < 2000].index, axis=0)
    df = df.drop(df[df['release_year'] > 2019].index, axis=0)
    count = df.groupby('primary_artist')[['title']].count().sort_values(by='title', ascending=False)
    artists_with_too_many_songs = count[count.title > 200].index.tolist()
    for artist in artists_with_too_many_songs:
        filtered_df = df[df['primary_artist'] == artist]
        filtered_df = filtered_df.sample(200)
        df.drop(df[df['primary_artist'] == artist].index, axis=0, inplace=True)
        df = df.append(filtered_df)
    df.drop(df[df['release_date'].isna()].index, axis=0, inplace=True)
    df.to_csv('sentiment_data/filtered_grand_df.csv')
    return df

def topics_per_year():
    df_2000 = pd.read_csv(f'topics_data/2000.csv', index_col=0)
    df_2001 = pd.read_csv(f'topics_data/2001.csv', index_col=0)
    df_2002 = pd.read_csv(f'topics_data/2002.csv', index_col=0)
    df_2003 = pd.read_csv(f'topics_data/2003.csv', index_col=0)
    df_2004 = pd.read_csv(f'topics_data/2004.csv', index_col=0)
    df_2005 = pd.read_csv(f'topics_data/2005.csv', index_col=0)
    df_2006 = pd.read_csv(f'topics_data/2006.csv', index_col=0)
    df_2007 = pd.read_csv(f'topics_data/2007.csv', index_col=0)
    df_2008 = pd.read_csv(f'topics_data/2008.csv', index_col=0)
    df_2009 = pd.read_csv(f'topics_data/2009.csv', index_col=0)
    df_2010 = pd.read_csv(f'topics_data/2010.csv', index_col=0)
    df_2011 = pd.read_csv(f'topics_data/2011.csv', index_col=0)
    df_2012 = pd.read_csv(f'topics_data/2012.csv', index_col=0)
    df_2013 = pd.read_csv(f'topics_data/2013.csv', index_col=0)
    df_2014 = pd.read_csv(f'topics_data/2014.csv', index_col=0)
    df_2015 = pd.read_csv(f'topics_data/2015.csv', index_col=0)
    df_2016 = pd.read_csv(f'topics_data/2016.csv', index_col=0)
    df_2017 = pd.read_csv(f'topics_data/2017.csv', index_col=0)
    df_2018 = pd.read_csv(f'topics_data/2018.csv', index_col=0)
    df_2019 = pd.read_csv(f'topics_data/2019.csv', index_col=0)
    return df_2000, df_2001, df_2002, df_2003, df_2004, df_2005, df_2006, df_2007, df_2008, df_2009, df_2010, df_2011, df_2012, df_2013, df_2014, df_2015, df_2016, df_2017, df_2018, df_2019
