import pyaudio
import sys
from pydub import AudioSegment
import time

# --- KONFIGURATION ---
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "aufnahme_session.mp3"

p = pyaudio.PyAudio()

# 1. BlackHole suchen
device_index = None
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if "BlackHole" in dev['name']:
        device_index = i
        break

if device_index is None:
    print("Fehler: BlackHole wurde nicht gefunden!")
    sys.exit()

print(f"Nutze Gerät: {p.get_device_info_by_index(device_index)['name']}")

# 2. Stream starten
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK)

print("\n" + "="*30)
print("🔴 AUFNAHME LÄUFT...")
print("Beenden mit: STRG + C")
print("="*30 + "\n")

frames = []

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
except KeyboardInterrupt:
    print("\n\n--- Aufnahme gestoppt. ---")
finally:
    # Stream schließen
    stream.stop_stream()
    stream.close()
    p.terminate()

# 3. Konvertierung in MP3
print("Konvertiere zu MP3... Bitte warten.")

# Wir fügen die Chunks zusammen
raw_data = b''.join(frames)

# Erstelle ein AudioSegment aus den Rohdaten
audio_segment = AudioSegment(
    data=raw_data,
    sample_width=p.get_sample_size(FORMAT),
    frame_rate=RATE,
    channels=CHANNELS
)

# Export als MP3
audio_segment.export(OUTPUT_FILENAME, format="mp3", bitrate="192k")

print(f"ERFOLG: Datei gespeichert als '{OUTPUT_FILENAME}'")