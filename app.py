import pandas as pd
import numpy as np
import flask
from flask import render_template, request
from plotter import sentiment_plot, cluster_plot, view_albums, artists_cluster
from plotter import polarity_plot
from bokeh.embed import components
from lyrics_scraper import scrape_artist
from sentiment_extractor import extract_sentiments
from IPython.display import HTML
from helper import read_data, cluster_data, albums_data, all_artists_data, topics_per_year
from word_cloud_generator import generate_word_cloud
from topic_modeller import model_topic

app = flask.Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    df = pd.read_csv('sentiment_data/filtered_grand_df.csv')
    random = df['primary_artist'].sample(1).tolist()[0]
    url = "/artist?name=" + random
    return render_template('search.html', feeling_lucky=url)

@app.route('/compare_search', methods=['POST', 'GET'])
def compare_search():
    df = pd.read_csv('sentiment_data/filtered_grand_df.csv')
    randoms = df['primary_artist'].sample(2).tolist()
    url = "/compare_artists?name_1=" + randoms[0].replace(' ', '+') + "&name_2=" + randoms[1].replace(' ', '+')
    return render_template('compare_search.html', feeling_lucky=url)

@app.route('/compare_artists', methods=['POST', 'GET'])
def compare_artists():
    try:
        artist_1 = flask.request.args['name_1']
        artist_2 = flask.request.args['name_2']
        stripped_artist_1 = artist_1.lower().replace(' ', '')
        stripped_artist_2 = artist_2.lower().replace(' ', '')
        df_1 = pd.read_csv(f'sentiment_data/{stripped_artist_1}.csv')
        df_2 = pd.read_csv(f'sentiment_data/{stripped_artist_2}.csv')
        polarity_1 = round(df_1.polarity.mean(), 2)
        polarity_2 = round(df_2.polarity.mean(), 2)
        return render_template('compare_artists.html', artist_1=artist_1.upper(), artist_2=artist_2.upper(), polarity_1=polarity_1, polarity_2=polarity_2)
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
            generate_word_cloud(artist)
            model_topic(artist)
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
        chart_1 = sentiment_plot(normalized_df, 0.4)
        clusters = cluster_data(df)
        clusters['title'] = df['title']
        clusters['album'] = df['album']
        clusters = clusters.replace('None', 'Unknown')
        chart_2 = cluster_plot(clusters)
        albums = albums_data(df)
        chart_3 = view_albums(albums)
        script_1, div_1 = components(chart_1)
        script_2, div_2 = components(chart_2)
        script_3, div_3 = components(chart_3)
        image = f'static/images/word_clouds/{stripped_artist}.png'
        data_url = f'/artist_data?name={stripped_artist}'
        topics = pd.read_csv(f'topics_data/{stripped_artist}.csv', index_col=0)
        return render_template('artist.html', the_script_1=script_1, the_div_1=div_1, the_script_2=script_2, the_div_2=div_2, polarity=polarity, artist=artist.upper(), image=image,
        the_script_3=script_3, the_div_3=div_3, data_url=data_url, topic_1=topics['words'][0], topic_2=topics['words'][1], topic_3=topics['words'][2], topic_4=topics['words'][3], topic_5=topics['words'][4])
    except:
        return render_template('inventory_error.html')

@app.route('/popular_artists', methods=['POST', 'GET'])
def popular_artists():
    df = pd.read_csv('sentiment_data/filtered_grand_df.csv')
    df_normalized = read_data(df)
    chart_1 = sentiment_plot(df_normalized, 0.15)
    script_1, div_1 = components(chart_1)
    polarity = df.groupby('release_year')[['polarity']].mean().reset_index()
    polarity['text'] = round(polarity['polarity'],2)
    chart_2 = polarity_plot(polarity)
    script_2, div_2 = components(chart_2)
    df_2000, df_2001, df_2002, df_2003, df_2004, df_2005, df_2006, df_2007, df_2008, df_2009, df_2010, df_2011, df_2012, df_2013, df_2014, df_2015, df_2016, df_2017, df_2018, df_2019 = topics_per_year()
    df_2 = pd.read_csv('sentiment_data/grand_df.csv', index_col=0)
    artists = df.groupby('primary_artist')[['anger', 'anticipation', 'disgust', 'fear', 'joy', 'positive', 'negative', 'sadness', 'surprise', 'trust']].mean()
    artists = artists.reset_index()
    clusters = cluster_data(artists)
    clusters['artist'] = artists['primary_artist']
    chart_3 = artists_cluster(clusters)
    script_3, div_3 = components(chart_3)
    return render_template('popular_artists.html', the_script_1=script_1, the_div_1=div_1, songs_no=df.shape[0], the_script_2=script_2, the_div_2=div_2, topic_1=df_2000['words'][0], topic_2=df_2000['words'][1], topic_3=df_2000['words'][2],
    topic_4=df_2001['words'][0], topic_5=df_2001['words'][1], topic_6=df_2001['words'][2], topic_7=df_2002['words'][0], topic_8=df_2002['words'][1], topic_9=df_2002['words'][2], topic_10=df_2003['words'][0], topic_11=df_2003['words'][1], topic_12=df_2003['words'][2],
    topic_13=df_2004['words'][0], topic_14=df_2004['words'][1], topic_15=df_2004['words'][2], topic_16=df_2005['words'][0], topic_17=df_2005['words'][1], topic_18=df_2005['words'][2], topic_19=df_2006['words'][0], topic_20=df_2006['words'][1], topic_21=df_2006['words'][2],
    topic_22=df_2007['words'][0], topic_23=df_2007['words'][1], topic_24=df_2007['words'][2], topic_25=df_2008['words'][0], topic_26=df_2008['words'][1], topic_27=df_2008['words'][2], topic_28=df_2009['words'][0], topic_29=df_2009['words'][1], topic_30=df_2009['words'][2],
    topic_31=df_2010['words'][0], topic_32=df_2010['words'][1], topic_33=df_2010['words'][2], topic_34=df_2011['words'][0], topic_35=df_2011['words'][1], topic_36=df_2011['words'][2], topic_37=df_2012['words'][0], topic_38=df_2012['words'][1], topic_39=df_2012['words'][2],
    topic_40=df_2013['words'][0], topic_41=df_2013['words'][1], topic_42=df_2013['words'][2], topic_43=df_2014['words'][0], topic_44=df_2014['words'][1], topic_45=df_2014['words'][2], topic_46=df_2015['words'][0], topic_47=df_2015['words'][1], topic_48=df_2015['words'][2],
    topic_49=df_2016['words'][0], topic_50=df_2016['words'][1], topic_51=df_2016['words'][2], topic_52=df_2017['words'][0], topic_53=df_2017['words'][1], topic_54=df_2017['words'][2], topic_55=df_2018['words'][0], topic_56=df_2018['words'][1], topic_57=df_2018['words'][2],
    topic_58=df_2019['words'][0], topic_59=df_2019['words'][1], topic_60=df_2019['words'][2], the_script_3=script_3, the_div_3=div_3)

@app.route('/popular_artists_list', methods=['POST', 'GET'])
def popular_artists_list():
    df = pd.read_csv('data/list_of_artists.csv')[['name']]
    df = HTML(df.to_html(classes="table table-stripped"))
    return render_template('popular_artists_list.html', data = df)

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 4000
    app.run(HOST, PORT, debug=True)
