import pandas as pd
import pandas_datareader.data as web
import datetime
import sqlite3


s = datetime.datetime(2010,1,1)
e = datetime.datetime(2016,6,12)
df = web.DataReader("078930.KS","yahoo",s,e)

df = df.rename({'Adj Close':'AdjClose'},axis = 'columns') #열이름에 띄어쓰기 있으면 안됨


con = sqlite3.connect("c:/Users/LG/kospi.db")
df.to_sql(name = '078930',con = con, if_exists = 'replace')

readed_df = pd.read_sql("SELECT * FROM '078930'",con, index_col = 'Date')
print(readed_df.head())

con.close()

