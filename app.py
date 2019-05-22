import pandas as pd
import flask
import numpy as np
from flask import render_template, request
from plotter import sentiment_plot, cluster_plot
from bokeh.embed import components
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from lyrics_scraper import scrape_artist
from sentiment_extractor import extract_sentiments

def read_data(df):
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
    return pca

app = flask.Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    return render_template('search.html')

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    try:
        if flask.request.method == 'POST':
            inputs = flask.request.form
            artist = inputs['name']
            scrape_artist(artist)
            extract_sentiments(artist)
        return render_template('scrape.html')
    except:
        return render_template('scraper_error.html')

@app.route('/artist', methods=['POST', 'GET'])
def artist():
    try:
        artist = flask.request.args['name']
        stripped_artist = artist.replace(' ', '')
        df = pd.read_csv(f'sentiment_data/{stripped_artist}.csv', index_col=0)
        df = df.drop_duplicates()
        polarity = round(df.polarity.mean(), 2)
        normalized_df = read_data(df)
        chart_1 = sentiment_plot(normalized_df)
        clusters = cluster_data(df)
        chart_2 = cluster_plot(clusters)
        script_1, div_1 = components(chart_1)
        script_2, div_2 = components(chart_2)
        image = f'static/images/word_clouds/{stripped_artist}.png'
        return render_template('artist.html', the_script_1=script_1, the_div_1=div_1, the_script_2=script_2, the_div_2=div_2, polarity=polarity, artist=artist.upper(), image=image)
    except:
        return render_template('inventory_error.html')

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 4000
    app.run(HOST, PORT, debug=True)
