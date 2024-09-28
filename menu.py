import os
from subprocess import call
from replit import clear
from termcolor import colored
import time


def main():
    token_file = 'token.txt'
    join = colored('[1]', 'light_magenta')
    spammer = colored('[2]', 'light_magenta')
    thread_spammer = colored('[3]', 'light_magenta')
    checker = colored('[4]', 'light_magenta')
    X = colored('[X]', 'red')
    T = colored('[T]', 'light_magenta')
    menu_color = colored('[/] Menu >> ', 'light_magenta')
    spam_color = colored('[/] Spammer >> ', 'light_magenta')
    debug_color = colored('[/] Debug >> ', 'light_magenta')

    os.system('title Discord Multitool')

    clear()
    
    def run_file(filename):
        call(['python', filename + ".py"])

    # Load the saved token or ask for a new one
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            token_path = f.read().strip()
    else:
        # If no token file exists, ask for a new token and save it
        token_path = input("[/] Menu >> Enter token: ")
        with open(token_file, 'w') as f:
            f.write(token_path)


    menu = f"""
        │━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
        │                                                               {X} Quit    │
        │                              {join} Join                         {T} Token   │
        │                              {spammer} Spammer                                  │
        │                              {thread_spammer} Thread Spammer                           │
        │                              {checker} Checker[WIP]                             │
        |                                                                           |
        │━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
        """

    print(menu)

    choice = input(f"{menu_color}Choose an option: ")

    if choice == '1':
        print("Not safe for now")
        time.sleep(1)
        main()

    elif choice == '2':
        run_file("spammer")
    elif choice.lower == 't':
        # Let the user enter a new token and save it
        token_path = input(f"{menu_color}Enter new token: ")
        with open(token_file, 'w') as f:
            f.write(token_path)
        print(f"{menu_color}New token saved.")
        token_choice = input(f"{menu_color}[E]xit or [P]rint: ")
        if token_choice.lower() == 'p':
            with open(token_path, 'r') as f:
                print(f"{menu_color}Token: \n{f.read().strip()}")
                cont = input(f"{menu_color}[C]ontinue/[E]xit: ")
                if cont.lower() == 'c':
                    time.sleep(2)
                    main()
                elif cont.lower() == 'e':
                    print(f"{menu_color}Exiting...")
                    time.sleep(2)
                    exit()
        elif token_choice.lower() == 'e':
            time.sleep(2)
            main()
    elif choice.lower() == 'x':
        print("Exiting...")
        exit()
    elif choice == '1':
        print("Not safe for now")
        time.sleep(1)
        main()
    elif choice == '3':
        run_file("thread")

    elif choice == '4':
        run_file("checker")
    else:
        print("Invalid choice")

        

if __name__ == "__main__":
    main()
