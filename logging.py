import colorama, threading
from datetime import datetime



class Log:
    colorama.init(autoreset=True)
    
    def amazing(msg: str, symbol="U", lock=threading.Lock()):
        lock.acquire(blocking=True)
        print(f"[{colorama.Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{colorama.Fore.RESET}] ({colorama.Fore.BLUE}{symbol}{colorama.Fore.RESET}) - {msg}")
        lock.release()
    
    def good(msg: str, symbol="+", lock=threading.Lock()):
        lock.acquire(blocking=True)
        print(f"[{colorama.Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{colorama.Fore.RESET}] ({colorama.Fore.LIGHTBLUE_EX}{symbol}{colorama.Fore.RESET}) - {msg}")
        lock.release()
    
    def info(msg: str, symbol="=", lock=threading.Lock()):
        lock.acquire(blocking=True)
        print(f"[{colorama.Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{colorama.Fore.RESET}] ({colorama.Fore.LIGHTCYAN_EX}{symbol}{colorama.Fore.RESET}) - {msg}")
        lock.release()
    
    def bad(msg: str, symbol="X", lock=threading.Lock()):
        lock.acquire(blocking=True)
        print(f"[{colorama.Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{colorama.Fore.RESET}] ({colorama.Fore.RED}{symbol}{colorama.Fore.RESET}) - {msg}")
        lock.release()

    def warn(msg: str, symbol="!", lock=threading.Lock()):
        lock.acquire(blocking=True)
        print(f"[{colorama.Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{colorama.Fore.RESET}] ({colorama.Fore.YELLOW}{symbol}{colorama.Fore.RESET}) - {msg}")  
        lock.release()

