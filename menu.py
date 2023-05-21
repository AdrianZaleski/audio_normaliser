"""
Moduł wyświetlania głównego menu z obsługą interfejsu użytkownika. 

"""
import sys
from folder_selector import create_file_list, select_folder_and_subfolders, select_single_file, select_single_folder
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
        display_menu(
            "Menu wyboru pliku",
            [
                "Wybór pojedynczego pliku",
                "Utworzenie listy plików",
                "Wybór pojedynczego folderu",
                "Wybór folderu z podfolderami",
                "Wróć do głównego menu",
                "Zakończ program",
            ],
        )
        choice = get_user_choice(6)

        if choice == 1:
            # Obsługa wyboru pojedynczego pliku
            select_single_file()
            conversion_menu()
        elif choice == 2:
            # Obsługa utworzenia listy plików
            create_file_list()
            conversion_menu()
        elif choice == 3:
            # Obsługa wyboru folderu
            select_single_folder()
            conversion_menu()
        elif choice == 4:
            # Obsługa wyboru folderu
            select_folder_and_subfolders()
            conversion_menu()
        elif choice == 5:
            break
        elif choice == 6:
            print("Koniec programu.")
            sys.exit()


def conversion_menu():
    while True:
        display_menu(
            "Menu konwersji pliku",
            [
                "Normalizacja pliku",
                "Konwersja formatu pliku",
                "Wróć do poprzedniego menu",
                "Zakończ program",
            ],
        )
        choice = get_user_choice(4)

        if choice == 1:
            # Obsługa normalizacji pliku
            pass
        elif choice == 2:
            # Obsługa konwersji formatu pliku
            pass
        elif choice == 3:
            break
        elif choice == 4:
            print("Koniec programu.")
            sys.exit()


if __name__ == "__main__":
    main_menu()
