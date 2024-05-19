import json, time, base64
from datetime import datetime


# Im revamping all this shitty old code soon no worries
class Utils:
    @staticmethod
    def fetch_buildnum() -> int: # gotta fix too lazy tho
            return 294520

    @staticmethod
    def build_x_context_properties(location: str) -> str:
        return base64.b64encode(json.dumps({"location":location}).replace("'", '"').replace(" ", "").encode()).decode()

    @staticmethod
    def nonce():
        date = datetime.now()
        unixts = time.mktime(date.timetuple())
        return str((int(unixts)*1000-1420070400000)*4194304)

    @staticmethod
    def build_xsup(user_agent: str, ua_version: str, bn: int) -> str:
        data = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": user_agent,
            "browser_version": f"{ua_version}.0.0.0",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "https://discord.com/",
            "referring_domain_current": "discord.com",
            "release_channel": "stable",
            "client_build_number": bn,
            "client_event_source": None,
            "design_id":0
        }
        data = str(data).replace("None", "null")
        return base64.b64encode(str(data).replace("'", '"').replace('": "', '":"').replace('", "', '","').replace('number": ', 'number":').replace(', "client', ',"client').replace('source": ', 'source":').encode()).decode()
        
    @staticmethod
    def JS_version():
        pass # Gotta finish