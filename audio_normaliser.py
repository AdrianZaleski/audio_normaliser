import os
import pprint
from pydub import AudioSegment
from pydub.utils import which, mediainfo


# wskazanie ścieżki do ffmpeg - biblioteki potrzebnej do konwersji audio
ffmpeg_path = which("ffmpeg")


# odczytanie metadanych z pliku oryginalnego
def meta_dane_z_pliku(song) -> dict:
    metadata = mediainfo(song)

    # utworzenie słownika tagów
    tags = {}

    # iteracja po kluczach w słowniku metadanych
    for key in metadata.get("TAG", {}):
        # dodanie tagu do słownika tagów
        tags[key] = metadata["TAG"][key]

    return tags


# Funkcja do obliczania średniej arytmetycznej głośności z listy plików mp3
def calculate_average_volume_from_list(song_list) -> float:
    """Funkcja obliczająca średnią arytmetyczną wartość głośności wszystkich plików mp3 w dostarczonej liście. W przypadku braku takich plików - zwracany jest None.

    Args:
        song_list (list): lista plików, z których obliczana będzie średnia wartość głośności

    Returns:
        float or None: Średnia arytmetyczna głośności lub None
    """

    values = []

    for file_name in song_list:
        if file_name.endswith(".mp3"):
            audio = AudioSegment.from_file(file_name, format="mp3")
            values.append(audio.dBFS)

    if values:
        total_db = sum(values)
        num_files = len(values)
        average_db = round((total_db / num_files), 2)

        target_db_file = "target_volume.txt"
        with open(target_db_file, "w") as f:
            f.write(str(average_db))

        print(f"\n****** DEBUG ****** ")
        print(f"****** calculate_average_volume_from_list ******\n ")
        print(f"total_db : {total_db}")
        print(f"num_files : {num_files}")
        print(f"max_db : {max(values)}")
        print(f"average_db : {average_db}")
        print(f"min_db : {min(values)}")
        print(f"Zapisano srednia glosnosc do pliku : {target_db_file}")

        print(f"\n****** DEBUG END ******\n ")

        result = average_db
    else:
        print("Brak plików mp3 w folderze.")
        result = None
    return result


# Normalizacja głośności listy plików:
def normalize_volume(song_list, target_dBFS):
    """Głowny proces normalizacji głośności plików mp3 do zadanej wartości głośności.
    Dodatkowo zapisuje pliki w określonej lokalizacji.

    Args:
        song_list (list): lista utworów mp3 do przerobienia
        target_dBFS (float): wartość głośności do jakiej ma być przeprowadzona normalizacja
    """
    
    for file in song_list:
        print("******************\n")
        print(f"Przerabiam utwor: {file}")

        # załadowanie pliku mp3
        song = AudioSegment.from_file(file, format="mp3", ffmpeg_path=ffmpeg_path)

        # Wypisanie wartości głośności przed normalizacją
        print(f"Glosnosc przed: {song.dBFS}")

        # normalizacja poziomu głośności
        normalized_song = song.apply_gain(target_dBFS - song.dBFS)

        # ścieżka do aktualnego pliku:
        mp3_folder = os.path.dirname(file)

        # Sprawdzenie i utworzenie folderu 'normalized', jeśli nie istnieje
        output_folder = os.path.join(mp3_folder, "normalized")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)

        # zapisanie znormalizowanego pliku mp3 w lokaliacji: normalized
        output_file = os.path.join(
            mp3_folder, "normalized", f"normalized_{os.path.basename(file)}"
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
