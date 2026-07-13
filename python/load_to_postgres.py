
import os
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine

username = os.environ.get("PGUSER", "postgres")
password = os.environ.get("PGPASSWORD", "7821029949")
host = os.environ.get("PGHOST", "localhost")
port = os.environ.get("PGPORT", "5432")
database = os.environ.get("PGDATABASE", "postgres")

try:
    engine = create_engine(
        f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
    )
    engine.connect()
    print(f"Connected to PostgreSQL at {host}:{port}/{database} as {username}.")
except Exception as exc:
    print(
        f"Warning: Unable to connect to PostgreSQL at {host}:{port}/{database} as {username}: {exc}\nUsing local SQLite fallback for demonstration."
    )
    engine = create_engine("sqlite:///stock_data.db")
    print("Connected to SQLite database 'stock_data.db'.")

stocks = ["AAPL", "MSFT", "TSLA", "RELIANCE.NS", "TCS.NS"]
is_sqlite = engine.dialect.name == "sqlite"
_sqlite_table_created = False

for stock in stocks:
    df = yf.download(stock, period="1y")
    df = df.reset_index()
    # If yfinance returns MultiIndex columns (ticker in second level), drop the extra level
    if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)
    df["company"] = stock
    df = df.rename(columns={
        "Open": "open_price",
        "High": "high_price",
        "Low": "low_price",
        "Close": "close_price",
        "Volume": "trading_volume",
        "Date": "date",
    })

    df = df[[
        "company",
        "date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "trading_volume",
    ]]

    # When using SQLite fallback, ensure the table schema is created cleanly on first insert
    if is_sqlite and not _sqlite_table_created:
        to_sql_if_exists = "replace"
        _sqlite_table_created = True
    else:
        to_sql_if_exists = "append"

    df.to_sql(
        "stock_prices",
        engine,
        if_exists=to_sql_if_exists,
        index=False,
    )

    print(f"Inserted {len(df)} rows for {stock}.")
