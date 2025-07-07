import os
import time
from google.cloud import texttospeech
from google.api_core.exceptions import GoogleAPIError

GOOGLE_CREDENTIALS_JSON = "ENTER YOUR CREDENTIALS HERE"

WORDLIST_FILE = "wordlist.txt"
OUTPUT_DIR = "audio"

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_JSON

# TTS client
client = texttospeech.TextToSpeechClient()

# Voice & audio config
voice = texttospeech.VoiceSelectionParams(
    language_code="ja-JP",
    name="ja-JP-Wavenet-A"
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.OGG_OPUS
)

# folder exists?
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read word list
with open(WORDLIST_FILE, "r", encoding="utf-8") as f:
    katakana_words = [line.strip() for line in f if line.strip()]

# Generate audio
for word in katakana_words:
    filename = os.path.join(OUTPUT_DIR, f"{word}.ogg")
    if os.path.exists(filename):
        print(f"Skipping (already exists): {filename}")
        continue

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            synthesis_input = texttospeech.SynthesisInput(text=word)
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            with open(filename, "wb") as out:
                out.write(response.audio_content)
            print(f"Generated: {filename}")
            break
        except GoogleAPIError as e:
            print(f"Error generating '{word}' (attempt {attempt}/{MAX_RETRIES}): {e.message}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                print(f"Skipped: {word} after {MAX_RETRIES} failed attempts")

print("\n done. Audio files are in the 'audio' folder.")
