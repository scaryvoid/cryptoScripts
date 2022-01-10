#!/home/scaryvoid/venv/cryptoscripts/bin/python

# give me 3 buy limits based on current price and desired percentages

import argparse
from cryptolib import getCoinData


def getLimit(currentVal, per):
    return currentVal - (currentVal * (per / 100))


def main():
    parser = argparse.ArgumentParser(description='Print buy limits based on current value.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('coinName', help='Current Value.')
    parser.add_argument('percentages', metavar='<n>', type=float, nargs=argparse.REMAINDER, help='Percentages to divide initialamt into.')
    args = parser.parse_args()

    currentVal = getCoinData(args.coinName)["rate"]
    for i, p in enumerate(args.percentages):
        print(f'Limit {i + 1}: {getLimit(currentVal, p):.2f}')


if __name__ == "__main__":
    main()
