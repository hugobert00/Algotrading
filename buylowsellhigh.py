
#Setting up the data reader using - DataReader
#arg1 -> symbol (ex: GOOG for Google)
#arg2 -> source for retrieving the data & range of days to get the data 
#arg3 -> the starting data from which to fetch historical data 
#arg4 -> the end of the data for the historical data series 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from pandas_datareader import data 

#First day 
start_date = '2014-01-01'
#Last day 
end_date = '2018-01-01'
#We call the function DataReader from the class data 
goog_data = data.DataReader('GOOG', 'yahoo', start_date, end_date)

print(goog_data)
pd.set_option('display.width', 1000)

#available data are: 
#'High' -> The highest price of the stock on that trading day 
#'Low' -> The lowest price of the stock on that trading day 
#'Close' -> The price of the stock at the closing time 
#'Open' -> The price of the stock at the begining of the trading day(closing price of the previous trading day)
#'Volume' -> How many stocks were traded
#'Adj Close' -> The closing price of the stock that adjusts the price for corporate actions. 
#This price takes into account the stock splits and dividends. 

goog_data_signal = pd.DataFrame(index = goog_data_signal.index)
goog_data_signal['Price'] = goog_data['Adj Close']
goog_data_signal['daily_difference']= goog_data_signal['price'].diff()
print(goog_data_signal.head())

goog_data_signal['signal'] = 0.0
#reading the column we have 1 when we need to but and 0 when we need to sell
goog_data_signal['signal']= np.where(goog_data_signal['daily_difference']> 0, 1.0, 0.0)

print(goog_data_signal.head())

#we set up a limit in the number of orders and positions on the market
#in a purpose of simplification, i t is impossible to buy or sell
#more than one time consecutively 

goog_data_signal['positions']= goog_data_signal['signal'].diff()
print(goog_data_signal.head())

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel = 'Google price in $')
#plot of the range of days we initially chose
goog_data_signal['price'].plot(ax=ax1, color ='r', lw=2.)

#we draw an up arrow when we buy one share
ax1.plot(goog_data_signal.loc[goog_data_signal.positions == 1.0].index,
         goog_data_signal.price[goog_data_signal.positions == 1.0],
         '^', markersize=5, color='m')

#we draw a down arrow when we sell one share
ax1.plot(goog_data_signal.loc[goog_data_signal.positions == -1.0].index,
         goog_data_signal.price[goog_data_signal.positions == -1.0],
         'v', markersize=5, color='k')

plt.show()

#==========================
#Backtesting -> intégration 
#==========================
#PnL 
#Net Profit (Net PnL --> includes fees)
#Exposure -> capital exposed (or nominal used)
#Number of trades
#Annualized returns 
#Sharpe ratio 

#construction of a portfolio w GOOG stocks and bonds
initial_capital = float(1000.0) #<- initial capital of 1,000.00 USD 
positions = pd.DataFrame(index = goog_data_signal.index).fillna(0.0)
portfolio = pd.DataFrame(index = goog_data_signal.index).fillna(0.0)

#storing positions 
positions['GOOG']= goog_data_signal['signal']

#storing of the amout of positions in the portfolio
portfolio['positions']= (positions.multiply(goog_data_signal['price'], axis=0))
#computation of the non-invested in stock money(cash)
portfolio['cash']= initial_capital - (positions.diff().multiply(goog_data_signal['price'], axis=0)).cumsum()
#total investment = position + cahs holdings 
portfolio['total']= portfolio['positions']+portfolio['cash']

#plot of the strategy -> to be insert 






