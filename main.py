import os
from datetime import datetime

from audio_normaliser import avg_volume, normalize_volume


# TODO:
# - Zapisanie wartości normalizacji do pliku
# - Opcja do zaczytania wartości z pliku do normalizacji
# - Przerabianie plików wewnątrz podfolderów
# - Dodanie wgrywania oryginalnych metadanych z oryginału do normalizowanego pliku (tytuł, artysta, numer ścieżki itp.)


# przykładowe użycie
mp3_dir = input("Podaj ścieżkę do folderu z plikami mp3: ")


# zapisanie czasu początkowego
start_time = datetime.now()

mp3_files = [
    os.path.join(mp3_dir, f) for f in os.listdir(mp3_dir) if f.lower().endswith(".mp3")
]

ilosc_utworow = len(mp3_files)
# średnia wartość głośności zestawu utworów:
avg_volume_value = avg_volume(mp3_files)

print(f"\n###############################\n")

normalize_volume(mp3_dir, mp3_files, avg_volume_value)

# zapisanie czasu końcowego
end_time = datetime.now()

# obliczenie czasu działania programu
operation_time = end_time - start_time

total_seconds = operation_time.total_seconds()

# obliczenie godzin, minut i sekund
hours, remainder = divmod(total_seconds, 3600)
minutes, seconds = divmod(remainder, 60)

# wyświetlenie czasu w formacie hh:mm:ss
print(
    f"Czas działania programu dla {ilosc_utworow} utworów: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
)


print(f"\n###############################\n")
