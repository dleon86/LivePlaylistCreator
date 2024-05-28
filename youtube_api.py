import os
import google.auth.transport.requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from flask import session, redirect, request, url_for
import logging
import oauthlib.oauth2

# Set up OAuth 2.0 Client ID and Secret from Google API Console
CLIENT_SECRETS_FILE = "client_secret.json"

# The OAuth 2.0 scopes
SCOPES = ['https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/youtube.force-ssl']

# Disable OAuthlib's HTTPS requirement when running locally.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Set up the OAuth 2.0 flow
def get_authenticated_service():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback_route', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    session['state'] = state
    logging.debug(f"Redirecting to Google OAuth 2.0 authorization URL: {authorization_url}")
    return redirect(authorization_url)

def oauth2callback():
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback_route', _external=True)

    authorization_response = request.url
    logging.debug(f"Authorization response received: {authorization_response}")
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    logging.debug(f"OAuth 2.0 credentials stored in session: {session['credentials']}")

    return redirect(url_for('create_playlist'))

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

def get_youtube_service():
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube

def search_youtube(song_title, artist_name):
    youtube = get_youtube_service()
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=f"{song_title} {artist_name}"
    )
    response = request.execute()
    if 'items' in response and len(response['items']) > 0:
        video_id = response['items'][0]['id']['videoId']
        return video_id
    else:
        return None

def create_youtube_playlist(playlist_name, video_ids):
    youtube = get_youtube_service()
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_name,
                "description": "Playlist created from setlist",
                "tags": ["music", "setlist"],
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "public"
            }
        }
    )
    response = request.execute()
    playlist_id = response['id']
    logging.debug(f"Created YouTube playlist with ID: {playlist_id}")

    for video_id in video_ids:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()

    return playlist_id
