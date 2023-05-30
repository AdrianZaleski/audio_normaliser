import os
import pprint
import time
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

    print(f"Zaczalem obliczanie sredniej dla {len(song_list)} elementow")
    values = []
    maximum = {
        "najcichszy": [float("inf"), None],
        "najglosniejszy": [-float("inf"), None],
    }

    for file_name in song_list:
        print(f"Sprawdzam glosnosc utworu: {file_name}")

        if file_name.lower().endswith(".mp3"):
            min_value = min(values) if values else float("inf")
            max_value = max(values) if values else (-float("inf"))

            audio = AudioSegment.from_file(file_name, format="mp3")
            values.append(audio.dBFS)

            poziom_audio = audio.dBFS
            print(f"Wartosc audio.dBFS: {audio.dBFS}")

            if poziom_audio < min_value:
                min_value = poziom_audio
                maximum["najcichszy"] = [min_value, file_name]

            if poziom_audio > max_value:
                max_value = poziom_audio
                maximum["najglosniejszy"] = [max_value, file_name]
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
        print(f"max_db : {max(values)} nalezy do: {maximum.get('najglosniejszy')}")
        print(f"average_db : {average_db}")
        print(f"min_db : {min(values)} nalezy do: {maximum.get('najcichszy')}")
        print(f"Zapisano srednia glosnosc do pliku : {target_db_file}")

        print(f"\n****** NAJ UTWORY: ******")
        print(f"\nNajcichszy utwor: ({max(values)}dB: \n{maximum['najcichszy'][1]}")
        print(
            f"\nNajglosniejszy utwor: ({min(values)}dB: \n{maximum['najglosniejszy'][1]}"
        )

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

    i = 0
    t0 = time.time()
    for file in song_list:
        t1 = time.time()
        i += 1
        print("******************\n")
        print(f"Przerabiam utwor: {file} jako {i}/{len(song_list)}")

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
            # mp3_folder, "normalized", f"normalized_{os.path.basename(file)}"
            mp3_folder,
            "normalized",
            f"{os.path.basename(file)}",
        )

        # Eksport pliku i dodanie metadanych z oryginału
        normalized_song.export(
            out_f=output_file,
            format="mp3",
            bitrate=mediainfo(file)["bit_rate"],
            id3v2_version="3",
            tags=meta_dane_z_pliku(file),
        )
        t2 = time.time()
        # Wypisanie wartości głośności po normalizacji
        print(f"Glosnosc po normalizacji: {normalized_song.dBFS}")

        print("Plik został znormalizowany i zachowane zostały tagi.")
        print(
            f"Przerobiono utwor: {i}/{len(song_list)} ({100*i//len(song_list)}%)",
            end="",
        )
        single = round(t2 - t1, 2)
        total = round(t2 - t0, 2)

        # obliczenie godzin, minut i sekund
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(
            f" zajelo to: {single}s (total: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d} hh:mm:ss)"
        )

    print("**********\n")
    print("Zakończono normalizację głośności.")
