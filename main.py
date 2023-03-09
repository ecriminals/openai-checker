from colorama import Fore, init
from os import system
import requests
import random
import time

init(autoreset=True)


class OpenAiKey:
    def __init__(this):
        this._char_length = 48
        this._chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def _keys(this):
        with open("./data/keys.txt", "w") as _f:
            start = time.time()
            for i in range(100_000):
                b = [
                    this._chars[random.randint(0, len(this._chars) - 1)]
                    for i in range(this._char_length)
                ]
                _f.write(f'sk-{"".join(b)}\n')

            _f.close()
            elapsed = time.time() - start
            print(f"Generated 100k Keys. | {elapsed:.2f}s")


class OpenAiCheck:
    def __init__(this):
        with open("./data/keys.txt", "r") as f:
            this._key = [line.strip() for line in f.readlines()]
        this._session = requests.Session()
        this._check_api = "https://api.openai.com/v1/chat/completions"

    def _start(this):
        for key in this._key:
            time.sleep(1.5)
            system("clear")
            _res = this._session.post(
                this._check_api,
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                          "role": "user", 
                          "content": "What is the OpenAI mission?"}
                    ],
                },
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {key}",
                },
            )
            try:
                if _res.status_code == 401:
                    print(f"{Fore.RESET}[{Fore.RED}*{Fore.RESET}] {key} invalid.")

                elif _res.status_code == 200:
                    print(f"{Fore.RESET}[{Fore.GREEN}*{Fore.RESET}] {key} valid.")
                    open("./data/avail.txt", "a").write(f"{_res.json()}\n")
            except Exception as e:
                print(f"{Fore.RESET}[{Fore.MAGENTA}!{Fore.RESET}] {key} {e}.")


if __name__ == "__main__":
    _choice = input("[1] Generate Keys | [2] Check Keys\n-> ")
    if _choice == "1":
        OpenAiKey()._keys()

    elif _choice == "2":
        OpenAiCheck()._start()
