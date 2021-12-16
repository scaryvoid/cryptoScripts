#!cryptoscriptsenv/bin/python

# library for crypto scripts

import configparser, sys, os, json, requests

config = configparser.RawConfigParser()
configPath = os.path.join('/', 'home', 'scaryvoid', 'cryptoScripts', 'crypto.cfg')
url = "https://api.livecoinwatch.com/coins/single"
if not os.path.exists(configPath):
    print(f'Error: {configPath} not found')
    sys.exit()

config.read(configPath)
try:
    key = config.get("key", "key")
except KeyError:
    print("Error: no key found")
    sys.exit()


class colors:
    RED = '\033[0;31m'
    NONE = '\033[0m'
    TITLE = '\033[7;31m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[0;33m'


def cc(f, usd=True):
    neg = True if f < 0 else False
    string = f'{abs(f):,.2f}'
    pre = "$" if usd else ""
    pre = colors.RED + f'-{pre}' if neg else colors.GREEN + pre
    post = "%" if not usd else ""
    return f'{pre}{string}{post}' + colors.NONE


def getCoinData(name):
    headers = {
        'content-type': 'application/json',
        'x-api-key': f'{key}'
    }
    payload = json.dumps({
        "currency": "USD",
        "code": f'{name}',
        "meta": False
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()
