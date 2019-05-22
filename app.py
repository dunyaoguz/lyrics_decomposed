import pandas as pd
import flask
import numpy as np
from flask import render_template
from plotter import sentiment_plot
from bokeh.embed import components

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

app = flask.Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
  return render_template('home.html')

@app.route('/artist', methods=['POST', 'GET'])
def artist():
    artist = 'arianagrande'
    df = pd.read_csv(f'sentiment_data/{artist}.csv', index_col=0)
    polarity = round(df.polarity.mean(), 2)
    df = read_data(df)
    chart = sentiment_plot(df)
    script, div = components(chart)
    return render_template('artist.html', the_script=script, the_div=div, polarity=polarity)

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 4000
    app.run(HOST, PORT, debug=True)
