import cloudscraper
import random
import itertools
import json
import os
from datetime import datetime, timezone
import time
from colorama import *
import pytz
from requests.exceptions import RequestException

wib = pytz.timezone('Asia/Jakarta')

class VooiApp:
    def __init__(self) -> None:
        self.scraper = cloudscraper.create_scraper()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'api-tg.vooi.io',
            'Origin': 'https://app.tg.vooi.io',
            'Pragma': 'no-cache',
            'Referer': 'https://app.tg.vooi.io/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
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

    def login(self, query: str):
        url = 'https://api-tg.vooi.io/api/v2/auth/login'
        data = json.dumps({'initData': query})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        response = self.scraper.post(url, headers=self.headers, data=data)
        result = response.json()
        if response.status_code == 201:
            token  = result['tokens']['access_token']
            return result, token
        else:
            return None
        
    def check_frens(self, token: str):
        url = 'https://api-tg.vooi.io/api/frens'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.scraper.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def claim_frens(self, token: str):
        url = 'https://api-tg.vooi.io/api/frens/claim'
        data = {}
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.scraper.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            return True
        else:
            return False
        
    def check_autotrade(self, token: str):
        url = 'https://api-tg.vooi.io/api/autotrade'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.scraper.get(url, headers=self.headers)
        if response.status_code in [200, 201]:
            try:
                return response.json()
            except json.JSONDecodeError:
                return None
        else:
            return None
        
    def start_autotrade(self, token: str):
        url = 'https://api-tg.vooi.io/api/autotrade/start'
        data = {}
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.scraper.post(url, headers=self.headers, json=data)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return None
        
    def claim_autotrade(self, token: str, autotrade_id: str):
        url = 'https://api-tg.vooi.io/api/autotrade/claim'
        data = json.dumps({'autoTradeId': autotrade_id})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.scraper.post(url, headers=self.headers, data=data)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return None
        
    def start_tapping(self, token: str):
        url = 'https://api-tg.vooi.io/api/tapping/start_session'
        data = {}
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.scraper.post(url, headers=self.headers, json=data)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return None
        
    def finish_tapping(self, token: str, session_id: str, money: str, points: str):
        url = 'https://api-tg.vooi.io/api/tapping/finish'
        data = json.dumps({'sessionId': session_id, 'tapped': {'virtMoney': money, 'virtPoints': points}})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.scraper.post(url, headers=self.headers, data=data)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return None
        
    def get_tasks(self, token: str):
        url = 'https://api-tg.vooi.io/api/tasks?limit=200&skip=0'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.scraper.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()['nodes']
        else:
            return None
        
    def start_tasks(self, token: str, task_id: str):
        url = f'https://api-tg.vooi.io/api/tasks/start/{task_id}'
        data = {}
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.scraper.post(url, headers=self.headers, json=data)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return None
        
    def claim_tasks(self, token: str, task_id: str):
        url = f'https://api-tg.vooi.io/api/tasks/claim/{task_id}'
        data = {}
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.scraper.post(url, headers=self.headers, json=data)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return None
        
    def question(self):
        while True:
            tap_tap = input("Play Tap Tap Game? [y/n] -> ").strip().lower()
            if tap_tap in ["y", "n"]:
                tap_tap = tap_tap == "y"
                break
            else:
                print(f"{Fore.RED + Style.BRIGHT}Invalid Input.{Fore.WHITE + Style.BRIGHT} Choose 'y' to Yes or 'n' to No.{Style.RESET_ALL}")

        if tap_tap:
            while True:
                try:
                    print("1. Multi Account Processing [1x Tap Tap Game]")
                    print("2. Single Account Processing [Looping Tap Tap Game]")
                    choose = int(input("Choose [1/2] -> ").strip())

                    if choose in [1, 2]:
                        print(f"{Fore.GREEN + Style.BRIGHT}You chose {'Multi' if choose == 1 else 'Single'} Account Processing.{Style.RESET_ALL}")
                        return tap_tap, choose
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")
        
        return tap_tap, None
        
    def process_query(self, query: str, tap_tap: bool, choose: int):
        try:
            data, token = self.login(query)

            if data:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {data['name']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Money{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {data['balances']['virt_money']} Virtual USD {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Points{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {data['balances']['virt_points']} VT {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )

                frens = self.check_frens(token)
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
                                    f"{Fore.WHITE+Style.BRIGHT} {reward} VT {Style.RESET_ALL}"
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
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Next Claim at{Style.RESET_ALL}"
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
                        f"{Fore.RED+Style.BRIGHT} is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )

                autotrade = self.check_autotrade(token)
                if not autotrade:
                    start = self.start_autotrade(token)
                    if start:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Started {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )

                    autotrade = self.check_autotrade(token)

                if autotrade:
                    end_time = autotrade['endTime']
                    utc_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                    wib_time = utc_time.astimezone(wib).strftime('%x %X %Z')
                    
                    autotrade_id = autotrade.get('autoTradeId', None)

                    if autotrade['status'] == 'finished' and autotrade_id:
                        claim = self.claim_autotrade(token, autotrade_id)
                        if claim:
                            self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        else:
                            self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} Not Time to Claim {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Claim at{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {wib_time} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )

                    start = self.start_autotrade(token)
                    if start:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Started {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Claim at{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {wib_time} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Autotrade{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} Is Already Started {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )

                tasks = self.get_tasks(token)
                if tasks:
                    for task in tasks:
                        task_id = task['id']

                        if task['status'] == 'new':
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

                            tasks = self.get_tasks(token)

                        if task['status'] == 'done':
                            claim = self.claim_tasks(token, task_id)
                            if claim and 'claimed' in claim:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['name'].upper()} {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['description']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {claim['claimed']['virt_money']} Virtual USD {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {claim['claimed']['virt_points']} VT {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
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
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )

                if tap_tap:
                    if choose == 1:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Started {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        start = self.start_tapping(token)
                        if not start:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT} Isn't Started {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        
                        session_id = start['sessionId']

                        money_limit = int(start['config']['virtMoneyLimit'])
                        points_limit = int(start['config']['virtPointsLimit'])

                        money = random.randint(max(1, int(money_limit * 0.5)), int(money_limit * 0.8))
                        money -= money % 1

                        points = points_limit if points_limit > 0 else 0

                        print(
                            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} 30 Seconds {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}]{Style.RESET_ALL}",
                            end="\r",
                            flush=True
                        )
                        time.sleep(30)

                        finish = self.finish_tapping(token, session_id, money, points)
                        if finish:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {finish['tapped']['virtMoney']} Virtual USD {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}|{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {finish['tapped']['virtPoints']} VT {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT} Isn't Completed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )

                    else:
                        for game in itertools.count(1):
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {game} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}Started{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                            session_data = self.start_tapping(token)
                            if not session_data:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {game} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Failed to Start{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                                continue
                            
                            session_id = session_data['sessionId']

                            money_limit = int(session_data['config']['virtMoneyLimit'])
                            points_limit = int(session_data['config']['virtPointsLimit'])

                            money = random.randint(max(1, int(money_limit * 0.5)), int(money_limit * 0.8))
                            money -= money % 1

                            points = points_limit if points_limit > 0 else 0

                            print(
                                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} 30 Seconds {Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT}]{Style.RESET_ALL}",
                                end="\r",
                                flush=True
                            )
                            time.sleep(30)

                            finish = self.finish_tapping(token, session_id, money, points)
                            if finish:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {game} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {finish['tapped']['virtMoney']} Virtual USD {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}|{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {finish['tapped']['virtPoints']} VT {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {game} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Not Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )

                            print(
                                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT} Wait... {Style.RESET_ALL}"
                                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                                end="\r",
                                flush=True
                            )
                            time.sleep(1.5)
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Play Game{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Is Skipped {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )

        except RequestException as e:
            self.log(
                f"{Fore.RED + Style.BRIGHT}[ Blocked By Cloudflare ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}[ Restart First ]{Style.RESET_ALL}"
            )

    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            tap_tap, choose = self.question()

            while True:
                self.clear_terminal()
                time.sleep(1)
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-------------------------------------------------------------------------{Style.RESET_ALL}")

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query, tap_tap, choose)
                        self.log(f"{Fore.CYAN+Style.BRIGHT}-------------------------------------------------------------------------{Style.RESET_ALL}")

                seconds = 3
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
    vooi = VooiApp()
    vooi.main()
