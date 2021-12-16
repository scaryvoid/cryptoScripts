#!/home/scaryvoid/venv/cryptoscriptsenv/bin/python

# print percentages of given amount

import argparse, sys


def main():
    parser = argparse.ArgumentParser(description='Look at depths of dips.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('initialamt', type=float, help='Amount to divide up.')
    parser.add_argument('percentages', metavar='<percentages>', type=float, nargs=argparse.REMAINDER, help='Percentages to divide initialamt into.')
    args = parser.parse_args()
    args.percentages.sort(reverse=True)
    
    # may not want this bit, make optional?
    if sum(args.percentages) != 100:
        print(f'Error: Sum of percentages ({sum(args.percentages)}) is not 100')
        sys.exit()
    
    for p in args.percentages:
        print(f'{p}% of args.initialamt = {args.initialamt * (float(p) / 100):.02f}')
    

if __name__ == "__main__":
    main()
