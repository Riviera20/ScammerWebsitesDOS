import random
import sys
import time
import urllib

import requests


def load_proxies_from_url():
    try:
        response = requests.get(
            "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text&anonymity=Elite&timeout=4999")
        response.raise_for_status()
        proxies = response.text.splitlines()
        return proxies
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching proxies: {e}")
        return []


def load_random_bestemmia():
    lines = open("bestemmie.txt").read().splitlines()
    return random.choice(lines)


def send_post_request(url):
    email = load_random_bestemmia()
    password = load_random_bestemmia()
    tel = load_random_bestemmia()

    data = {
        "email": email,
        "password": password,
        "tel": tel
    }
    encoded_data = urllib.parse.urlencode(data)
    try:

        if useProxies:
            if not proxies:
                print("No proxies found.")
                return

            selected_proxy = random.choice(proxies)
            proxy_dict = {
                "http": selected_proxy,
                "https": selected_proxy
            }

            response = requests.post(url, data=encoded_data, proxies=proxy_dict, timeout=5, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        else:
            response = requests.post(url, data=encoded_data, timeout=3, headers={'Content-Type': 'application/x-www-form-urlencoded'})

        print(f"Response Status Code: {response.status_code}")
    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    url = input("Insert the url (Check the README for examples ;) ): ")
    args = sys.argv[1:]

    useProxies = False
    proxies = None

    if "--proxies" in args:
        useProxies = True
        proxies = load_proxies_from_url()

    last_proxy_reload = time.time()

    while 1:
        if useProxies and (time.time() - last_proxy_reload) > 300: # 5min
            proxies = load_proxies_from_url()
            last_proxy_reload = time.time()

        send_post_request(url)
        time.sleep(1)
