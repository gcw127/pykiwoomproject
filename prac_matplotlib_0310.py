import matplotlib.pyplot as plt
import pandas_datareader.data as web


sk_hynix = web.DataReader("000660.KS","yahoo")

fig = plt.figure(figsize=(12,8))

#subplot2grid( 전체 몇그리드인지, 왼쪽상단 시작 그리드, 몇그리드 걸칠건지 (행),열)
top_axes = plt.subplot2grid((4,4),(0,0),rowspan = 3, colspan=4)
bottom_axes = plt.subplot2grid((4,4),(3,0), rowspan = 1, colspan =4)
bottom_axes.get_yaxis().get_major_formatter().set_scientific(False) #큰값일때 e로 안표현되게 하기

top_axes.plot(sk_hynix.index, sk_hynix['Adj Close'],label='Adjusted Close')
bottom_axes.plot(sk_hynix.index, sk_hynix['Volume'])

plt.tight_layout() #객체들 각자 영역내에서 꽉차게 그리기
plt.show()