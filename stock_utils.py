import asyncio
import aiofiles
import aiohttp
import requests
import pandas as pd
import io
from datetime import date
import json

# get all liquid stocks: vol>4M


def fetch_liquid_stocks(vol=4_000_000, *, min_price=5, avg_vol=None):
    avg = f'&min_avgvol={int(avg_vol / 1000)}' if avg_vol else ''
    URL_AJAX = f"https://www.stock-watcher.com/screener/default/result/ajax?&min_price={min_price}&min_curvol={vol}{avg}&geo=USA&Exchange=1,2&etf=2&row=10000&order=chp&asc=1&page=1&trow=fortickers&CSRF_TOKEN=4ceb139282afc1ca5ec1947900af56df85d86952&_=1589233508250"
    res = requests.get(URL_AJAX)

    if res.status_code == 200:
        return res.json()['records']['ticker']


def create_traidingview_watchlist(symbols, filename):
    if not symbols:
        raise ValueError("Ticker's list is empty")

    with open(filename, 'w') as f:
        f.write(','.join(symbols))


async def fetch_historical_data_alhavantage(symbol, api, session, save_to_file=False):
    URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&timeseries=5&apikey={api}&datatype=csv"
    async with session.get(URL, allow_redirects=True) as response:
        data = await response.read()
        filename = f"data/{symbol}_{str(date.today())}.csv"
        if save_to_file:
            async with aiofiles.open(filename, mode='wb') as f:
                await f.write(data)

        df = pd.read_csv(io.BytesIO(data), encoding='utf8', sep=',')
        df.rename(columns={'timestamp': 'date'})
        return df
    # df = pd.read_csv(URL)

    # if df.iloc[:, 0].str.contains('"Error Message"').sum():
    #     print("Symbol: {} \n{}".format(symbol, df.iloc[0, 0]))
    #     return pd.DataFrame()

    # if df.iloc[:, 0].str.contains('"Note"').sum():
    #     print("Symbol: {} \n{}".format(symbol, df.iloc[0, 0]))
    #     return pd.DataFrame()

    # return df.iloc[::-1].round(2)


async def fetch_historical_data_financialmodelingprep(symbol, api, session, save_to_file=False):
    # Returns json object
    URL = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={api}"
    async with session.get(URL, allow_redirects=True) as response:
        data = await response.json()
        filename = f"data/{symbol}_{str(date.today())}.csv"
        df = pd.DataFrame(data['historical'])
        df.rename(columns={'timestamp': 'date'})
        df =df[['date','open', 'high', 'low', 'close']]
        if save_to_file:
            async with aiofiles.open(filename, mode='wb') as f:
                await f.write(df.to_csv(index=False).encode('utf-8'))
        return df

    
def get_ignored_symbols(default_file='ignored'):
    with open(default_file) as f:
        return [l.strip() for l in f.readlines()]