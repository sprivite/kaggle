import datetime as dt
import os
import sys

import iexfinance as iex
import pandas as pd


#
# get symbol metadata
#
available_symbols = [s['symbol'] for s in iex.get_available_symbols()]
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
print('Retrieving data for all {} available symbols'.format(len(requested_symbols)))


#
# get price data
#
end = dt.date.today()
for s in requested_symbols[:10]:

    sout = 'data/{}_TIME_SERIES_DAILY.csv'.format(s)
    if os.path.isfile(sout):
        df0 = pd.read_csv(sout, parse_dates=[0]).set_index('date')
        start = df0.index.max() + dt.timedelta(1)
    else:
        # should warn that no data exists
        df0 = pd.DataFrame()
        start = end - dt.timedelta(365*5) # 5 years look back

    df = iex.get_historical_data(s, start=start, end=end, output_format='pandas')
    print('Retrieved {} new price records for symbol {}.'.format(len(df), s))

    # merge
    df = pd.concat([df0, df])
    assert df.index.is_unique

    # write
    df.to_csv(sout)
