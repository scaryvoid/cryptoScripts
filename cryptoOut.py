#!/home/scaryvoid/venv/cryptoscripts/bin/python

import argparse, tabulate


def main():
    parser = argparse.ArgumentParser(description='Print buy limits based on current value.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('investAmt', type=float, help='Current Value.')
    parser.add_argument('perGain', type=float, help='Percentage per out.')
    parser.add_argument('perOut', type=float, help='Percentage to pull out.')
    args = parser.parse_args()

    output = [["", "Invested", f"{args.perGain}% Gain", "Out", "Withdrawn", "Cash Out", "No Out"]]
    lastVal = args.investAmt
    totOut = 0
    noOut = args.investAmt
    for i in range(1, 11):
        newGain = lastVal * (args.perGain / 100)
        out = newGain * (args.perOut / 100)
        noOut = noOut + (noOut * (args.perGain / 100))
        totOut = totOut + out
        output.append([f'{i}', f'{lastVal:0.2f}', f'{newGain:0.2f}', f'{out * (1 - 0.2697 - .005):0.2f}', f'{totOut:0.2f}', f'{totOut + lastVal:0.2f}', f'{noOut:0.2f}'])
        lastVal = lastVal + newGain - out


    print(tabulate.tabulate(output, headers="firstrow", tablefmt="fancy_grid"))


if __name__ == "__main__":
    main()
