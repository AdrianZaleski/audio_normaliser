import os
import pprint
from pydub import AudioSegment
from pydub.utils import which, mediainfo


# wskazanie ścieżki do ffmpeg - biblioteki potrzebnej do konwersji audio
ffmpeg_path = which("ffmpeg")


def normalize_volume(mp3_dir, mp3_files, target_dBFS):
    for file in mp3_files:
        print("******************\n")
        print(f"Przerabiam utwor: {file}")

        # załadowanie pliku mp3
        song = AudioSegment.from_file(file, format="mp3", ffmpeg_path=ffmpeg_path)

        # Wypisanie wartości głośności przed normalizacją
        print(f"Glosnosc przed: {song.dBFS}")

        # normalizacja poziomu głośności
        normalized_song = song.apply_gain(target_dBFS - song.dBFS)

        # zapisanie znormalizowanego pliku mp3 w lokaliacji: normalized
        output_file = os.path.join(
            mp3_dir, "normalized", f"normalized_{os.path.basename(file)}"
        )

        # Eksport pliku i dodanie metadanych z oryginału
        normalized_song.export(
            out_f=output_file,
            format="mp3",
            bitrate=mediainfo(file)["bit_rate"],
            id3v2_version="3",
            tags=meta_dane_z_pliku(file),
        )

        # Wypisanie wartości głośności po normalizacji
        print(f"Glosnosc po normalizacji: {normalized_song.dBFS}")

        print("Plik został znormalizowany i zachowane zostały tagi.")

    print("**********\n")
    print("Zakończono normalizację głośności.")


def avg_volume(mp3_files: list) -> int:
    """Funkcja do określania średniej wartości głośności plików z zadanej listy.

    Args:
        mp3_files (list): lista plików, z której zostanie obliczona średnia wartość głośności

    Returns:
        int: średnia wartość głośności z listy
    """

    # lista wartości głośności
    volumes = []

    for track in mp3_files:
        song = AudioSegment.from_file(track, format="mp3", ffmpeg_path=ffmpeg_path)

        # dodanie wartości głośności do listy przed normalizacją
        print(f"Glosnosc przed: {song.dBFS} - utwor: {track}")
        print(f"\n*************************\n")

        volumes.append(song.dBFS)

    # obliczenie minimalnej, maksymalnej i średniej wartości głośności po normalizacji
    min_volume = min(volumes)
    max_volume = max(volumes)
    avg_volume = sum(volumes) / len(volumes)
    avg_volume = round(avg_volume, 2)

    print(f"Minimalna wartość głośności przed normalizacją:", min_volume)
    print(f"Maksymalna wartość głośności przed normalizacją:", max_volume)
    print(
        f"Średnia wartość głośności dla {len(volumes)} przed normalizacją zaokrąglona do 2 miejsc po przecinku:",
        avg_volume,
    )

    return avg_volume


def meta_dane_z_pliku(song) -> dict:
    # odczytanie metadanych z pliku oryginalnego
    metadata = mediainfo(song)

    # utworzenie słownika tagów
    tags = {}

    # iteracja po kluczach w słowniku metadanych
    for key in metadata.get("TAG", {}):
        # dodanie tagu do słownika tagów
        tags[key] = metadata["TAG"][key]

    return tags
