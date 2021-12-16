#!cryptoscriptsenv/bin/python

# import csv of transactions and print profit data

import argparse, os, tabulate, requests, json, sys, configparser
from cryptolib import cc

config = configparser.RawConfigParser()
configPath = "crypto.cfg"
url = "https://api.livecoinwatch.com/coins/single"


class Coin:
    def __init__(self, name):
        self.name = name
        self.deposits = []
        self.prices = []

    def addTrans(self, quantity, price):
        self.deposits.append(quantity)
        self.prices.append(price)


def main():
    parser = argparse.ArgumentParser(description='Import csv of transactions and pring profit data.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('filepath', help='Path of csv to import.')
    args = parser.parse_args()

    # populate objects
    if not os.path.exists(args.filepath):
        print("Error: file not found")
        sys.exit()

    # get config
    if not os.path.exists(configPath):
        print(f'Error: {configPath} not found')
        sys.exit()

    config.read(configPath)
    try:
        key = config.get("key", "key")
    except KeyError:
        print("Error: no key found")
        sys.exit()

    headers = {
        'content-type': 'application/json',
        'x-api-key': f'{key}'
    }

    objs = {}
    with open(args.filepath, 'r') as f:
        for line in f:
            if "date,trade" in line.lower():
                continue

            date, trade, quantity, base, quote, feecurrency, feetype, price, sincetrade = line.split(',')
            if "deposit" not in trade:
                continue

            if base not in objs.keys():
                objs[base] = Coin(base)

            obj = objs.get(base)
            obj.addTrans(float(quantity), float(price))

    # print coin info
    for obj in objs.values():
        buys = []
        payload = json.dumps({
            "currency": "USD",
            "code": f'{obj.name}',
            "meta": False
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        res = response.json()
        currentPrice = float(res["rate"])
        if not currentPrice:
            continue

        print(f'{obj.name} {currentPrice:.4f}:')
        text = [["Deposit", "Price", "Profit"]]
        for deposit, price in zip(obj.deposits, obj.prices):
            buyValue = deposit * price
            curValue = deposit * currentPrice
            profit = curValue - buyValue
            buys.append(buyValue)
            text.append([f'{deposit:.4f}', f'${price:.2f}', f'{cc(profit)}'])

        totBuyValue = sum(buys)
        totCurValue = sum(obj.deposits) * currentPrice
        totProfit = totCurValue - totBuyValue
        text.append([f'Total Buy:{cc(totBuyValue)}', f'Total Value:{cc(totCurValue)}', f'Total Profit:{cc(totProfit)}'])
        print(tabulate.tabulate(text, headers="firstrow", tablefmt="fancy_grid"))
        print("")


if __name__ == "__main__":
    main()
