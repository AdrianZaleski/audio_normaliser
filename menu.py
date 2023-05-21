"""
Moduł wyświetlania głównego menu z obsługą interfejsu użytkownika. 

"""
import sys
from audio_normaliser import (
    calculate_average_volume_from_list,
)
from folder_selector import (
    create_file_list,
    select_folder_and_subfolders,
    select_single_file,
    select_single_folder,
)
from menu_utils import display_menu, get_user_choice


def main_menu():
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
            print(f"lista_utworow: {lista_utworow}")
            conversion_menu()
        elif choice == 2:
            # Obsługa utworzenia listy plików
            lista_utworow = create_file_list()
            print(f"lista_utworow: {lista_utworow}")
            conversion_menu(lista_utworow)
        elif choice == 3:
            # Obsługa wyboru folderu
            lista_utworow = select_single_folder()
            print(f"lista_utworow: {lista_utworow}")
            conversion_menu(lista_utworow)
        elif choice == 4:
            # Obsługa wyboru folderu
            lista_utworow = select_folder_and_subfolders()
            print(f"lista_utworow: {lista_utworow}")

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
            # Otwieranie pliku do odczytu
            with open("target_volume.txt", "r") as file:
                # Odczyt zawartości pliku
                glosnosc_z_pliku = file.read()
            print(f"wartosc glosnosci z pliku: {glosnosc_z_pliku}")
            pass
        elif choice == 2:
            # Normalizacja głośności do średniej wartości z listy plików
            srednia_wartosc = calculate_average_volume_from_list(songs_list)
            print(f"srednia wartosc: {srednia_wartosc}")
            pass
        elif choice == 3:
            break
        elif choice == 4:
            print("Koniec programu.")
            sys.exit()


if __name__ == "__main__":
    main_menu()
