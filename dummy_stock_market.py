import pandas_datareader as pdr
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
import os
from datetime import date

os.environ['TIINGO_API_KEY']='ba84458e3ebffd6ef866b6e0ed5a8cf2de9c21dc'
TIINGO_API_KEY='ba84458e3ebffd6ef866b6e0ed5a8cf2de9c21dc'
msft_df = pdr.get_data_tiingo('MSFT', api_key=os.getenv(TIINGO_API_KEY))
last_close = msft_df.tail(1).close
volume = msft_df.tail(1).volume
open_price =  msft_df.tail(1).open
highprice = msft_df['high'].tail(1)
lowprice = msft_df['low'].tail(1)


api_key = 'NXMA9QIUL2F5YT4P'
ts = TimeSeries(key=api_key, output_format='pandas')
data,metadata = ts.get_intraday(symbol='MSFT', interval='1min',outputsize='full')
current_price = data['4. close'][:1]