"""
Moduł: folder_selector

Moduł służący do wybierania plików mp3 wraz z własnym menu wyboru:
-  pojedynczych plików,
- kilku plików,
- pojedynczego folderu
- pojedynczego folderu wraz z jego podfolderami.

"""
import os
import sys


def select_single_file():
    file_list = []
    file_path = input("Podaj dokładną ścieżkę do pliku: ")
    if os.path.isfile(file_path) and file_path.lower().endswith(".mp3"):
        file_list.append(file_path)
    else:
        print("Podana ścieżka nie prowadzi do pliku.")
        file_list = []

    return file_list


def create_file_list():
    file_list = []
    while True:
        file_path = input("Podaj ścieżkę do pliku (lub wpisz 'q' aby zakończyć): ")
        if file_path == "q":
            break
        elif os.path.isfile(file_path) and file_path.lower().endswith(".mp3"):
            file_list.append(file_path)
        else:
            print("Podana ścieżka nie prowadzi do pliku.")
    return file_list


def select_single_folder():
    folder_path = input("Podaj ścieżkę do folderu: ")
    if os.path.isdir(folder_path):
        file_list = [
            os.path.join(folder_path, file)
            for file in os.listdir(folder_path)
            if os.path.isfile(
                os.path.join(folder_path, file) and file.lower().endswith(".mp3")
            )
        ]

        return file_list
    else:
        print("Podana ścieżka nie prowadzi do folderu.")
        return []


def select_folder_and_subfolders():
    folder_path = input("Podaj ścieżkę do folderu: ")
    if os.path.isdir(folder_path):
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(".mp3"):
                    file_list.append(os.path.join(root, file))
        return file_list
    else:
        print("Podana ścieżka nie prowadzi do folderu.")
        return []


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

    # print("Lista plików:")
    # for file in file_list:
    #     print(file)


if __name__ == "__main__":
    menu()
