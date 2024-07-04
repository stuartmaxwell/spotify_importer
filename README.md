# Spotify Album Import Script

> Please note that I used Claude.ai to produce this code, and even the README contents below were written by Claude. This script worked for me and I'm sharing it, in case it's useful for others. The remainder of this README file and the `spotify_import.py` script itself were written completely by Claude 3.5 Sonnet.

This Python script allows you to import your local music library into Spotify by adding entire albums to your Spotify library. It's designed to work with a local music collection organized by artist and album folders.

## Features

- Searches Spotify for albums based on your local folder structure
- Adds full albums to your Spotify library
- Provides a dry run option to preview changes without modifying your Spotify library
- Generates a detailed CSV log of the import process
- Displays real-time progress and a summary of results

## Prerequisites

- Python 3.6 or higher
- A Spotify Premium account
- Spotify Developer credentials (Client ID and Client Secret)

## Installation

1. Clone this repository or download the script file.

2. Install the required Python packages:

   ```bash
   pip install spotipy python-dotenv
   ```

3. Create a `.env` file in the same directory as the script with your Spotify API credentials:

   ```bash
   SPOTIPY_CLIENT_ID=your_client_id
   SPOTIPY_CLIENT_SECRET=your_client_secret
   ```

   Replace `your_client_id` and `your_client_secret` with your actual Spotify Developer credentials.

4. In your Spotify Developer dashboard, add `http://localhost:8080` as a redirect URI for your application.

## Usage

Run the script from the command line:

```bash
python spotify_import.py /path/to/your/music/directory [--dry-run]
```

- Replace `/path/to/your/music/directory` with the actual path to your local music collection.
- Use the `--dry-run` flag to simulate the import process without making changes to your Spotify library.

## Music Directory Structure

The script expects your music directory to be organized as follows:

```bash
/path/to/your/music/directory
├── Artist1
│   ├── Album1
│   └── Album2
├── Artist2
│   ├── Album1
│   └── Album2
└── ...
```

## Output

- The script will display real-time progress in the terminal.
- A CSV log file will be generated with details of each processed album.
- After completion, a summary will show the number of albums matched and not found.

## Notes

- The script adds albums to your Spotify library, not to a specific playlist.
- Albums not found on Spotify will be logged but not added to your library.
- Be mindful of Spotify's API rate limits when running the script on large music collections.

## Troubleshooting

- If you encounter authentication issues, ensure your Spotify API credentials in the `.env` file are correct.
- For albums not found, check if the artist and album names in your folder structure match those on Spotify.

## License

This script is provided "as is", without warranty of any kind. Use at your own risk.

## Contributing

Feel free to fork this project and submit pull requests with any enhancements.
