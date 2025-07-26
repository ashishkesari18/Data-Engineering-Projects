-- 1. Total customers and revenue by region (masked data)
SELECT region, COUNT(*) AS total_customers, SUM(total_sales) AS revenue
FROM sales_masked
GROUP BY region;

-- 2. Average order value per region
SELECT region, AVG(total_sales) AS avg_order_value
FROM sales_masked
GROUP BY region;

-- 3. Top 5 highest spending customers (PII masked)
SELECT customer_id, name, total_sales
FROM sales_masked
ORDER BY total_sales DESC
LIMIT 5;

-- 4. Distribution of total sales
SELECT 
  CASE 
    WHEN total_sales < 100 THEN 'Under $100'
    WHEN total_sales >= 100 AND total_sales <= 500 THEN '$100-$500'
    ELSE 'Over $500'
  END AS sales_range,
  COUNT(*) AS customer_count
FROM sales_masked
GROUP BY 
  CASE 
    WHEN total_sales < 100 THEN 'Under $100'
    WHEN total_sales >= 100 AND total_sales <= 500 THEN '$100-$500'
    ELSE 'Over $500'
  END;
-- 5. Query to verify PII masking is applied
SELECT DISTINCT email, phone
FROM sales_masked
LIMIT 10;
