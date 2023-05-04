import os
from pydub import AudioSegment
from pydub.utils import which
from datetime import datetime

# wskazanie ścieżki do ffmpeg
ffmpeg_path = which("ffmpeg")


# TODO:
# - Zapisanie wartości normalizacji do pliku
# - Opcja do zaczytania wartości z pliku do normalizacji
# - Przerabianie plików wewnątrz podfolderów
# - Dodanie wgrywania oryginalnych metadanych z oryginału do normalizowanego pliku (tytuł, artysta, numer ścieżki itp.)

def normalize_volume(mp3_files, target_dBFS):
    
    for file in mp3_files:
        print('******************\n')
        print(f'Przerabiam utwor: {file}')

        # załadowanie pliku mp3
        song = AudioSegment.from_file(file, format="mp3", ffmpeg_path=ffmpeg_path)
        
        # dodanie wartości głośności do listy przed normalizacją
        print(f'Glosnosc przed: {song.dBFS}')

        # normalizacja poziomu głośności
        normalized_song = song.apply_gain(target_dBFS - song.dBFS)
       
        # zapisanie znormalizowanego pliku mp3
        output_file = os.path.join(mp3_dir, 'normalized', f"normalized_{os.path.basename(file)}")
        normalized_song.export(output_file, format="mp3")
        
        # dodanie wartości głośności do listy przed normalizacją
        print(f'Glosnosc po normalizacji: {normalized_song.dBFS}')
    
    print('**********\n')
    print("Zakończono normalizację głośności.")


def avg_volume(mp3_files):
    
    # lista wartości głośności
    volumes = []

    for track in mp3_files:
        song = AudioSegment.from_file(track, format="mp3", ffmpeg_path=ffmpeg_path)
        
        # dodanie wartości głośności do listy przed normalizacją
        print(f'Glosnosc przed: {song.dBFS}')
        volumes.append(song.dBFS)

    # obliczenie minimalnej, maksymalnej i średniej wartości głośności po normalizacji
    min_volume = min(volumes)
    max_volume = max(volumes)
    avg_volume = sum(volumes) / len(volumes)


    print(f"Minimalna wartość głośności przed normalizacją:", min_volume)
    print(f"Maksymalna wartość głośności przed normalizacją:", max_volume)
    print(f"Średnia wartość głośności dla {len(volumes)} przed normalizacją:", avg_volume)  

    return avg_volume



# przykładowe użycie
mp3_dir = input("Podaj ścieżkę do folderu z plikami mp3: ")


# zapisanie czasu początkowego
start_time = datetime.now()

mp3_files = [os.path.join(mp3_dir, f) for f in os.listdir(mp3_dir) if f.lower().endswith('.mp3')]

ilosc_utworow = len(mp3_files)
# średnia wartość głośności zestawu utworów:
avg_volume_value = avg_volume(mp3_files)

print(f'\n###############################\n')

normalize_volume(mp3_files, avg_volume_value)

# zapisanie czasu końcowego
end_time = datetime.now()

# obliczenie czasu działania programu
operation_time = end_time - start_time

total_seconds = operation_time.total_seconds()

# obliczenie godzin, minut i sekund
hours, remainder = divmod(total_seconds, 3600)
minutes, seconds = divmod(remainder, 60)

# wyświetlenie czasu w formacie hh:mm:ss
print(f"Czas działania programu dla {ilosc_utworow} utworów: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")


print(f'\n###############################\n')
