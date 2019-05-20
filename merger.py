import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_popular_artists():
    '''Scrape the top 100 artists of the year per yer from Billboard, starting from 2006'''
    base_url = 'https://www.billboard.com/charts/year-end/'
    popular_artists = []
    for year in list(range(2006, 2019)):
        search_url = base_url + str(year) + '/top-artists'
        response = requests.get(search_url)
        html = BeautifulSoup(response.content, 'html.parser')
        artists = html.find_all('div', {'class': 'ye-chart-item__title'})
        for artist in artists:
            cleaned_artist = artist.text.strip().replace('\n', '')
            popular_artists.append({'year': year, 'name': cleaned_artist})
        print(f'Completed fetching artists for {year}')
    df = pd.DataFrame(popular_artists)
    df.drop(df[df.name.duplicated()].index, axis=0, inplace=True)
    df.to_csv('data/top_100_artists.csv', index=False)
    return df

def merge_all_artists():
	''' Gather data collected for all scraped artists into one big csv'''
	artists = pd.read_csv('data/list_of_artists.csv')
	grand_df = pd.DataFrame({'api_path': [], 'primary_artist': [], 'title': [], 'url': [],
                         	 'song_endpoint': [], 'album': [], 'release_date': [], 'lyrics': []})
	count = 0
	for artist in artists.name.tolist():
	    artist_csv = pd.read_csv(f'data/{artist}.csv')
	    count += artist_csv.shape[0]
	    grand_df = grand_df.append(artist_csv)
	if count == grand_df.shape[0]:
		grand_df.to_csv('data/grand_df.csv')

fetch_popular_artists()
merge_all_artists()