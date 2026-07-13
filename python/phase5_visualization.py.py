import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect("stock_data.db")
stock_df = pd.read_sql("SELECT * FROM stock_prices", conn, parse_dates=["date"])
conn.close()

# ---------------- FEATURE ENGINEERING ----------------
stock_df["daily_return"] = (stock_df["close_price"] - stock_df["open_price"]) / stock_df["open_price"]
stock_df["ma_20"] = stock_df.groupby("company")["close_price"].transform(lambda x: x.rolling(window=20).mean())
stock_df["ma_50"] = stock_df.groupby("company")["close_price"].transform(lambda x: x.rolling(window=50).mean())
stock_df["volatility_20"] = stock_df.groupby("company")["daily_return"].transform(lambda x: x.rolling(window=20).std())
stock_df["cumulative_return"] = stock_df.groupby("company")["daily_return"].transform(lambda x: (1 + x).cumprod())

# ---------------- VISUALIZATION ----------------

# 1. Closing Price with Moving Averages
for company in stock_df["company"].unique():
    company_data = stock_df[stock_df["company"] == company]
    plt.figure(figsize=(10,6))
    plt.plot(company_data["date"], company_data["close_price"], label="Close Price")
    plt.plot(company_data["date"], company_data["ma_20"], label="MA 20")
    plt.plot(company_data["date"], company_data["ma_50"], label="MA 50")
    plt.title(f"{company} - Closing Price with Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

# 2. Daily Return
plt.figure(figsize=(10,6))
for company in stock_df["company"].unique():
    plt.plot(stock_df[stock_df["company"] == company]["date"],
             stock_df[stock_df["company"] == company]["daily_return"], label=company)
plt.title("Daily Returns")
plt.xlabel("Date")
plt.ylabel("Return")
plt.legend()
plt.show()

# 3. Volatility (20-day rolling std)
plt.figure(figsize=(10,6))
for company in stock_df["company"].unique():
    plt.plot(stock_df[stock_df["company"] == company]["date"],
             stock_df[stock_df["company"] == company]["volatility_20"], label=company)
plt.title("20-Day Rolling Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility")
plt.legend()
plt.show()

# 4. Cumulative Return
plt.figure(figsize=(10,6))
for company in stock_df["company"].unique():
    plt.plot(stock_df[stock_df["company"] == company]["date"],
             stock_df[stock_df["company"] == company]["cumulative_return"], label=company)
plt.title("Cumulative Returns")
plt.xlabel("Date")
plt.ylabel("Cumulative Growth")
plt.legend()
plt.show()
