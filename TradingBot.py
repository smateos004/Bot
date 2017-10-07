import pandas
import utils
import TA_pylib
import matplotlib.pyplot as plt
from utils import *
from TA_pylib import *
WAIT = 0
BUY = 1
SELL = 2
POLONIEX_COMMISSION = 0.0021
PROFITS = 0.5
MONEY = 1000
RISK = 1
MAGIC_FACTOR = 1.8
class Trader:  
    _position = WAIT
    _position_ant = WAIT
    _order = WAIT
    _order_ant = WAIT
    last_buy_price = 0
    last_sell_price = 0
    def __init__(self):
        self._position = WAIT
        self._position_ant = WAIT
        self._order = WAIT
    def add_buy_cond(self,buy_cond,enable = True):
        if(enable & buy_cond & (self._position == WAIT) & (self._order != BUY)):
            self._order = BUY
    def add_sell_cond(self,sell_cond,enable = True):
        if(enable & sell_cond & (self._position == BUY) & (self._order != SELL)):
            self._order = SELL
    def run_order(self,price):
        self._position_ant = self._position 
        if(self._order == BUY):
            self.last_buy_price = price
            self._position = self._order
        if(self._order == SELL):
            self.last_sell_price = price
            self._position = WAIT
        self._order_ant =  self._order
        self._order = WAIT     
        return self._order_ant

class Wallet:
    _risk = 0
    money = 0
    stocks = 0
    _commission = 0
    _risk_threshold = 0
    _position = WAIT
    def __init__(self,money,risk,commission = 0.0025, init_stocks = 0):
        self.money = money
        self._risk = risk
        self._commission = commission
        self.stocks = init_stocks
        self._risk_threshold = self.money * (1 - self._risk)
        self._position = WAIT
    def place_position(self, order, price, percentage = 1, enable = True):
        if(enable):
            if(order == BUY):
                self.stocks = ((self.money * percentage) * (1 - self._commission)) / price
                self._risk_threshold = self.money * (1 - self._risk)
                self.money = (self.money * (1 - percentage) * (1 - self._commission))
                self._position = BUY
            if(order == SELL):
                self.money = self.stocks * percentage * price * (1 - self._commission)
                self.stocks = (self.stocks * (1 - percentage))
                self._position = WAIT

    def is_risk(self,price):
        if(self._position == BUY):
            if((self.stocks * price) <= self._risk_threshold ):
                return True
            else:
                return False
        else:
            return False


ethereum_trader = Trader()
ethereum_wallet = Wallet(MONEY ,RISK ,commission = POLONIEX_COMMISSION)

##VOLCANDO CSV EN UN DATAFRAME
ethusd_df = get_csv_data(['ethusd'],"C:\GitProjects\TradingBot\CSV")


##CALCULANDO MACD, SIGNAL Y DIFFERENCE

ethusd_df = MA(ethusd_df,5)
ethusd_df = BBANDS2(ethusd_df,5)
ethusd_df = EMA(ethusd_df,15)
ethusd_df = MA(ethusd_df,26)
ordenes = np.zeros(ethusd_df['close'].size)


for i in range (1 , ethusd_df['close'].size):
    pot_commission = ((ethereum_wallet.money * ethereum_wallet._commission) / (ethereum_wallet.money / ethusd_df['close'][i]))
    ethereum_trader.add_buy_cond((ethusd_df['close'][i]) < (ethusd_df['MA_5'][i] - pot_commission - PROFITS))
    ethereum_trader.add_sell_cond((ethusd_df['close'][i]) > (ethereum_trader.last_buy_price + ethusd_df['close'][i]  * MAGIC_FACTOR * POLONIEX_COMMISSION + PROFITS))
    ethereum_trader.add_sell_cond(ethereum_wallet.is_risk(ethusd_df['close'][i]))
    
    ordenes[i] = ethereum_trader.run_order(ethusd_df['close'][i])
    ethereum_wallet.place_position(ordenes[i], ethusd_df['close'][i])
    #print(ordenes[i])
    if(ordenes[i] == BUY):
        print("Precio Compra: "+str(ethereum_trader.last_buy_price))
        print("EUROS: "+str(ethereum_wallet.money))
        print("\n")
    if(ordenes[i] == SELL):
        print("Precio Venta: "+str(ethereum_trader.last_sell_price))
        print("EUROS: "+str(ethereum_wallet.money))
        print("\n")
print("Rentabilidad HOLD:")
print(ethusd_df['close'][ethusd_df['close'].size - 1]/ethusd_df['close'][0])
print("\n")
plt.figure(15)
for orden in range (0,ordenes.size):
    if(ordenes[orden] == 1):
        plt.axvline(ethusd_df.index[orden],color='g')
    if(ordenes[orden] == 2):
        plt.axvline(ethusd_df.index[orden],color='k')
plt.plot(ethusd_df.index,ethusd_df['close'].values,label = 'close')
plt.plot(ethusd_df.index,ethusd_df['UpperBand_5'].values,'r',label = 'UpperBand')
plt.plot(ethusd_df.index,ethusd_df['LowerBand_5'].values,'r',label = 'LowerBand')
plt.plot(ethusd_df.index,ethusd_df['MA_5'].values,'b',label = 'SMA_5')

plt.legend(loc='best')
plt.show()


plt.figure(16)
plt.plot(ethusd_df.index,ethusd_df['close'].values,label = 'close')
plt.plot(ethusd_df.index,ethusd_df['MA_26'].values,'g',label = 'SMA_7')
plt.plot(ethusd_df.index,ethusd_df['EMA_15'].values,'r',label = 'EMA_3')
plt.legend(loc='best')
plt.show()
