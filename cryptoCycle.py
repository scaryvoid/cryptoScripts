#!/home/scaryvoid/venv/cryptoscriptsenv/bin/python

import argparse, tabulate


def main():
    parser = argparse.ArgumentParser(description='Print buy limits based on current value.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('initialAmt', type=float, help='Amount initially invested.')
    parser.add_argument('percentSell', type=float, help='Percentage to pull out and reinvest.')
    parser.add_argument('percentDip', type=float, help='Percentage of dip from initialGain.')
    args = parser.parse_args()
    perSell = args.percentSell / 100
    perDip = args.percentDip / 100
    l = [["Initial Amount", "Sell Amount", f"After {args.percentDip}% Dip", "Reinvest/Recovery", "% Needed Rec", "Gross Profit", "Profit < 1 Year", "Profit > 1 Year"]]
    sell = args.initialAmt * perSell
    dip = (args.initialAmt - sell) * (1 - perDip)
    recPer = (args.initialAmt - sell - dip) / dip
    final = (dip + sell) * (1 + recPer)
    profit = (final - args.initialAmt) * (1 - .010)  # 0.5% times three (sell, buy). Profits do not count final sell.
    l.append([f'{args.initialAmt}', f'{sell}', f'{dip}', f'{final}', f'{recPer * 100}', f'{profit}', f'{profit * (1 - .2697)}', f'{profit * (1 - .1963)}'])
    print(tabulate.tabulate(l, headers="firstrow", tablefmt="fancy_grid"))


if __name__ == "__main__":
    main()
