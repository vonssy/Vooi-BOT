import cloudscraper
import requests
from datetime import datetime, timezone
from colorama import *
from fake_useragent import FakeUserAgent
import json, os, time, random, pytz

wib = pytz.timezone('Asia/Jakarta')

class VooiApp:
    def __init__(self) -> None:
        self.scraper = cloudscraper.create_scraper()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'api-tg.vooi.io',
            'Origin': 'https://app.tg.vooi.io',
            'Pragma': 'no-cache',
            'Referer': 'https://app.tg.vooi.io/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': FakeUserAgent().random
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Vooi App - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def user_login(self, query: str, retries=3):
        url = 'https://api-tg.vooi.io/api/v2/auth/login'
        data = json.dumps({'initData':query, 'inviterTelegramId':'DYR2rnq'})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=headers, data=data, timeout=10)
                if response.status_code == 403:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Blocked By Cloudflare. {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}Restart Again{Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                    )
                    return
        
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def frens_data(self, token: str, retries=3):
        url = 'https://api-tg.vooi.io/api/frens'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                response = self.scraper.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def claim_frens(self, token: str, retries=3):
        url = 'https://api-tg.vooi.io/api/frens/claim'
        data = {}
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=headers, json=data, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def autotrade_data(self, token: str, retries=3):
        url = 'https://api-tg.vooi.io/api/autotrade'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                response = self.scraper.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return None
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def start_autotrade(self, token: str, retries=3):
        url = 'https://api-tg.vooi.io/api/autotrade/start'
        data = {}
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=headers, json=data, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def claim_autotrade(self, token: str, autotrade_id: str, retries=3):
        url = 'https://api-tg.vooi.io/api/autotrade/claim'
        data = json.dumps({'autoTradeId':autotrade_id})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=headers, data=data, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def task_lists(self, token: str, retries=3):
        url = 'https://api-tg.vooi.io/api/tasks'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                response = self.scraper.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                return response.json()['nodes']
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                        
    def start_tasks(self, token: str, task_id: int, retries=3):
        url = f'https://api-tg.vooi.io/api/tasks/start/{task_id}'
        data = {}
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=headers, json=data, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def claim_tasks(self, token: str, task_id: int, retries=3):
        url = f'https://api-tg.vooi.io/api/tasks/claim/{task_id}'
        data = {}
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=headers, json=data, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                    
    def start_tapping(self, token: str, retries=3):
        url = 'https://api-tg.vooi.io/api/tapping/start_session'
        data = {}
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=headers, json=data, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def finish_tapping(self, token: str, session_id: str, money: str, points: str, retries=3):
        url = f'https://api-tg.vooi.io/api/tapping/finish'
        data = json.dumps({'sessionId':session_id, 'tapped':{'virtMoney':money, 'virtPoints':points}})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        for attempt in range(retries):
            try:
                response = self.scraper.post(url, headers=headers, data=data, timeout=10)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.Timeout, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}Request Timeout.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
                
    def question(self):
        while True:
            try:
                print("1. Multi Account Processing [1x Tap Tap Game]")
                print("2. Single Account Processing [Looping Tap Tap Game]")
                choose = int(input("Choose [1/2] -> ").strip())

                if choose in [1, 2]:
                    print(f"{Fore.GREEN + Style.BRIGHT}{'Multi' if choose == 1 else 'Single'} Account Processing Selected.{Style.RESET_ALL}")
                    time.sleep(1)
                    return choose
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")
            
    def process_query(self, query: str, choose: int):
        user = self.user_login(query)
        if not user:
            return
        
        if user:
            token = user['tokens']['access_token']
            money = float(user['balances']['virt_money'])
            points = float(user['balances']['virt_points'])
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {user['name']} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}] [ Money{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {money:.2f} $USD {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}] [ Points{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {points:.2f} $VT {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )
            time.sleep(1)

            frens = self.frens_data(token)
            if frens:
                now = datetime.utcnow().replace(tzinfo=timezone.utc)
                next_claim = datetime.fromisoformat(frens['nextDateToClaim'].replace("Z", "+00:00"))
                next_claim_wib = next_claim.astimezone(wib).strftime('%x %X %Z')

                reward = float(frens['totalProfit'])
                if reward > 0:
                    if now > next_claim:
                        claim = self.claim_frens(token)
                        if claim:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Frens{Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {reward:.2f} $VT {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Frens{Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Frens{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} Not Time to Claim {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Claim at{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {next_claim_wib} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Frens{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} No Profit to Claim {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Frens{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Data is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
            time.sleep(1)

            autotrade = self.autotrade_data(token)
            if not autotrade:
                start = self.start_autotrade(token)
                if start:
                    end_utc = datetime.fromisoformat(start['endTime'].replace('Z', '+00:00'))
                    end_wib = end_utc.astimezone(wib).strftime('%x %X %Z')
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Is Started {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Claim at{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {end_wib} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

            else:
                status = autotrade['status']
                if status == 'finished':
                    autotrade_id = autotrade['autoTradeId']
                    claim = self.claim_autotrade(token, autotrade_id)
                    if claim:
                        money_reward = float(claim['reward']['virtMoney'])
                        vt_reward = float(claim['reward']['virtPoints'])
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {money_reward:.2f} $USD {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {vt_reward:.2f} $VT {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        time.sleep(1)

                        start = self.start_autotrade(token)
                        if start:
                            end_utc = datetime.fromisoformat(start['endTime'].replace('Z', '+00:00'))
                            end_wib = end_utc.astimezone(wib).strftime('%x %X %Z')
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT} Is Started {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Claim at{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {end_wib} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    time.sleep(1)

                elif status == 'claimed':
                    start = self.start_autotrade(token)
                    if start and start['status'] == "in_progress":
                        end_utc = datetime.fromisoformat(start['endTime'].replace('Z', '+00:00'))
                        end_wib = end_utc.astimezone(wib).strftime('%x %X %Z')
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Started {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Claim at{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {end_wib} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    time.sleep(1)

                else:
                    end_utc = datetime.fromisoformat(autotrade['endTime'].replace('Z', '+00:00'))
                    end_wib = end_utc.astimezone(wib).strftime('%x %X %Z')
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Not Time to Claim {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Claim at{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {end_wib} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                    time.sleep(1)

            tasks = self.task_lists(token)
            if tasks:
                completed = False
                for task in tasks:
                    task_id = str(task['id'])
                    status = task['status']

                    if task and status == 'new':
                        start = self.start_tasks(token, task_id)
                        if start:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['name'].upper()} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['description']} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT} Is Started {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['name'].upper()} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['description']} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        time.sleep(1)

                    elif task and status == 'done':
                        claim = self.claim_tasks(token, task_id)
                        if claim:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['name'].upper()} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['description']} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['reward']['virt_money']} $USD {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['reward']['virt_points']} $VT {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['name'].upper()} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['description']} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        time.sleep(1)

                    elif task and status == 'in_progress':
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {task['name'].upper()} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {task['description']} {Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT}In Progress{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                        time.sleep(1)

                    else:
                        completed = True

                if completed:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                    
            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
            time.sleep(1)

            if choose == 1:
                start = self.start_tapping(token)
                if start:
                    session_id = start['sessionId']
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT}Is Started{Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                    )

                    for remaining in range(30, 0, -1):
                        print(
                            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}Seconds to Finish Game{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}  ",
                            end="\r",
                            flush=True
                        )
                        time.sleep(1)

                    money_config = int(start['config']['virtMoneyLimit'])
                    points = int(start['config']['virtPointsLimit'])
                    money = random.randint(money_config - 25, money_config)

                    finish = self.finish_tapping(token, session_id, money, points)
                    if finish:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT}Is Finished{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {points} $USD {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {points} $VT {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT}Isn't Finished{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}            "
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                    )
                time.sleep(1)

            else:
                while True:
                    start = self.start_tapping(token)
                    if start:
                        session_id = start['sessionId']
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT}Is Started{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}             "
                        )

                        for remaining in range(30, 0, -1):
                            print(
                                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}Seconds to Finish Game{Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}  ",
                                end="\r",
                                flush=True
                            )
                            time.sleep(1)

                        money_config = int(start['config']['virtMoneyLimit'])
                        points = int(start['config']['virtPointsLimit'])
                        money = random.randint(money_config - 25, money_config)

                        finish = self.finish_tapping(token, session_id, money, points)
                        if finish:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}Is Finished{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {money} $USD {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {points} $VT {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Isn't Finished{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}             "
                            )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} ID {session_id} {Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                    time.sleep(1)

                    for remaining in range(3, 0, -1):
                        print(
                            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}Seconds to Play Next Game{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}  ",
                            end="\r",
                            flush=True
                        )
                        time.sleep(1)

    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            choose = self.question()

            while True:
                self.clear_terminal()
                time.sleep(1)
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query, choose)
                        self.log(f"{Fore.CYAN+Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        time.sleep(3)

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Vooi App - BOT.{Style.RESET_ALL}                                      ")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    bot = VooiApp()
    bot.main()