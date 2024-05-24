import json, time, base64, requests, re
from datetime import datetime


# Im revamping all this shitty old code soon no worries
class Utils:
    @staticmethod
    def fetch_buildnum() -> int: # gotta fix too lazy tho
        try:
            asset_files = re.findall(r'<script\s+src="([^"]+\.js)"\s+defer>\s*</script>', requests.get("https://discord.com/login").text)
            for js_endpoint in asset_files:
                resp = requests.get(f"https://discord.com/{js_endpoint}")
                try:
                    build_number = resp.text.split('"buildNumber",(_="')[1].split('"')[0]
                    break
                except:
                    pass
            return build_number
        except:
            return 295805

    @staticmethod
    def build_x_context_properties(location: str) -> str:
        return base64.b64encode(json.dumps({"location":location}).replace("'", '"').replace(" ", "").encode()).decode()

    @staticmethod
    def nonce() -> str:
        return str((int(time.mktime(datetime.now().timetuple()))*1000-1420070400000)*4194304)

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
        data = json.dumps(data, separators=(":", ","))
        return base64.b64encode(str(data).replace("'", '"').replace('": "', '":"').replace('", "', '","').replace('number": ', 'number":').replace(', "client', ',"client').replace('source": ', 'source":').encode()).decode()
        
    @staticmethod
    def JS_version():
        pass # Gotta finish