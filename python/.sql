
SELECT company, ROUND(AVG(close_price), 2) AS avg_close
FROM stock_prices
GROUP BY company
ORDER BY avg_close DESC;


SELECT company, MAX(close_price) AS max_close
FROM stock_prices
GROUP BY company
ORDER BY max_close DESC;


SELECT DISTINCT ON (company) company, date, close_price
FROM stock_prices
ORDER BY company, date DESC;

SELECT company, DATE_TRUNC('month', date) AS month, SUM(trading_volume) AS total_volume
FROM stock_prices
GROUP BY company, month
ORDER BY company, month;


SELECT product_name, SUM(revenue) AS total_revenue
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC;

SELECT category, ROUND(AVG(revenue), 2) AS avg_revenue
FROM sales
GROUP BY category
ORDER BY avg_revenue DESC;

SELECT product_name, SUM(revenue) AS total_revenue
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 1;


SELECT DATE_TRUNC('month', sale_date) AS month, SUM(revenue) AS monthly_revenue
FROM sales
GROUP BY month
ORDER BY month;
