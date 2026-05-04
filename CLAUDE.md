# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This App Does

Flask web app that takes a setlist.fm URL, fetches the setlist via the Setlist.fm API, then creates a YouTube playlist of those songs using the YouTube Data API v3.

## Running the App

```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Run the dev server
python app.py
# App runs at http://127.0.0.1:5000/
```

## Setup Requirements

Two files must be created from templates before the app works:

1. `config.py` — copy from `config.py.template`, add your `SECRET_KEY` and `SETLIST_FM_API_KEY`
2. `client_secret.json` — copy from `client_secret.json.template`, add your Google OAuth 2.0 credentials (from Google Cloud Console, YouTube Data API v3 enabled)

## Architecture

**Three-module structure:**

- `app.py` — Flask routes only; orchestrates calls between the two API modules
- `setlist_api.py` — Single function `get_setlist_by_id()` that calls the Setlist.fm REST API
- `youtube_api.py` — All YouTube/Google API logic: OAuth 2.0 flow, YouTube search, playlist creation

**OAuth flow:** Google OAuth credentials are stored in the Flask `session` dict (via `credentials_to_dict()`). The `get_authenticated_service()` function initiates the redirect to Google; `oauth2callback()` exchanges the code for tokens and stores them in session. Credentials are not persisted across server restarts.

**Frontend:** `templates/index.html` is a single-page UI using `fetch()` to call `/fetch_setlist` (GET) and `/create_playlist` (POST). There is no `setlist.html` template — the `/show_setlist` route in `app.py` is unused dead code.

**Known issue:** The `/create_playlist` route redirects to Google OAuth if credentials are missing, but this redirect happens inside a `fetch()` call from the frontend, so the browser won't follow the redirect automatically. A fix would require returning a JSON response with the auth URL and handling the redirect in JavaScript.

**Setlist ID extraction:** The setlist ID is parsed from the URL in two places — `app.py:31` for the unused form-POST route and `index.html:64` (JS) for the actual fetch flow. They use slightly different string splitting logic.

**Dev-only flag:** `youtube_api.py` sets `OAUTHLIB_INSECURE_TRANSPORT=1` globally to allow HTTP during local development. Remove this for any production deployment.
