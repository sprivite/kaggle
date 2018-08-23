help = '''

Download historical stock price data from alphavantage. To use, you
need to first claim an API key via:
  https://www.alphavantage.co/support/#api-key

NB: It turns out this API throttles requests to five per minute, so
I have to add a sleeping mechanism here for now, until I find a better
data source.

Usage: python update_price_data.py SYMBOLS APIKEY

where APIKEY is the path to a plain text file containing your API key
and SYMBOLS is a CSV-formatted file whose first column is the symbol
value you wish to download; the file is assumed to have a header and
the first row is therefore skipped.

The script is barebones and does nothing fancy for you. It "updates"
the data by simply downloading it all again via the API. Use with
caution.

Hint: you can get all historical data by running:
  python update_symbol_metadata.py
  python update_price_data.py <(cat data/SYMBOLS_NYSE.csv data/SYMBOLS_NASDAQ.csv) data/APIKEY.txt

'''

from collections import deque
import time
import sys
import urllib
import pandas as pd


def get_price_data(symbol, apikey, function, verbose=1):
    '''
    Get historical price data for a given symbol.

    '''

    dest = 'data/{symbol}_{function}.csv'.format(function=function, symbol=symbol)

    if verbose:
        print('Writing historical data for {symbol} to {dest} ...'.format(symbol=symbol, dest=dest))

    response = urllib.request.urlopen(
        'https://www.alphavantage.co/query=?outputsize=full&symbol={symbol}&apikey={apikey}&function={function}&datatype=csv'.
        format(symbol=symbol, apikey=apikey, function=function)
    )
    fd = open(dest, 'w')
    result = str(response.read().decode())
    if 'Information' in result:
        # something went wrong
        # despite my best effort to respect the API limits, I still get
        # angry server responses ... at this point, take a deep breath
        # and start again
        fd.close()
        print('Sleeping 60 seconds to respect API request limits ...')
        time.sleep(60)
        get_price_data(symbol, apikey, function, verbose)

    else:
        fd.write(result)
        fd.close()

    return


if not len(sys.argv) == 3:
    print(help)
    sys.exit(1)


# read symbols and API key
SYMBOLS, APIKEY = sys.argv[1:]
symbols = pd.read_csv(SYMBOLS, usecols=[0]).values[:, 0]
apikey = open(APIKEY, 'r').read()

# TODO: support other modes
function = 'TIME_SERIES_DAILY'


#
# query API for price data
#

# track times of last requests to avoid getting VOID responses
# according to the website, the limit is five requests per minute in
# practice, we have to stick a little bit below that; here I throttle
# to 4 requests per 65 seconds. It seems to keep the server happy.
max_requests = 4
time_buffer = 65
history = deque([-time_buffer]*max_requests, maxlen=max_requests)
t0 = time.time()
for symbol in symbols:


    tnow = time.time() - t0
    sleepy_time = time_buffer - (tnow - history[0])
    if sleepy_time > 0:
        print('Sleeping {} seconds to respect API request limits ...'.format(sleepy_time))
        time.sleep(sleepy_time)

    history.append(time.time() - t0)
    get_price_data(symbol, apikey, function)
