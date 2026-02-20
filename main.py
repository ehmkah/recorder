import pyaudio
import wave
import sys

# --- KONFIGURATION ---
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5        # Testdauer: 5 Sekunden
OUTPUT_FILENAME = "test_aufnahme.wav"

p = pyaudio.PyAudio()

# 1. BlackHole suchen
device_index = None
print("--- Suche nach BlackHole Device ---")

for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    # Wir suchen nach "BlackHole" im Namen des Audio-Geräts
    if "BlackHole" in dev['name']:
        device_index = i
        print(f"Gefunden: '{dev['name']}' auf Index {i}")
        break

if device_index is None:
    print("FEHLER: BlackHole wurde nicht gefunden!")
    print("Stelle sicher, dass BlackHole installiert ist.")
    p.terminate()
    sys.exit()

# 2. Aufnahme-Stream vorbereiten
try:
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK)
except Exception as e:
    print(f"Fehler beim Öffnen des Streams: {e}")
    p.terminate()
    sys.exit()

print(f"\n--- Aufnahme gestartet ({RECORD_SECONDS} Sek) ---")
print("TIPP: Spiel jetzt Musik ab (du wirst nichts hören!).")

frames = []

# 3. Daten in den RAM lesen
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    try:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    except Exception as e:
        print(f"Fehler während der Aufnahme: {e}")
        break

print("--- Aufnahme beendet ---")

# 4. Aufräumen
stream.stop_stream()
stream.close()
p.terminate()

# 5. Als WAV speichern (zum Testen am einfachsten)
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"\nFERTIG! Datei gespeichert als: {OUTPUT_FILENAME}")
print("Stelle deinen Ton-Ausgang wieder auf 'Lautsprecher' um sie anzuhören.")