from flask import Flask, session, redirect, url_for, request, render_template, jsonify
from setlist_api import get_setlist_by_id
from youtube_api import get_authenticated_service, oauth2callback, search_youtube, create_youtube_playlist
from googleapiclient.errors import HttpError
import logging
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch_setlist')
def fetch_setlist():
    setlist_id = request.args.get('setlist_id')
    setlist = get_setlist_by_id(setlist_id)
    if not setlist:
        return jsonify({"error": "Setlist not found"})
    session['setlist'] = setlist
    return jsonify({"setlist": setlist})


@app.route('/submit_setlist', methods=['POST'])
def submit_setlist():
    setlist_url = request.form['setlist_url']
    setlist_id = setlist_url.split('-')[-1].split('.')[0]
    logging.debug(f"Extracted setlist ID: {setlist_id}")
    return redirect(url_for('show_setlist', setlist_id=setlist_id))


@app.route('/show_setlist')
def show_setlist():
    setlist_id = request.args.get('setlist_id')
    setlist = get_setlist_by_id(setlist_id)
    if not setlist:
        logging.debug("Setlist not found")
        return "Setlist not found"

    session['setlist'] = setlist
    return render_template('setlist.html', setlist=setlist)


@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    if 'credentials' not in session:
        logging.debug("No user credentials in session, initiating OAuth flow")
        auth_url = get_authenticated_service()
        return jsonify({"auth_url": auth_url})

    setlist = session.get('setlist')
    if not setlist:
        return jsonify({"error": "Setlist not found"})

    try:
        video_ids = []
        for set in setlist['sets']['set']:
            for song in set['song']:
                video_id = search_youtube(song['name'], setlist['artist']['name'])
                if video_id:
                    video_ids.append(video_id)

        artist_name = setlist['artist']['name']
        event_date = setlist['eventDate']
        city = setlist['venue']['city']['name']
        state = setlist['venue']['city']['state']

        playlist_name = f"{artist_name} {event_date} Setlist - {city}, {state}"
        logging.debug(f"Creating YouTube playlist with name: {playlist_name}")

        playlist_id = create_youtube_playlist(playlist_name, video_ids)
        logging.debug(f"YouTube playlist created with ID: {playlist_id}")

        return jsonify({"playlist_url": f"https://www.youtube.com/playlist?list={playlist_id}"})
    except HttpError as e:
        logging.error(f"YouTube API error: {e}")
        if e.resp.status == 403 and 'quotaExceeded' in str(e.content):
            return jsonify({"error": "YouTube API quota exceeded. Quota resets daily at midnight Pacific time."}), 429
        return jsonify({"error": f"YouTube API error: {e.reason}"}), 500


@app.route('/oauth2callback', methods=['GET'])
def oauth2callback_route():
    logging.debug("Handling OAuth 2.0 callback")
    oauth2callback()
    logging.debug("OAuth 2.0 callback completed")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
