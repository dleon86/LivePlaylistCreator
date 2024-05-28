import requests
import logging

SETLIST_FM_API_KEY = 'o-W-zRQa2mwq4K_iGJ0GwFo2gRbr31cUoThh'

logging.basicConfig(level=logging.DEBUG)

def get_setlist_by_id(setlist_id):
    url = f"https://api.setlist.fm/rest/1.0/setlist/{setlist_id}"
    headers = {
        'x-api-key': SETLIST_FM_API_KEY,
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    logging.debug(f"Request URL: {url}")
    logging.debug(f"Response Status Code: {response.status_code}")
    logging.debug(f"Response Content: {response.content}")
    if response.status_code == 200:
        return response.json()
    else:
        return None
