import datetime
import pandas_datareader.data as web

import mplfinance as mpf

s = datetime.datetime(2016, 3, 1)
e = datetime.datetime(2016, 3, 31)

sk_hynix = web.DataReader("000660.KS", "yahoo", s, e)

mc = mpf.make_marketcolors(up='r', down='b')
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(sk_hynix, type="candle", mav=(3, 6, 9), volume=True, style=s)