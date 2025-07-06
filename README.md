# Katakana TTS Generator

Generates OGG audio files from a list of Japanese katakana words using Google Cloud Text-to-Speech.

## Requirements

- Python 3.x  
- `google-cloud-texttospeech` (`pip install google-cloud-texttospeech`)  
- Google Cloud TTS credentials JSON

## Usage

1. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to your credentials file.
2. Put katakana words (one per line) in `wordlist.txt`.
3. Run the script: `python Generate.py`
4. Audio files will be saved in the `audio/` folder.
