def display_menu(title, options):
    print(title)
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")


def get_user_choice(num_options):
    while True:
        choice = input("Wybierz opcję: ")
        if choice.isdigit() and 1 <= int(choice) <= num_options:
            return int(choice)
        else:
            print("Nieprawidłowa opcja. Wybierz ponownie.")
