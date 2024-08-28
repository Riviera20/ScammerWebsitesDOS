import random
import sys
import time
import urllib

import requests


def load_proxies_from_url():
    try:
        response = requests.get(
            "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=protocolipport&format=text&timeout=20000")
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

        if (useProxies):
            proxies = load_proxies_from_url()
            if not proxies:
                print("No proxies found.")
                return

            selected_proxy = random.choice(proxies)
            proxy_dict = {
                "http": selected_proxy,
                "https": selected_proxy
            }

            response = requests.post(url, data=encoded_data, proxies=proxy_dict, timeout=3, headers={'Content-Type': 'application/x-www-form-urlencoded'})
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

    if "--proxies" in args:
        useProxies = True

    while 1:
        send_post_request(url)
        time.sleep(1)
