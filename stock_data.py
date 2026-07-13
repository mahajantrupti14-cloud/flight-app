import yfinance as yf
import pandas as pd 
stocks = "AAPL MSFT GOOG"
data = yf.download(stocks, period="1y", group_by="ticker")
data.to_csv("data/stock_data.csv")
print("stock data downloaded successfully!")
