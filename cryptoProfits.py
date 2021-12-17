#!/home/scaryvoid/venv/cryptoscripts/bin/python

# import csv of transactions and print profit data

import argparse, os, tabulate, sys
from cryptolib import cc, getCoinDataList


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

    if not os.path.exists(args.filepath):
        print("Error: file not found")
        sys.exit()

    # parse csv file and create coin objs
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

    # get current prices for coins
    json = getCoinDataList()
    for key, obj in objs.items():
        for d in json:
            if d["code"] == key:
                obj.currentPrice = d["rate"]

    # print coin info
    profits = []
    invested = []
    for key, obj in sorted(objs.items()):
        buys = []
        coins = []
        if not obj.currentPrice:
            continue

        print(f'{obj.name} {obj.currentPrice:.4f}:')
        text = [["Coins", "Price", "Invested", "Profit", "% Profit"]]
        for deposit, price in zip(obj.deposits, obj.prices):
            buyValue = deposit * price
            curValue = deposit * obj.currentPrice
            profit = curValue - buyValue
            buys.append(buyValue)
            coins.append(deposit)
            text.append([f'{deposit:,.4f}', f'${price:,.2f}', f'{cc(buyValue)}', f'{cc(profit)}', f'{cc((profit / buyValue) * 100, False)}'])

        totBuyValue = sum(buys)
        totCurValue = sum(obj.deposits) * obj.currentPrice
        totProfit = totCurValue - totBuyValue
        text.append([f'Total Coins:{sum(coins):,.4f}', f'Total Buy:{cc(totBuyValue)}', f'Total Value:{cc(totCurValue)}', f'Total Profit:{cc(totProfit)}', f'% Profit:{cc((totProfit / totBuyValue) * 100, False)}'])
        profits.append(totProfit)
        invested.append(totBuyValue)
        print(tabulate.tabulate(text, headers="firstrow", tablefmt="fancy_grid"))
        print("")

    totText = [["Total Invested", "Total Profit", "% Profit"]]
    totText.append([f'${sum(invested):,.2f}', f'{cc(sum(profits))}', f'{cc((sum(profits) / sum(invested)) * 100, False)}'])
    print(tabulate.tabulate(totText, headers="firstrow", tablefmt="fancy_grid"))


if __name__ == "__main__":
    main()
