import datetime as dt
import os
import sys

import iexfinance as iex
import pandas as pd


def parse_args():

    #
    # get symbol metadata
    #
    available_symbols = [s['symbol'] for s in iex.get_available_symbols() if s['type'] in ['cs', 'etf']]
    
    # these symbols cause an exception in the API request and I don't
    # care enough to figure out if I should care about this exception
    # at the moment ... FIXME
    # available_symbols.remove('ALL-C*')
    # available_symbols.remove('ARNC-')
    # available_symbols.remove('BNGO')
    # available_symbols.remove('CMCTP')
    # available_symbols.remove('DTLA-')
    # available_symbols.remove('BNBUSDT')

    if len(sys.argv) == 2:
        requested_symbols = pd.read_csv(sys.argv[1]).Symbol.values
    elif len(sys.argv) == 1:
        requested_symbols = available_symbols
    else:
        # FIXME help
        raise ValueError()

    #
    # check availability
    #
    missing_symbols = set(requested_symbols) - set(available_symbols)
    if missing_symbols:
        print('Missing symbols {} from database. Skipping ...'.format(','.join(missing_symbols)))
        requested_symbols = list(set(requested_symbols) - missing_symbols)

    return requested_symbols


symbols = parse_args()
print('Retrieving data for all {} available symbols'.format(len(symbols)))


#
# get price data
#
blacklist = []
end = dt.date.today() - dt.timedelta(2)
for j, s in enumerate(symbols):

    sout = 'data/{}_TIME_SERIES_DAILY.csv'.format(s)
    if os.path.isfile(sout):
        start = (pd.read_csv(sout, parse_dates=[0]).date.max() + dt.timedelta(1)).date()
        header = False
    else:
        # should warn that no data exists
        start = end - dt.timedelta(365*5) # 5 years look back
        header = True

    # don't unnecessarily abuse server
    if (start - end).days >= 0:
        print('Skipping symbol {} ({}/{}). Already up to date.'.format(s, j, len(symbols)))
        continue

    try:
        df = iex.get_historical_data(s, start=start, end=end, output_format='pandas')
    except KeyError:
        blacklist.append(s)
        print(s)
        continue
    print('Retrieved {} new price records for symbol {} ({}/{}).'.format(len(df), s, j, len(symbols)))

    # write out
    # header: date,open,high,low,close,volume
    with open(sout, 'a') as f:
        df.to_csv(f, header=header)

print(blacklist)
