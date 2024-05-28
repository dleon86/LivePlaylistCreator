from flask import Flask, session, redirect, url_for, request, render_template
from setlist_api import get_setlist_by_id
from youtube_api import get_authenticated_service, oauth2callback, search_youtube, create_youtube_playlist
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    setlist_id = request.form['setlist_id']

    setlist = get_setlist_by_id(setlist_id)
    if not setlist:
        logging.debug("Setlist not found")
        return "Setlist not found"

    if 'credentials' not in session:
        logging.debug("No credentials in session, initiating OAuth flow")
        return get_authenticated_service()

    video_ids = []
    for song in setlist['sets']['set'][0]['song']:
        video_id = search_youtube(song['name'], setlist['artist']['name'])
        if video_id:
            video_ids.append(video_id)

    playlist_id = create_youtube_playlist(f"{setlist['artist']['name']} {setlist['eventDate']} Setlist", video_ids)
    logging.debug(f"YouTube playlist created with ID: {playlist_id}")

    return redirect(f"https://www.youtube.com/playlist?list={playlist_id}")

@app.route('/oauth2callback')
def oauth2callback_route():
    logging.debug("Handling OAuth 2.0 callback")
    response = oauth2callback()
    logging.debug("OAuth 2.0 callback completed")
    return response

if __name__ == '__main__':
    app.run(debug=True)
