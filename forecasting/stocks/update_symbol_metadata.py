help = '''

Download available symbols in the NASDAQ and NYSE exchanges.

Usage: python update_symbol_metadata.py

The script is barebones and does nothing fancy for you. It "updates"
the data by simply downloading it all again. Use with caution.

'''

import sys
import urllib
import pandas as pd


def get_all_symbols():
    '''
    Download symbol metadata for the NASDAQ and NYSE exchanges.
    '''
    for exchange in ['NASDAQ', 'NYSE']:
    
        dest = 'data/SYMBOLS_{exchange}.csv'.format(exchange=exchange)
        response = urllib.request.urlopen(
            'https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange={exchange}&render=download'.
            format(exchange=exchange)
        )
        fd = open(dest, 'w')
        fd.write(response.read().decode())
        fd.close()
    
        # some columns I don't care about. some data is suspect. maybe
        # there's a more elegant way to reformat the data, but this
        # was easiest for me.
        df = pd.read_csv(
            dest,
            usecols=['Symbol', 'Name', 'MarketCap', 'IPOyear', 'Sector', 'Industry']
        )
        df = df[df.MarketCap > 0] # entries with 0 marketcap are suspicious, remove
        df.to_csv(dest, index=False)


    return



if not len(sys.argv) == 1:
    print(help)
    sys.exit(1)


if __name__ == '__main__':
    get_all_symbols()
