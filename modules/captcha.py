import requests
import time
from .logging import Log
import colorama


##  ##  ##
# Im revamping all this shitty old code soon no worries
##  ##  ## 

class Captcha:
    @staticmethod
    def solve(user_agent: str, api_key:str, proxy: str, service: str='capmonster', site_key: str="4c672d35-0701-42b2-88c3-78380b0db560", rq_data: str=None, max_retries: int=150) -> str|bool:
        custom = None
        headers = {
            'user-agent': "Mozilla"
        }
        if service == "capmonster":
            url = 'https://api.capmonster.cloud'
            payload = {
                    "clientKey": api_key,
                    "task":
                    {
                        "type":"HCaptchaTaskProxyless",
                        "websiteURL":"https://discord.com/",
                        "websiteKey": site_key,
                        "userAgent": user_agent,
                    }
            }
        elif service == "capsolver":
            url = "https://api.capsolver.com"
            payload = {
                    "clientKey": api_key,
                    "task":
                    {
                        "websiteURL":"https://discord.com/",
                        "websiteKey": site_key,
                    }
            }
            payload["task"]["type"] = "HCaptchaTurboTask"
            payload["task"]["proxy"] = proxy
            payload['task']['userAgent'] = user_agent
        elif service == "hcoptcha":
            url = "https://api.hcoptcha.online/api"
            payload = {
            "api_key": api_key, 
            "task_type": "hcaptchaEnterprise", 
                "data": {
                    "sitekey": site_key,
                    "proxy": proxy,
                    "host": "discord.com"
                }
            }
        elif service == "24captcha":
            custom = True
            url = "https://24captcha.online/in.php"
            payload = {                
                "key": api_key,
                "sitekey": site_key,
                "pageurl": "https://discord.com/register",
                "proxy": proxy,
                "json": 0
            }
        elif service == "fcaptcha":
            custom = True
            url = 'https://api.fcaptcha.lol/api/createTask'
            headers = {"authorization": api_key}
            payload = {
                "sitekey": site_key,
                "host": "https://discord.com",
                "proxy": proxy,
                "user_agent": user_agent
            }
        elif service == "2captcha":
            url = "https://2captcha.com"
            payload = {
                "clientKey":api_key,
                "task": {
                    "type":"HCaptchaTaskProxyless",
                    "websiteURL":"https://discord.com/register",
                    "websiteKey":site_key
                }
            }
        elif service == "anticaptcha":
            url = "https://api.anti-captcha.com"
            payload = {
                "clientKey": api_key,
                "task": {
                    "type": "HCaptchaTaskProxyless",
                    "websiteURL": "https://discord.com/register",
                    "websiteKey": site_key,
                    "isInvisible": False
                },
                "softId": 0
            }
        
        try:
            if custom:
                r = requests.post(url, headers=headers, json=payload)
            else:
                r = requests.post(f"{service}/createTask", json=payload)
        except:
            Log.bad(f"Error Creating {service} Task")
            return None
        try:
            
            if service not in ['hcoptcha', '24captcha', 'fcaptcha']:
                if r.json().get("taskId"):
                    taskid = r.json()["taskId"]
                else:
                    Log.bad("Error getting captcha task id")
                    return None
            else:
                if service == "24captcha":
                    try:
                        taskid = r.text.split("|")[1]
                    except:
                        Log.bad("Error getting captcha task id")
                        return None                 
                elif service == 'fcaptcha':
                    taskid = r.json()['task']['task_id']
                else:
                    if r.json().get("task_id"):
                        taskid = r.json()["task_id"]
                    else:
                        Log.bad("Error getting captcha task id")
                        return None
        except:
            Log.bad("Error getting captcha task id")
            return None
        for i in range(max_retries):
            try:
                if service not in ['hcoptcha', '24captcha', 'fcaptcha']:
                    r = requests.post(f"{url}/getTaskResult",json={"clientKey": api_key,"taskId":taskid})
                    if r.json()["status"] == "ready":
                        cap_pri = r.json()["solution"]["gRecaptchaResponse"][:35]
                        Log.good(f"Solved captcha ({colorama.Fore.LIGHTBLACK_EX}{cap_pri}..{colorama.Fore.RESET})")
                        return r.json()["solution"]["gRecaptchaResponse"]
                else:
                    if service == "24captcha":
                        payload = {
                            "key": api_key,
                            "id": taskid,
                            "action": "get",
                            "json": 1
                        }
                        r = requests.post("https://24captcha.online/res.php", json=payload).json()
                        if r['status'] == 1:
                            cap_pri = r["request"][:35]
                            Log.good(f"Solved captcha ({colorama.Fore.LIGHTBLACK_EX}{cap_pri}..{colorama.Fore.RESET})")
                            return r["request"]             
                    elif service == "fcaptcha":
                        r = requests.post(f"https://api.fcaptcha.lol/api/getTaskData", headers=headers, json={"task_id":taskid})
                        if r.json()['task']['state'] == "completed":
                            cap_pri = r.json()["task"]["captcha_key"][:35]
                            Log.good(f"Solved captcha ({colorama.Fore.LIGHTBLACK_EX}{cap_pri}..{colorama.Fore.RESET})")
                            return r.json()["task"]["captcha_key"]  
                    else:
                        r = requests.post(f"{url}/getTaskData",json={"api_key": api_key,"task_id":taskid})
                        if r.json()['task']['state'] == "completed":
                            cap_pri = r.json()["task"]["captcha_key"][:35]
                            Log.good(f"Solved captcha ({colorama.Fore.LIGHTBLACK_EX}{cap_pri}..{colorama.Fore.RESET})")
                            return r.json()["task"]["captcha_key"]
                time.sleep(0.5)
            except Exception:
                Log.bad("Failed to solve captcha.", symbol="!")
                return None
        Log.bad("Failed to solve captcha.", symbol="!")
        return None

