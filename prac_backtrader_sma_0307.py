from datetime import datetime
import backtrader as bt
import yfinance as yf
import locale


#한국시간 사용
locale.setlocale(locale.LC_ALL,'ko_KR')

class SmaCross(bt.Strategy):
    params = dict(
        pfast=5, #단기
        pslow=30 #장기
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period = self.p.pfast)
        sma2 = bt.ind.SMA(period = self.p.pslow)

       #크로스오버 시그널
        self.crossover = bt.ind.CrossOver(sma1,sma2)

        self.holding = 0

    def next(self): #기간동안 액션 취하기 위한 함수
        current_stock_price = self.data.close[0]

        if not self.position: #not in the market
            if self.crossover > 0:
                #매수 가능한 주식 수
                availble_stocks = self.broker.getcash() / current_stock_price
                self.buy(size = 1)

        elif self.crossover < 0 : #데드크로스
            self.close() #데드크로스일때 전량매도 , 하나씩 팔려면 sell(1)

    def notify_order(self, order): #주문체결될때 호출되는 함수
        if order.status not in [order.Completed]:
            return

        if order.isbuy():
            action = 'Buy'
        elif order.issell():
            action = 'Sell'

        stock_price = self.data.close[0] #주문체결될때 주식가격
        cash = self.broker.getcash() #보유현금
        value = self.broker.getvalue() #자산가치
        self.holding += order.size #보유주식 수

        print('%s[%d] holding[%d] price[%d] cash[%.f] value[%.2f]'
              % (action, abs(order.size), self.holding, stock_price, cash,value ))











cerebro = bt.Cerebro() #객체 바인딩
cerebro.broker.setcash(10000000) #가지고 있는 돈 설정
cerebro.broker.setcommission(0.002)  #수수료 0.2%

#데이터feed 생성
data = bt.feeds.PandasData(dataname=yf.download('036570.KS', '2018-01-01', '2022-03-04'))
cerebro.adddata(data)
cerebro.addstrategy(SmaCross)

start_value = cerebro.broker.get_value()
cerebro.run() #전부 실행
final_value = cerebro.broker.get_value() #현재 자산가치가져오기

print(' * start value : %s won' % locale.format_string('%d',start_value,
      grouping = True))
print(' * final value : %s won' % locale.format_string('%d', final_value, grouping = True ))
print(' * earning rate : %.2f %%' % ((final_value - start_value) / start_value *100.0))

cerebro.plot()



