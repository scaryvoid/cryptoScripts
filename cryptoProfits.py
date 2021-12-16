#!/bin/env python3

# import csv of transactions and print profit data

import argparse, os, tabulate


class Coin:
    def __init__(self, name):
        self.name = name
        self.deposits = []
        self.prices = []
        self.currentPrice = 0

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
        os.exit()

    objs = {}
    with open(args.filepath, 'r') as f:
        for line in f:
            if "date,trade" in line.lower():
                continue

            date, trade, quantity, base, quote, feecurrency, feetype, price = line.split(',')
            if "deposit" not in trade:
                continue

            if base not in objs.keys():
                objs[base] = Coin(base)

            obj = objs.get(base)
            obj.addTrans(float(quantity), float(price))

    # todo: get current prices

    # print coin info
    for obj in objs.values():
        print(f'{obj.name}:')
        text = [["Deposit", "Price", "Profit"]]
        for deposit, price in zip(obj.deposits, obj.prices):
            buyValue = deposit * price
            curValue = deposit * obj.currentPrice
            profit = curValue - buyValue
            text.append([f'{deposit}', f'{price}', f'{profit}'])

        totBuyValue = sum(obj.deposits) * sum(obj.prices)
        totCurValue = sum(obj.deposits) * obj.currentPrice
        totProfit = totCurValue - totBuyValue
        text.append([f'Total Buy:{totBuyValue}', f'Total Value:{totCurValue}', f'Total Profit:{totProfit}'])
        print(tabulate.tabulate(text, headers="firstrow", tablefmt="fancy_grid"))


if __name__ == "__main__":
    main()
