import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from statistics import mode
import re
load_dotenv(find_dotenv())

ACCESS_TOKEN = os.environ.get('ACCESS_ID')
base_url = 'http://api.genius.com'
headers = {
    'Authorization': 'Bearer ' + ACCESS_TOKEN
}

def get_artist_api_path(search_term):
    '''Find the api_path of the queried artist on Genius.com'''
    search_url = base_url + '/search?q=' + search_term
    search_response = requests.get(search_url, headers=headers)
    search_json = search_response.json()
    artist_api_path = ''
    for _ in search_json['response']['hits']:
        if _['result']['primary_artist']['name'].lower() == search_term.lower():
            artist_api_path = _['result']['primary_artist']['api_path']
            break
    if artist_api_path == '':
        print('Couldn\'t find artist on Genius.com')
    return artist_api_path

def parse_song(json, search_term):
    '''Parse relevant information from song json'''
    songs_list = []
    for song in json['response']['songs']:
        api_path = song['api_path']
        title = song['title']
        primary_artist = song['primary_artist']['name']
        url = song['url']
        duplicated = False
        if url.endswith('-lyrics'):
            for _ in ['remix', 'live', 'version', 'grammys', 'mix', 'edit', 'vma', 'acoustic', 'demo', 'statement', 'radio', 'session', 'awards', 'extended', 'setlist']:
                if _ in url:
                    duplicated = True
            if duplicated == False:
                songs_list.append({'primary_artist': primary_artist, 'url': url, 'title' : title, 'api_path': api_path})
    return songs_list

def filter_songs(results):
    '''Filter and clean results, transform fetched json to a pandas dataframe'''
    df = pd.DataFrame(results)
    df = df.drop(df[df.title.duplicated()].index, axis=0)
    df = df[df.primary_artist == mode(df.primary_artist)]
    df['song_endpoint'] = base_url + df['api_path']
    return df

def fetch_song_info(df):
    '''Get release date and album title for each song'''
    albums = []
    release_dates = []
    song_no = 1
    for song in df['song_endpoint'].tolist():
        response = requests.get(song, headers=headers)
        json = response.json()
        release_date = json['response']['song']['release_date']
        album = json['response']['song']['album']
        if release_date != None:
            release_dates.append(release_date)
        else:
            release_dates.append('None')
        if album != None:
            albums.append(album['name'])
        else:
            albums.append('None')
        print(f'Fetched album and release date information on {song_no} songs')
        song_no += 1
    df['album'] = albums
    df['release_date'] = release_dates
    return df

def parse_song_info(results):
    '''Fill in the NaN values in the release_date column with the respective song's album's release date if it exists'''
    df = filter_songs(results)
    df = fetch_song_info(df)
    null_dates_albums = df[df.release_date == 'None']['album'].unique().tolist()
    if null_dates_albums == []:
        return df
    else:
        albums_dates = []
        for album in null_dates_albums:
            for i, row in df.iterrows():
                if row.album == album and row.release_date != 'None':
                    albums_dates.append({'album': row.album, 'release_date': row.release_date})
        if albums_dates == []:
            return df
        else:
            albums_dates = pd.DataFrame(albums_dates)
            albums_dates_count = albums_dates.groupby(['album', 'release_date'])['release_date'].count().to_frame().rename(columns={'release_date': 'count'})
            albums_dates = albums_dates_count.reset_index()
            final_dates = {}
            for album in null_dates_albums:
                if album in albums_dates.album.unique().tolist():
                    final_dates[album] = albums_dates.groupby('album')['release_date'].max()[album]
            for i, row in df[df.release_date == 'None'].iterrows():
                if row.album in list(final_dates.keys()):
                    df.at[i, 'release_date'] = final_dates[row.album]
            return df

def fetch_songs(search_term):
    '''Get all the songs that exist on Genius.com for a given artist'''
    artist_api_path = get_artist_api_path(search_term)
    current_page = 1
    is_there_next = True
    all_songs_list = []
    while is_there_next == True:
        artist_url = '{}{}/songs'.format(base_url, artist_api_path)
        params = {'page': current_page}
        artist_response = requests.get(artist_url, headers=headers, params=params)
        artist_json = artist_response.json()
        songs_list = parse_song(artist_json, search_term)
        all_songs_list.extend(songs_list)
        print(f'Fetched {current_page*15} song api paths')
        current_page += 1
        next_page = artist_json['response']['next_page']
        if next_page is None:
            is_there_next = False
    df = parse_song_info(all_songs_list)
    return df

def fetch_lyrics(df):
    '''Get lyrics for each song and clean them up with regex'''
    count = 1
    lyrics = []
    for url in df['url'].tolist():
        response = requests.get(url)
        if response.status_code == 200:
            html = BeautifulSoup(response.content, 'html.parser')
            lyric = html.find('div', {'class': 'lyrics'}).get_text().replace('\n', ' ').strip()
            lyric = re.sub(r'\[(\w+)(:)?(\s)?(-)?(\s)?(\w+)?(\s)?(\()?(\w+)?(\W+)?(:)?(\s)?(\w+)?(&)?(\s)?(\w+)?(\))?(.)?\]', '', lyric)
            print(f'Fetched lyrics from {count} songs')
            lyrics.append(lyric)
            count += 1
        else:
            df.drop(df[df.url == url].index, axis=0, inplace=True)
    df['lyrics'] = lyrics
    # remove songs that don't have lyrics
    df = df.drop(df[(df['lyrics'] == '') | (df['lyrics'].apply(lambda x : len(x.split())) < 30)].index, axis=0)
    return df

def scrape_artist(artist):
    ''' Scrape the lyrics of of all songs which exist on Genius.com of an artist'''
    print(f'Scraping {artist} lyrics from Genius.com...')
    df = fetch_songs(artist)
    df = fetch_lyrics(df)
    artist = artist.replace(' ', '').lower()
    df.to_csv(f'data/{artist}.csv', index=False)
    print('Lyrics info for this artist has been scraped from genius.com')
    existing_artists = pd.read_csv('data/list_of_artists.csv')
    existing_artists = existing_artists.append({'name': artist.replace(' ', '').lower(), 'song_count': df.shape[0]}, ignore_index=True)
    existing_artists.to_csv('data/list_of_artists.csv', index=False)
    return df

if __name__ == '__main__':
    top_100_artists = pd.read_csv('data/top_100_artists.csv')
    year = input('Enter the year for which you want to scrape the top artists: ')
    filtered_top_artists = top_100_artists[top_100_artists.year == int(year)].name.tolist()
    filtered_top_artists = [artist for artist in filtered_top_artists if artist.replace(' ', '').lower() not in existing_artists.name.tolist()]
    if filtered_top_artists != []:
        for artist in filtered_top_artists:
            df = scrape_artist(artist)
    else:
        print('All the top artists for this year have been scraped')
