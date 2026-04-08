def display_help_menu():
    help_menu = ""
    help_menu += "Scrollable Help Menu for Key System\n"
    help_menu += "1. Key Generation\n"
    help_menu += "2. Key Validation\n"
    help_menu += "3. Key Revocation\n"
    help_menu += "4. Key Distribution\n"
    help_menu += "5. Exit\n"
    return help_menu

if __name__ == '__main__':
    menu = display_help_menu()
    print(menu)
