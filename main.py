import tls_client
import random
import string
import time
import re
import threading
import json
import colorama
import ctypes
from websocket   import WebSocket
from modules.headers import Headers
from modules.utils import Utils
from modules.logging import Log
from modules.captcha import Captcha
from modules.extra import UI


class Discord:
    global unlocked
    global locked
    global start_time
    
    def __init__(self) -> None:
        self.data = configuration
        self.proxy = random.choice(loaded_proxies)

        self.ua_version = ua_version
        self.user_agent = user_agent
        self.sec_ch_ua = sec_ch_ua

        self.session = tls_client.Session(client_identifier=f"chrome_{self.ua_version}", random_tls_extension_order=True)

        proxy = "http://{}".format(self.proxy)
        self.session.proxies = {
            'http'  : proxy,
            'https' : proxy
        }

        self.ws = WebSocket()

        self.bios = loaded_bios if self.data['bio'] else []
        self.cap_key = self.data['captcha_api_key']
        self.toggle_errors = self.data['show_errors']
        
        self.lock = threading_lock
        self.capabilities = 16381
        self.build_num = build_number
        self.x_super_properties = x_super_properties

        self.rl = "The resource is being rate limited."
        self.locked = "You need to verify your account in order to perform this action"
        self.captcha_detected = "captcha-required"

        
        if self.data['random_username']:
            self.username = "".join(random.choice(string.ascii_letters) for x in range(random.randint(6, 8)))
        else:
            self.username = random.choice(loaded_usernames)


        self.email = "".join(random.choice(string.ascii_letters) for x in range(random.randint(6, 8)))
        self.email += str("".join(str(random.randint(1, 9) if random.randint(1, 2) == 1 else random.choice(string.ascii_letters)) for x in range(int(random.randint(6, 8)))))
        self.email += random.choice(["@gmail.com", "@outlook.com"])
        if self.data['password'] == "" :
            self.password = "".join(random.choice(string.digits) if random.randint(1, 2) == 1 else random.choice(string.ascii_letters) for x in range(random.randint(8, 24))) + "".join("" if random.randint(1, 2) == 1 else random.choice(["@", "$", "%", "*", "&", "^"]) for x in range(1, 6))
        else : self.password = self.data['password']

    @staticmethod
    def display_stats():
        while True:
            if locked == 0 and unlocked == 0:
                unlock_rate = "0.00%"
            elif unlocked > 0 and locked == 0:
                unlock_rate = "100.0%"
            elif locked > 0 and unlocked == 0:
                unlock_rate = "0.00%"
            else:
                unlock_rate = f"{round(100 - round(locked/unlocked * 100, 2), 2)}%"
            ctypes.windll.kernel32.SetConsoleTitleW(f"[GITHUB] Pr0t0n's Generator | Unlocked: {unlocked} | Locked: {locked} | Unlock Rate: {unlock_rate} | Threads: {threading.active_count() - 2} | Time: {round(time.time() - start_time, 2)}s | github.com/pr0t0ns")
            time.sleep(0.5)

    def get_cookies(self):
        url = "https://discord.com/register"
        headers = Headers.get_cookies
        headers['sec-ch-ua'] = self.sec_ch_ua
        headers['user-agent'] = self.user_agent
        self.session.headers = headers

        try:
            self.session.cookies = self.session.get(url).cookies
        except Exception:
            Log.bad('Error Fetching Cookies')
            return Discord().begin()
        return True
    
    def check_token(self):
        global unlocked, locked
        url = "https://discord.com/api/v9/users/@me/affinities/users"
        try:
            response = self.session.get(url)
        except:
            Log.bad("Error Sending Requests to check token")
            return Discord().begin()
        if int(response.status_code) in (400, 401, 403):
            Log.bad(f"Locked Token ({colorama.Fore.RED}{self.token[:25]}..{colorama.Fore.RESET})")
            locked += 1
            return
        else:
            Log.amazing(f"Unlocked Token ({colorama.Fore.LIGHTBLACK_EX}{self.token[:25]}..{colorama.Fore.RESET})")    
            unlocked += 1
            return True
        
    def ConnectWS(self):
        try:
            self.ws.connect('wss://gateway.discord.gg/?encoding=json&v=9&compress=zlib-stream')
            self.ws.send(json.dumps({
                "op": 2,
                "d": {
                    "token": self.token,
                    "capabilities": self.capabilities,
                    "properties": {
                        "os": "Windows",
                        "browser": "Chrome",
                        "device": "",
                        "system_locale": "en-US",
                        "browser_user_agent": self.user_agent,
                        "browser_version": f"{self.ua_version}.0.0.0",
                        "os_version": "10",
                        "referrer": "",
                        "referring_domain": "",
                        "referrer_current": "",
                        "referring_domain_current": "",
                        "release_channel": "stable",
                        "client_build_number": build_number,
                        "client_event_source": None
                    },
                        "presence": {
                        "status": random.choice(['online', 'idle', 'dnd']),
                        "since": 0,
                        "activities": [],
                        "afk": False
                    },
                    "compress": False,
                    "client_state": {
                        "guild_versions": {},
                        "highest_last_message_id": "0",
                        "read_state_version": 0,
                        "user_guild_settings_version": -1,
                        "user_settings_version": -1,
                        "private_channels_version": "0",
                        "api_code_version": 0
                    }
                }
            }))
        except:
            Log.bad("Error Onlining Token")
            return
        Log.good(f"Onlined Token --> ({colorama.Fore.LIGHTBLACK_EX}{self.token[:20]}..{colorama.Fore.RESET})", symbol="O")
        return
    
    
    def get_fingerprint(self):
        url = 'https://discord.com/api/v9/experiments?with_guild_experiments=true'
        headers = Headers.get_fingerprint
        headers['sec-ch-ua'] = self.sec_ch_ua
        headers['user-agent'] = self.user_agent
        headers['x-context-properties'] =  Utils.build_x_context_properties("Register")
        headers['x-super-properties'] = self.x_super_properties
        self.session.headers = headers

        try:
            r = self.session.get(url)
            return r.json()['fingerprint']
        except:
            Log.bad("Error Fetching Fingerprint")
            return Discord().begin()

    def create_account(self):
        # Create Account
        url = 'https://discord.com/api/v9/auth/register'

        captcha_key = str(Captcha.solve(
            user_agent=self.user_agent, 
            api_key=self.data['captcha_api_key'], 
            proxy=self.session.proxies['http'], 
            service=self.data['captcha_service']
        ))
        headers = Headers.register
        headers['sec-ch-ua'] = self.sec_ch_ua
        headers['user-agent'] = self.user_agent
        headers['x-captcha-key'] = captcha_key
        headers['x-super-properties'] = self.x_super_properties
        self.session.headers = headers

        self.display_name = self.username
        payload = {
            'fingerprint': self.fingerprint,
            'email': self.email,
            'username': self.username + "".join(random.choice(string.ascii_letters) for _ in range(random.randint(1, 3))),
            'global_name': self.display_name,
            'password': self.password,
            'invite': self.data["invite"] if self.data["invite"] != None else None,
            'consent': True,
            'date_of_birth': f'{random.randint(1980, 2001)}-{random.randint(1, 10)}-{random.randint(1, 10)}',
            'gift_code_sku_id': None
        }
        try:
            r = self.session.post(url, json=payload)
            self.token = r.json()['token']
        except Exception:
            Log.bad("Error Creating Account!")
            return Discord().begin()
        

        # Connect to websocket and check token
        headers = Headers.check_token
        headers['authorization'] = self.token
        headers['sec-ch-ua'] = self.sec_ch_ua
        headers['user-agent'] = self.user_agent
        headers["x-super-properties"] = self.x_super_properties
        self.session.headers = headers

        self.ConnectWS()
        res = self.check_token()
        if res:
            if True: # changed
                with open("./output/tokens.txt", 'a+') as f:
                    self.lock.acquire(blocking=True)
                    f.write(f"{self.email}:{self.password}:{self.token}\n")
                    self.lock.release()
        return
    
    def begin(self):
        self.get_cookies()
        self.fingerprint = self.get_fingerprint()
        self.create_account()
        return Discord().begin()

class load_files:
    
    @staticmethod
    def load_txt() -> list:
        formatted_usrs = [] 
        loaded_proxies = [prox.strip() for prox in open('./input/proxies.txt', encoding="utf-8")]
        loaded_bios = [bio.strip() for bio in open("./input/bios.txt", encoding="utf-8")]
        loaded_usernames = [usr.strip() for usr in open('./input/usernames.txt', encoding="utf-8")]
        for usr in loaded_usernames:
            formatted_usrs.append(re.sub(r'[^a-zA-Z0-9 \n\.]', '', usr).replace(" ", "")) # Try to get rid of malformatted usernames for discord
        return loaded_proxies, loaded_bios, formatted_usrs

    @staticmethod
    def load_config():
        global license_key

        with open("config.json") as f:
            data = json.load(f)
        return data

if __name__ == "__main__":
    unlocked = 0
    locked = 0

    # Initalize
    colorama.init(autoreset=True)
    threading_lock = threading.Lock()
    configuration = load_files.load_config()
    loaded_proxies, loaded_bios, loaded_usernames = load_files.load_txt()

    # User Agent Information
    ua_version = "124"
    user_agent = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ua_version}.0.0.0 Safari/537.36'
    sec_ch_ua = f'"Chromium";v="{ua_version}", "Google Chrome";v="{ua_version}", "Not-A.Brand";v="99"'

    # XSUP, BUILDNUM, ETC..
    build_number = Utils.fetch_buildnum()
    x_super_properties = Utils.build_xsp(user_agent, ua_version, build_number)

    UI.show()
    try:
        threads = int(input("Threads: "))
    except:
        Log.warn("Invalid input!")
        exit(0)
        
    UI.clear()
    start_time = time.time()
    for i in range(threads):
        discord = Discord()
        threading.Thread(target=discord.begin).start()


    #if configuration['display_title']:
    #    Ds = Discord()
    #    threading.Thread(target=Ds.display_stats).start()
