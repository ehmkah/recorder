import yt_dlp
import os

# Die URL deiner Playlist
playlist_url = "https://music.youtube.com/playlist?list=OLAK5uy_kcIHuKjVCx_z0X4o-m1BPjFgnn2ywUsog"

# Einstellungen für den Download
ydl_opts = {
    'format': 'bestaudio/best',
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    },
    'cookiesfrombrowser': ('firefox',),
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
        {
            # Schritt 2: Metadaten (Titel, Artist, etc.) einbetten
            'key': 'FFmpegMetadata',
            'add_metadata': True,
        },
        {
            # Schritt 3: Das Cover-Bild in die MP3-Datei bügeln
            'key': 'EmbedThumbnail',
        }

    ],
    'sleep_interval': 5,
    'max_sleep_interval': 15,
    # Dateiname: Playlist-Index - Künstler - Titel.mp3
    'outtmpl': '%(playlist_index)s - %(artist)s - %(title)s.%(ext)s',
    # Falls kein Künstler gefunden wird, nutze den Titel
    'default_search': 'ytsearch',
    'noplaylist': False,
}


def download_playlist(url):
    print(f"--- Starte Download der Playlist ---")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n--- Alle Lieder erfolgreich gespeichert! ---")
    except Exception as e:
        print(f"Fehler aufgetreten: {e}")


if __name__ == "__main__":
    download_playlist(playlist_url)
