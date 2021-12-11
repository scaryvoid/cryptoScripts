#!/bin/env python3

# give me 3 buy limits based on current price and desired percentages

import argparse


def getLimit(currentVal, per):
    return currentVal - (currentVal * (per / 100))


def main():
    parser = argparse.ArgumentParser(description='Print buy limits based on current value.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('currentVal', type=float, help='Current Value.')
    parser.add_argument('-a', metavar='<n>', nargs=1, default=[15], type=int, help='First dip percentage.')
    parser.add_argument('-b', metavar='<n>', nargs=1, default=[20], type=int, help='Second dip percentage.')
    parser.add_argument('-c', metavar='<n>', nargs=1, default=[25], type=int, help='Third dip percentage.')
    args = parser.parse_args()

    print(f'Limit 1: {getLimit(args.currentVal, args.a[0])}')
    print(f'Limit 2: {getLimit(args.currentVal, args.b[0])}')
    print(f'Limit 3: {getLimit(args.currentVal, args.c[0])}')


if __name__ == "__main__":
    main()
