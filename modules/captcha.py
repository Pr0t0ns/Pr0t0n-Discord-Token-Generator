import requests
import time
from .logging import Log
import colorama

class Captcha:
    @staticmethod
    def solve(user_agent: str, api_key:str, proxy: str, service: str='capmonster', site_key: str="4c672d35-0701-42b2-88c3-78380b0db560", rq_data: str=None, max_retries: int=150) -> str|bool:
        headers = {'user-agent': "Mozilla"}
        
        services = {
            "capmonster": {
                "url": 'https://api.capmonster.cloud',
                "payload": {
                    "clientKey": api_key,
                    "task": {
                        "type": "HCaptchaTaskProxyless",
                        "websiteURL": "https://discord.com/",
                        "websiteKey": site_key,
                        "userAgent": user_agent,
                    }
                },
                "custom": False
            },
            "capsolver": {
                "url": "https://api.capsolver.com",
                "payload": {
                    "clientKey": api_key,
                    "task": {
                        "type": "HCaptchaTurboTask",
                        "websiteURL": "https://discord.com/",
                        "websiteKey": site_key,
                        "proxy": proxy,
                        "userAgent": user_agent
                    }
                },
                "custom": False
            },
            "hcoptcha": {
                "url": "https://api.hcoptcha.online/api",
                "payload": {
                    "api_key": api_key,
                    "task_type": "hcaptchaEnterprise",
                    "data": {
                        "sitekey": site_key,
                        "proxy": proxy,
                        "host": "discord.com"
                    }
                },
                "custom": False
            },
            "24captcha": {
                "url": "https://24captcha.online/in.php",
                "payload": {
                    "key": api_key,
                    "sitekey": site_key,
                    "pageurl": "https://discord.com/register",
                    "proxy": proxy,
                    "json": 0
                },
                "custom": True
            },
            "fcaptcha": {
                "url": 'https://api.fcaptcha.lol/api/createTask',
                "headers": {"authorization": api_key},
                "payload": {
                    "sitekey": site_key,
                    "host": "https://discord.com",
                    "proxy": proxy,
                    "user_agent": user_agent
                },
                "custom": True
            },
            "2captcha": {
                "url": "https://api.2captcha.com",
                "payload": {
                    "clientKey": api_key,
                    "task": {
                        "type": "HCaptchaTaskProxyless",
                        "websiteURL": "https://discord.com/register",
                        "websiteKey": site_key
                    }
                },
                "custom": False
            },
            "anticaptcha": {
                "url": "https://api.anti-captcha.com",
                "payload": {
                    "clientKey": api_key,
                    "task": {
                        "type": "HCaptchaTaskProxyless",
                        "websiteURL": "https://discord.com/register",
                        "websiteKey": site_key,
                        "isInvisible": False
                    },
                    "softId": 0
                },
                "custom": False
            }
        }

        if service not in services:
            Log.bad(f"{service} Is Not Supported")
            return None

        config = services[service]
        url = config["url"]
        payload = config["payload"]
        headers = config.get("headers", headers)
        custom = config["custom"]

        try:
            if custom:
                r = requests.post(url, headers=headers, json=payload)
            else:
                r = requests.post(f"{url}/createTask", headers=headers, json=payload)
        except Exception:
            Log.bad(f"Error Creating {service} Task")
            return None

        try:
            if service in ['hcoptcha', '24captcha', 'fcaptcha']:
                if service == "24captcha":
                    try:
                        taskid = r.text.split("|")[1]
                    except Exception:
                        Log.bad("Error getting captcha task id")
                        return None
                elif service == 'fcaptcha':
                    taskid = r.json().get('task', {}).get('task_id')
                else:
                    taskid = r.json().get("task_id")
            else:
                taskid = r.json().get("taskId")
            
            if not taskid:
                Log.bad("Error getting captcha task id")
                return None
        except Exception:
            Log.bad("Error getting captcha task id")
            return None

        for i in range(max_retries):
            try:
                if service in ['hcoptcha', '24captcha', 'fcaptcha']:
                    if service == "24captcha":
                        payload = {"key": api_key, "id": taskid, "action": "get", "json": 1}
                        r = requests.post("https://24captcha.online/res.php", json=payload).json()
                        if r.get('status') == 1:
                            cap_pri = r["request"][:35]
                            Log.good(f"Solved captcha ({colorama.Fore.LIGHTBLACK_EX}{cap_pri}..{colorama.Fore.RESET})")
                            return r["request"]
                    elif service == "fcaptcha":
                        r = requests.post(f"https://api.fcaptcha.lol/api/getTaskData", headers=headers, json={"task_id": taskid})
                        if r.json().get('task', {}).get('state') == "completed":
                            cap_pri = r.json()["task"]["captcha_key"][:35]
                            Log.good(f"Solved captcha ({colorama.Fore.LIGHTBLACK_EX}{cap_pri}..{colorama.Fore.RESET})")
                            return r.json()["task"]["captcha_key"]
                    else:
                        r = requests.post(f"{url}/getTaskData", json={"api_key": api_key, "task_id": taskid})
                        if r.json().get('task', {}).get('state') == "completed":
                            cap_pri = r.json()["task"]["captcha_key"][:35]
                            Log.good(f"Solved captcha ({colorama.Fore.LIGHTBLACK_EX}{cap_pri}..{colorama.Fore.RESET})")
                            return r.json()["task"]["captcha_key"]
                else:
                    r = requests.post(f"{url}/getTaskResult", json={"clientKey": api_key, "taskId": taskid})
                    if r.json().get("status") == "ready":
                        cap_pri = r.json()["solution"]["gRecaptchaResponse"][:35]
                        Log.good(f"Solved captcha ({colorama.Fore.LIGHTBLACK_EX}{cap_pri}..{colorama.Fore.RESET})")
                        return r.json()["solution"]["gRecaptchaResponse"]
                time.sleep(0.5)
            except Exception:
                Log.bad("Failed to solve captcha.", symbol="!")
                return None
        Log.bad("Failed to solve captcha.", symbol="!")
        return None
