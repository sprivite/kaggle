help = '''

Download historical stock price data from alphavantage. To use, you
need to first claim an API key via:
  https://www.alphavantage.co/support/#api-key

Usage: python update_price_data.py SYMBOLS APIKEY

where APIKEY is the path to a plain text file containing your API
key and SYMBOLS is a newline-delimited plain text file containing
the list of symbols you want to download.

The script is barebones and does nothing fancy for you. It "updates"
the data by simply downloading it all again via the API. Use with
caution.

'''

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
    fd.write(str(response.read().decode()))
    fd.close()


if not len(sys.argv) == 3:
    print(help)
    sys.exit(1)


# read symbols and API key
SYMBOLS, APIKEY = sys.argv[1:]
symbols = list(filter(lambda x: x, open(SYMBOLS, 'r').read().split('\n')))
apikey = open(APIKEY, 'r').read()

# TODO: support other modes
function = 'TIME_SERIES_DAILY'

# query API
for symbol in symbols:
    get_price_data(symbol, apikey, function)
