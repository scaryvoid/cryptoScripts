#!/home/scaryvoid/venv/cryptoscriptsenv/bin/python

# looking into depth of dips


import argparse, os, sys, datetime, tabulate


def main():
    parser = argparse.ArgumentParser(description='Look at depths of dips.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('filepath', help='File to analize.')
    parser.add_argument('-s', metavar='<startdate>', nargs=1, default=['2001-01-01'], help='Day to start analizing (example: 2001-01-01).')
    args = parser.parse_args()

    dates = []
    closes = []
    lows = []
    if not os.path.exists(args.filepath):
        sys.exit()

    with open(args.filepath, 'r') as f:
        for line in f:
            if "Date" in line:
                continue

            date, op, high, low, close, adjClose, vol = line.split(',')
            if "null" in close or "null" in low:
                continue

            try:
                startdate = datetime.datetime.strptime(args.s[0], "%Y-%m-%d")
            except ValueError:
                print("Error: invalid date")
                sys.exit()

            datestamp = datetime.datetime.strptime(date, "%Y-%m-%d")
            if datestamp < startdate:
                continue

            dates.append(date)
            closes.append(close)
            lows.append(low)

    prevClose = 0
    changes = []
    for date, close, low in zip(dates, closes, lows):
        if float(prevClose) == 0:
            prevClose = close
            continue

        change = float(prevClose) - float(low)
        changes.append(change)
        prevClose = close


    for days in [1, 2, 7, 30]:
        text = [["Days", "Dip %", "# Dips", "Avg %", "Profit %", "Chance Day %", "Chance Incident %"]]
        for dipMin in range(5, 100, 5):
            dips = []
            last = 0
            incidentDates = []
            for x, change in enumerate(changes):
                amtDip = (float(max(changes[x:x+days])) / float(closes[x])) * 100
                if amtDip >= float(dipMin):
                    dips.append(amtDip)
                    last = x
                    d = dates[changes.index(max(changes[x:x+days]))]
                    if d not in incidentDates:
                        incidentDates.append(d)

            try:
                avg = sum(dips)/len(dips)
            except ZeroDivisionError:
                avg = 0

            try:
                chanceA = len(dips) / len(changes) * 100
                chanceB = len(incidentDates) / (len(changes) / days) * 100
            except ZeroDivisionError:
                chanceA = 0
                chanceB = 0

            profit = (len(incidentDates) * dipMin) - (0.5 * len(incidentDates))
            text.append([f'{days}', f'{dipMin}', f'{len(incidentDates)}', f'{round(avg)}', f'{round(profit)}', f'{round(chanceA, 2)} ({len(dips)}/ {len(changes)})', f'{round(chanceB, 2)} ({len(incidentDates)}/{len(changes) / days:.2f})'])

        print(tabulate.tabulate(text, headers="firstrow", tablefmt="fancy_grid"))


if __name__ == "__main__":
    main()
