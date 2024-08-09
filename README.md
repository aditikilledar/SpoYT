# SpoYT
Want to export playlists from Spotify to Youtube? I gotchu. :)

# SpoYT: Spotify to YouTube Playlist Transfer

SpoYT is a Python application that transfers playlists from Spotify to YouTube. This tool allows you to migrate your favorite playlists across platforms with ease.

## Requirements

- Python 3.11 or later
- `google-auth-oauthlib`
- `google-api-python-client`
- `spotipy`
- `python-dotenv`

You can install the required Python libraries using pip:

```bash
pip install google-auth-oauthlib google-api-python-client spotipy python-dotenv
```

## Setup

### 1. Google API Setup

1. **Create a Google Cloud Project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.

2. **Enable the YouTube Data API v3**:
   - Navigate to the “APIs & Services” > “Library” and search for "YouTube Data API v3".
   - Enable the API for your project.

3. **Create OAuth 2.0 Credentials**:
   - Go to “APIs & Services” > “Credentials”.
   - Click on “Create Credentials” and choose “OAuth 2.0 Client ID”.
   - Select “Desktop app” (or “Web application” if applicable) and configure the redirect URIs if necessary.
   - Download the `credentials.json` file.

### 2. Spotify API Setup

1. **Create a Spotify Developer Account**:
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
   - Log in or sign up, then create a new application.

2. **Get Credentials**:
   - Note your `Client ID` and `Client Secret`.
   - Set the redirect URI (e.g., `http://localhost:8888/callback`).

### 3. Configuration

1. **Create a `.env` File**:
   - In the root directory of your project, create a `.env` file.
   - Add the following lines with your own credentials:

     ```env
     SPOTIPY_CLIENT_ID=your_spotify_client_id
     SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
     SPOTIPY_REDIRECT_URI=http://localhost:8888/callback

     YOUTUBE_CLIENT_SECRET_FILE=path_to_your_credentials.json
     ```

### 4. Running the Application

1. **Authenticate with Spotify and YouTube**:
   - Ensure that you have set up OAuth 2.0 credentials as described in the setup sections.

2. **Execute the Script**:
   - Run the Python script to start transferring your playlist:

     ```bash
     python main.py
     ```

### Usage

1. **Find your Spotify Playlist Id**:
   - Add it to the ```spotify_playlist_id``` variable in main.py.

2. **Decide New Playlist Name**:
   - - Add it to the ```youtube_playlist_title``` variable in main.py.

### Example

Here is an example of how to use the provided script to add a video to a YouTube playlist:

```python
if __name__ == "__main__":
    spotify_playlist_id = '37i9dQZF1DX9tPFwDMOaN1'
    youtube_playlist_title = 'KPOP ON'
    transfer_playlist(spotify_playlist_id, youtube_playlist_title)
```

### Troubleshooting

- **Service Unavailable**: If you encounter `SERVICE_UNAVAILABLE` errors, check the Google API status and retry after some time.
- **Invalid Credentials**: Ensure your `credentials.json` and `.env` file are correctly configured.
- **Quota Limits**: Verify you have not exceeded API quota limits.

### License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). See the [LICENSE](LICENSE) file for details.
