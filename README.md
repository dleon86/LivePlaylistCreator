# Live Playlist Creator

Live Playlist Creator is a Flask web application that allows users to create a YouTube music playlist from a given setlist. The application uses the Setlist.fm API to fetch the setlist details and the YouTube Data API to create the playlist.

## Features

- Fetches setlist details from Setlist.fm
- Searches for songs on YouTube
- Creates a YouTube playlist with the searched songs

## Prerequisites

- Python 3.6 or higher
- Setlist.fm API key
- Google Cloud project with YouTube Data API enabled
- OAuth 2.0 credentials (client_secret.json)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/LivePlaylistCreator.git
    cd LivePlaylistCreator
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Add your configuration and secrets:

    - Copy the template `config.py` and update it with your details:

        ```bash
        cp config.py.template config.py
        ```

        Update `config.py` with your `SECRET_KEY` and `SETLIST_FM_API_KEY`.

    - Copy the template `client_secret.json` and update it with your details:

        ```bash
        cp client_secret.json.template client_secret.json
        ```

        Update `client_secret.json` with your OAuth 2.0 client secrets.

## Running the Application

1. Start the Flask application:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

3. Follow the instructions to authorize the application with your Google account.

## Project Structure

- `app.py`: The main Flask application file.
- `setlist_api.py`: Contains the function to fetch setlist details from Setlist.fm.
- `youtube_api.py`: Contains functions to handle YouTube Data API operations.
- `templates/index.html`: The HTML template for the main page.
- `config.py.template`: Template for configuration file.
- `client_secret.json.template`: Template for OAuth 2.0 credentials file.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
