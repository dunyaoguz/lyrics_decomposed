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
    df_normalized.index = pd.to_datetime(df_normalized.index)
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
    pca = pca.fit_transform(df[['anger', 'anticipation', 'disgust', 'fear', 'joy', 'surprise', 'trust']])
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
    pca['title'] = df['title']
    pca['album'] = df['album']
    pca = pca.replace('None', 'Unknown')
    return pca

def albums_data(df):
    '''Get albums for the discography plot'''
    df['release_date'] = pd.to_datetime(df['release_date'])
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
