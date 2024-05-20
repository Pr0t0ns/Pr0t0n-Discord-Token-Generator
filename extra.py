import platform, sys, os, shutil, random
import colorama
class UI:

    def clear(title: str=None): # Taken from Keyauth to clear UI
        if platform.system() == 'Windows':
            os.system(f'cls {title if title != None else ""}')  # clear console, change title
        elif platform.system() == 'Linux':
            os.system('clear')  # clear console
            if title != None:
                sys.stdout.write(f"\x1b]0;{title}\x07")  # change title
        elif platform.system() == 'Darwin':
            os.system("clear && printf '\e[3J'")  # clear console
            if title != None:
                os.system(f'''echo - n - e "\033]0;{title}\007"''')  # change title
    
    def show():
            colorama.init(autoreset=True)
            logo_text = """
            ██████╗ ██████╗  ██████╗ ████████╗ ██████╗ ███╗   ██╗     ██████╗ ███████╗███╗   ██╗
            ██╔══██╗██╔══██╗██╔═████╗╚══██╔══╝██╔═████╗████╗  ██║    ██╔════╝ ██╔════╝████╗  ██║
            ██████╔╝██████╔╝██║██╔██║   ██║   ██║██╔██║██╔██╗ ██║    ██║  ███╗█████╗  ██╔██╗ ██║
            ██╔═══╝ ██╔══██╗████╔╝██║   ██║   ████╔╝██║██║╚██╗██║    ██║   ██║██╔══╝  ██║╚██╗██║
            ██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║ ╚████║    ╚██████╔╝███████╗██║ ╚████║
            ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═══╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝
            """
            print("")
            logo_lines = logo_text.split('\n')
            console_width = shutil.get_terminal_size().columns # Used Chatgpt im sorry im not writing UI from scratch
            colorz = [
                colorama.Fore.RED, colorama.Fore.LIGHTRED_EX, colorama.Fore.LIGHTMAGENTA_EX, colorama.Fore.MAGENTA,
                colorama.Fore.BLUE, colorama.Fore.LIGHTBLUE_EX, colorama.Fore.CYAN, colorama.Fore.LIGHTCYAN_EX,
                colorama.Fore.LIGHTGREEN_EX, colorama.Fore.GREEN, colorama.Fore.BLACK, colorama.Fore.LIGHTBLACK_EX
            ]
            for i, line in enumerate(logo_lines):
                gradient_color = random.choice(colorz)
                centered_line = line.center(console_width)
                print(gradient_color + centered_line) 
            print("")
            print(f"{colorama.Fore.WHITE}Menu\n")
            print(f"[{colorama.Fore.BLUE}1{colorama.Fore.RESET}] - Start ")
            print(f"[{colorama.Fore.RED}2{colorama.Fore.RESET}] - Exit")
            choice = input(f"{colorama.Fore.BLUE}|> {colorama.Fore.WHITE}")
            UI.clear()
            if choice != "1":
                os._exit(1)