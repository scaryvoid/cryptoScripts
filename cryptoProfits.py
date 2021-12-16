#!/home/scaryvoid/venv/cryptoscriptsenv/bin/python

# import csv of transactions and print profit data

import argparse, os, tabulate, sys
from cryptolib import cc, getCoinData


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

    if not os.path.exists(args.filepath):
        print("Error: file not found")
        sys.exit()

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
        currentPrice = float(getCoinData(obj.name)["rate"])
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
