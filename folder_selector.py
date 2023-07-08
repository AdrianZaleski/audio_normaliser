"""
Moduł: folder_selector

Moduł służący do wybierania plików mp3 wraz z własnym menu wyboru:
-  pojedynczych plików,
- kilku plików,
- pojedynczego folderu
- pojedynczego folderu wraz z jego podfolderami.

"""
import os
import shutil
import sys


def select_single_file() -> list:
    """Funkcja do wyboru pojedynczego pliku mp3 z dokłej lokalizacji tego pliku

    Returns:
        list: lista jednoelementow ze ścieżką do pliku mp3
    """

    file_list = []
    file_path = input("Podaj dokładną ścieżkę do pliku: ")
    if (
        os.path.isfile(file_path)
        and file_path.lower().endswith(".mp3")
        and os.path.getsize(file_path) > 0
    ):
        file_list.append(file_path)
    else:
        print("Podana ścieżka nie prowadzi do pliku.")

    return file_list


def create_file_list():
    file_list = []

    while True:
        file_path = input("Podaj ścieżkę do pliku (lub wpisz 'q' aby zakończyć): ")
        if file_path == "q":
            break
        elif (
            os.path.isfile(file_path)
            and file_path.lower().endswith(".mp3")
            and os.path.getsize(file_path) > 0
        ):
            file_list.append(file_path)
        else:
            print("Podana ścieżka nie prowadzi do pliku.")
    return file_list


def select_single_folder():
    file_list = []
    folder_path = input("Podaj ścieżkę do folderu: ")
    if os.path.isdir(folder_path):
        file_list = [
            os.path.join(folder_path, file)
            for file in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, file))
            and file.lower().endswith(".mp3")
            and os.path.getsize(os.path.join(folder_path, file)) > 0
        ]

    else:
        print("Podana ścieżka nie prowadzi do folderu z utworami mp3.")

    return file_list


def select_folder_and_subfolders() -> list:
    file_list = []
    folder_path = input("Podaj ścieżkę do folderu: ")
    if os.path.isdir(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if (
                    file.lower().endswith(".mp3")
                    and os.path.getsize(os.path.join(root, file)) > 0
                ):
                    file_list.append(os.path.join(root, file))
    else:
        print("Podana ścieżka nie prowadzi do folderu.")

    return file_list


def menu():
    while True:
        print("1. Wybór pojedynczego pliku")
        print("2. Utworzenie listy pojedynczych plików")
        print("3. Wybór pojedynczego folderu (bez podfolderów)")
        print("4. Wybór folderu i wszystkich podfolderów")

        option = input("Wybierz opcję (1-4): ")

        if option == "1":
            file_list = select_single_file()
        elif option == "2":
            file_list = create_file_list()
        elif option == "3":
            file_list = select_single_folder()
        elif option == "4":
            file_list = select_folder_and_subfolders()
        elif option == "0":
            print("Koniec programu")
            sys.exit(0)
        else:
            print("Nieprawidłowa opcja. Wybierz ponownie")


# TODO: Wstępna przymiarka do metody zapisywania plików:
# Metoda zapisywania plików:
def save_normalized_file(file_path, output_folder=None, overwrite=False):
    # Pobranie nazwy pliku
    file_name = os.path.basename(file_path)

    # Ustalenie folderu docelowego
    if output_folder is None:
        # Zapis do folderu, w którym znajduje się oryginalny plik
        output_folder = os.path.dirname(file_path)

        # Utworzenie folderu 'normalized' w folderze docelowym
        output_folder = os.path.join(output_folder, "normalized")
        os.makedirs(output_folder, exist_ok=True)
    else:
        # Utworzenie folderu docelowego, jeśli nie istnieje
        os.makedirs(output_folder, exist_ok=True)

    # Utworzenie ścieżki pliku docelowego
    output_file = os.path.join(output_folder, file_name)

    # Sprawdzenie, czy plik docelowy już istnieje i czy ma być nadpisany
    if os.path.isfile(output_file) and not overwrite:
        print("Plik docelowy już istnieje. Ustaw `overwrite=True`, aby go nadpisać.")
        return

    # Kopia pliku po normalizacji do pliku docelowego
    shutil.copyfile(file_path, output_file)

    print("Plik został zapisany:", output_file)


# Zapisanie w folderze wybranym przez użytkownika
def save_in_user_folder():
    # pobranie od użytkonika lokalizacji zapisu plików:
    user_output_folder_path = input("Podaj gdzie zapisać pliki: ")

    if os.path.isdir(user_output_folder_path):
        result = user_output_folder_path
    elif user_output_folder_path == "exit":
        result = None
    else:
        print("Podana ścieżka nie jest poprawna dla folderów.")
        print("Nie zapisujemy w lokalizacji uzytkownika.")
        result = None

    return result


# Sprawdzenie czy folder docelowy nie jest taki sam jak pliku:
# if user_output_folder_path != os.path.dirname(file_path):
#     print("Wykorzystamy lokalizacje uzytkownika")
# else:
#     print("Podana jest ta sama lokalizacja.")
