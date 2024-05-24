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
from modules.utils import Utils
from modules.logging import Log
from modules.captcha import Captcha
from modules.extra import UI



class Discord:
    global unlocked
    global locked
    global st
    def __init__(self) -> None:
        self.data = configuration
        self.proxy = random.choice(loaded_proxies)

        self.ua_version = ua_version
        self.ua = ua
        self.sec_ch_ua = sec_ch_ua

        self.session = tls_client.Session(client_identifier=f"chrome_{self.ua_version}", random_tls_extension_order=True)
        self.session.proxies = {
            'https': "http://{}".format(self.proxy),
            'http': "http://{}".format(self.proxy)
        }
        self.ws = WebSocket()

        self.bios = loaded_bios if self.data['bio'] else []
        self.cap_key = self.data['captcha_api_key']
        self.toggle_errors = self.data['show_errors']
        
        self.lock = threading_lock
        self.capabilities = 16381
        self.build_num = build_num
        self.x_sup = x_sup

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
        if self.data['password'] == "":
            self.password = "".join(random.choice(string.digits) if random.randint(1, 2) == 1 else random.choice(string.ascii_letters) for x in range(random.randint(8, 24))) + "".join("" if random.randint(1, 2) == 1 else random.choice(["@", "$", "%", "*", "&", "^"]) for x in range(1, 6))
        else:   self.password = self.data['password']

    @staticmethod
    def display_stats():
        while True:
            if locked == 0 and unlocked == 0:
                ur = "0.00%"
            elif unlocked > 0 and locked == 0:
                ur = "100.0%"
            elif locked > 0 and unlocked == 0:
                ur = "0.00%"
            else:
                ur = f"{round(100 - round(locked/unlocked * 100, 2), 2)}%"
            ctypes.windll.kernel32.SetConsoleTitleW(f"[GITHUB] Pr0t0n's Generator | Unlocked: {unlocked} | Locked: {locked} | Unlock Rate: {ur} | Threads: {threading.active_count() - 2} | Time: {round(time.time() - st, 2)}s | github.com/pr0t0ns")
            time.sleep(0.5)

    def get_cookies(self):
        url = "https://discord.com/register"
        self.session.headers = {
            'authority': 'discord.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': self.sec_ch_ua,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.ua,
        }
        try:
            self.session.cookies = self.session.get(url).cookies
        except Exception:
            Log.bad('Error Fetching Cookies')
            return Discord().begin()
        return
    
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
                        "browser_user_agent": self.ua,
                        "browser_version": f"{self.ua_version}.0.0.0",
                        "os_version": "10",
                        "referrer": "",
                        "referring_domain": "",
                        "referrer_current": "",
                        "referring_domain_current": "",
                        "release_channel": "stable",
                        "client_build_number": build_num,
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
        self.session.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://discord.com/register',
            'sec-ch-ua': self.sec_ch_ua,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.ua,
            'x-context-properties': Utils.build_x_context_properties("Register"),
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'America/New_York',
            'x-super-properties': self.x_sup,
        }
        try:
            r = self.session.get(url)
            return r.json()['fingerprint']
        except:
            Log.bad("Error Fetching Fingerprint")
            return Discord().begin()

    def create_acct(self):
        url = 'https://discord.com/api/v9/auth/register'
        self.display_name = self.username
        self.session.headers = {
                'authority': 'discord.com',
                'accept': '*/*',
                "accept-encoding": "gzip, deflate, br",
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'content-type': 'application/json',
                'origin': 'https://discord.com',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://discord.com/register',
                'sec-ch-ua': self.sec_ch_ua,
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': self.ua,
                'x-captcha-key': str(Captcha.solve(user_agent=self.ua, api_key=self.data['captcha_api_key'], proxy=self.session.proxies['http'], service=self.data['captcha_service'])),
                'x-debug-options': 'bugReporterEnabled',
                'x-discord-locale': 'en-US',
                'x-discord-timezone': 'America/New_York',
                'x-fingerprint': self.fp,
                'x-super-properties': self.x_sup,
        }
        payload = {
                'fingerprint': self.fp,
                'email': self.email,
                'username': self.username + "".join(random.choice(string.ascii_letters) for x in range(random.randint(1, 3))),
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
            print(r.json())
            Log.bad("Error Creating Account!")
            return Discord().begin()
        
        self.session.headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'sec-ch-ua': self.sec_ch_ua,
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.ua,
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'America/New_York',
            'x-super-properties': self.x_sup,
        }
        self.ConnectWS()
        res = self.check_token()
        if res:
            if True:
                with open("./output/tokens.txt", 'a+') as f:
                    self.lock.acquire(blocking=True)
                    f.write(f"{self.email}:{self.password}:{self.token}\n")
                    self.lock.release()
        return
    
    def begin(self):
        self.get_cookies()
        self.fp = self.get_fingerprint()
        self.create_acct()
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
    ua = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ua_version}.0.0.0 Safari/537.36'
    sec_ch_ua = f'"Chromium";v="{ua_version}", "Google Chrome";v="{ua_version}", "Not-A.Brand";v="99"'

    # XSUP, BUILDNUM, ETC..
    build_num = Utils.fetch_buildnum()
    x_sup = Utils.build_xsup(ua, ua_version, build_num)

    UI.show()
    thds = int(input("Threads: "))
    UI.clear()
    st = time.time()
    for i in range(thds):
        discord = Discord()
        threading.Thread(target=discord.begin).start()

