import json
import configparser
import os

import urllib.request
import urllib.parse


def load_json_data_from_url(base_url, url_params):
    url = '%s?%s' % (base_url, urllib.parse.urlencode(url_params))
    response = urllib.request.urlopen(url).read().decode('utf-8')
    return json.loads(response)


def make_tmdb_api_request(method, api_key, extra_params=None):
    extra_params = extra_params or {}
    url = 'https://api.themoviedb.org/3%s' % method
    params = {
        'api_key': api_key,
        'language': 'ru',
    }
    params.update(extra_params)
    return load_json_data_from_url(url, params)

def get_film_data(film_id):
    film = dict()
    f_id = '/movie/%s' % film_id
    film = make_tmdb_api_request(method=f_id, api_key=api,extra_params={'append_to_response' : 'lists,keywords,credits'})
    return film


def create_film_db(db_size):
    db = []
    film_num = 1
    while(film_num <= db_size):
        try:
            print(film_num)
            db.append(get_film_data(i))
            film_num+=1
        except urllib.error.HTTPError:
            db_size += 1
            film_num+=1
    return db

if __name__ == '__main__':
    api = os.environ.get('my_api')
    data_base = create_film_db(1000)
    file = open('film_db.json', 'w')
    file.write(json.dumps(data_base))
    file.close()