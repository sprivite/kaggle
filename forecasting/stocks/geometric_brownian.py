#
# Compute the parameters of a geometric Brownian noise model for a
# number of stock symbols over the last N days and output a ranked
# list of symbols with highest projected growth. See corresponding
# notebook for a bit of the theory.
#
# Usage:
#    python geometric_brownian.py SYMBOLS NDAYS
#
#
# TODO:
#    implement parameter estimation error estimates
#    add cool plots
#



import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('agg')
mpl.rcParams['figure.figsize'] = (12, 8)
from matplotlib import pyplot as plt


SYMBOLS = sys.argv[1]
window = int(sys.argv[2])

symbols = pd.read_csv(SYMBOLS, usecols=[0]).values[:, 0]
stats = pd.DataFrame(index=symbols, columns=['mu', 'sigma', 'net_drift'])
for symbol in symbols:
    print(symbol,)
    stocks = pd.read_csv(
        'data/{}_TIME_SERIES_DAILY.csv'.format(symbol)
    ).sort_values('timestamp', ascending=True).set_index('timestamp')


    # compute fractional price changes
    Pt = stocks.open.values
    PtPlusOne = Pt[1:]
    Pt = Pt[:-1]
    pt = (PtPlusOne - Pt) / Pt

    # take a window of samples to estimate "local" mu and sigma
    # I assume these are not time independent
    # since I'm using smallish samples here, would be really nice to supplement with
    # error estimates TODO
    mu, sigma = [], []
    mu = pt[-window:].mean()
    sigma = pt[-window:].std()
    stats.loc[symbol].mu = mu
    stats.loc[symbol].sigma = sigma
    stats.loc[symbol].net_drift = mu - sigma**2 / 2
    print(stats.loc[symbol].as_matrix())

print(stats.sort_values('net_drift', ascending=False))
