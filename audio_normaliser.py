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


# Funkcja do obliczania średniej arytmetycznej głośności z utworów w folderach
def calculate_average_volume(folder_path) -> float:
    """Funkcja obliczająca średnią arytmetyczną wartość głośności wszystkich plików mp3 w folderach i podfolderach. W przypadku braku takich plików - zwracany jest None.

    Args:
        folder_path (_type_): Ścieżka do folderu nadrzędnego do normalizacji

    Returns:
        float or None: Średnia arytmetyczna głośności lub None
    """

    values = []

    for root, _, files in os.walk(folder_path):
        print(f'\n root: {root}')
        print(f'\n _: {_}')
        print(f'\n files: {files}')
        
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.endswith(".mp3"):
                audio = AudioSegment.from_file(file_path, format="mp3")
                values.append(audio.dBFS)
            
    if values:
        total_db = sum(values)
        num_files = len(values)
        average_db = round((total_db / num_files),2)
        
        print(f'total_db : {total_db}')
        print(f'num_files : {num_files}')
        print(f'max_db : {max(values)}')
        print(f'average_db : {average_db}')
        print(f'min_db : {min(values)}')
        
        result = average_db
    else:
        print("Brak plików mp3 w folderze.")
        result = None
    return result


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

