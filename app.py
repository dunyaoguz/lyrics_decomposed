import pandas as pd
import numpy as np
import flask
from flask import render_template, request
from plotter import sentiment_plot, cluster_plot, view_albums
from bokeh.embed import components
from lyrics_scraper import scrape_artist
from sentiment_extractor import extract_sentiments
from IPython.display import HTML
from helper import read_data, cluster_data, albums_data

app = flask.Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    return render_template('search.html')

@app.route('/compare_search', methods=['POST', 'GET'])
def compare_search():
    return render_template('compare_search.html')

@app.route('/compare_artists', methods=['POST', 'GET'])
def compare_artists():
    try:
        artist_1 = flask.request.args['name_1']
        artist_2 = flask.request.args['name_2']
        return render_template('compare_artists.html', artist_1=artist_1.upper(), artist_2=artist_2.upper())
    except:
        return render_template('inventory_error.html')

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

@app.route('/artist_data', methods=['POST', 'GET'])
def artist_data():
    artist = flask.request.args['name']
    df = pd.read_csv(f'data/{artist}.csv')
    df = df.drop(df[df.release_date == 'None'].index, axis=0)
    df = df[['primary_artist', 'album', 'release_date', 'title', 'url']].sort_values(by='release_date').reset_index()
    df = HTML(df.drop('index', axis=1).to_html(classes="table table-stripped"))
    return render_template('artist_data.html', data = df)

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
        albums = albums_data(df)
        chart_3 = view_albums(albums)
        script_1, div_1 = components(chart_1)
        script_2, div_2 = components(chart_2)
        script_3, div_3 = components(chart_3)
        image = f'static/images/word_clouds/{stripped_artist}.png'
        data_url = f'/artist_data?name={stripped_artist}'
        return render_template('artist.html', the_script_1=script_1, the_div_1=div_1, the_script_2=script_2, the_div_2=div_2, polarity=polarity, artist=artist.upper(), image=image, the_script_3=script_3, the_div_3=div_3, data_url=data_url)
    except:
        return render_template('inventory_error.html')

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 4000
    app.run(HOST, PORT, debug=True)
