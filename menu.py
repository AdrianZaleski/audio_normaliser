"""
Moduł wyświetlania głównego menu z obsługą interfejsu użytkownika. 
Dodatkowo odnosi się do osobnych modułów w których jest wybór folderów i normalizacja utworów

"""
from datetime import datetime
import sys
from audio_normaliser import (
    calculate_average_volume_from_list,
    normalize_volume,
)
from folder_selector import (
    create_file_list,
    select_folder_and_subfolders,
    select_single_file,
    select_single_folder,
)
from menu_utils import display_menu, get_user_choice


def main_menu():
    """
    Wyświetlanie głównego menu, który początkuje cały program.
    """

    while True:
        display_menu("Główne menu", ["Początek działania programu", "Zakończ program"])
        choice = get_user_choice(2)

        if choice == 1:
            file_menu()
        elif choice == 2:
            print("Koniec programu.")
            sys.exit()


def file_menu():
    while True:
        zawartosc_menu = [
            "Wybór pojedynczego pliku",
            "Utworzenie listy plików",
            "Wybór pojedynczego folderu",
            "Wybór folderu z podfolderami",
            "Wróć do głównego menu",
            "Zakończ program",
        ]
        display_menu(
            "Menu wyboru pliku",
            zawartosc_menu,
        )
        choice = get_user_choice(6)

        if choice == 1:
            # Obsługa wyboru pojedynczego pliku
            lista_utworow = select_single_file()
            conversion_menu(lista_utworow)

        elif choice == 2:
            # Obsługa utworzenia listy plików
            lista_utworow = create_file_list()
            conversion_menu(lista_utworow)

        elif choice == 3:
            # Obsługa wyboru folderu
            lista_utworow = select_single_folder()
            conversion_menu(lista_utworow)

        elif choice == 4:
            # Obsługa wyboru folderu i podfolderów
            lista_utworow = select_folder_and_subfolders()
            conversion_menu(lista_utworow)

        elif choice == 5:
            break
        elif choice == 6:
            print("Koniec programu.")
            sys.exit()


def conversion_menu(songs_list: list):
    while True:
        display_menu(
            "Menu konwersji pliku",
            [
                "Normalizacja głośności do wartości z pliku",
                "Normalizacja głośności do średniej wartości",
                "Wróć do poprzedniego menu",
                "Zakończ program",
            ],
        )
        choice = get_user_choice(4)

        if choice == 1:
            # Normalizacja głośności do wartości z pliku

            # zapisanie czasu początkowego
            start_time = datetime.now()

            # Otwieranie pliku do odczytu
            with open("target_volume.txt", "r") as file:
                # Odczyt zawartości pliku
                glosnosc_z_pliku = float(file.read())

            print(f"wartosc glosnosci z pliku: {glosnosc_z_pliku}")

            normalize_volume(songs_list, glosnosc_z_pliku)

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
                f"Czas działania programu dla {len(songs_list)} mp3: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            )

            print(f"\n###############################\n")
        elif choice == 2:
            # zapisanie czasu początkowego
            start_time = datetime.now()

            # Normalizacja głośności do średniej wartości z listy plików
            srednia_wartosc = calculate_average_volume_from_list(songs_list)
            print(f"srednia wartosc: {srednia_wartosc}")

            # Proces normalizacji
            normalize_volume(songs_list, srednia_wartosc)

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
                f"Czas działania programu dla {len(songs_list)} mp3: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            )

            print(f"\n###############################\n")

        elif choice == 3:
            break
        elif choice == 4:
            print("Koniec programu.")
            sys.exit()
