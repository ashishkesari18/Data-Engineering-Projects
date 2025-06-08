SELECT 
    sku,
    category,
    COUNT(*) AS total_orders,
    SUM(CAST(return_flag AS INT)) AS total_returns,
    ROUND(SUM(CAST(return_flag AS DOUBLE)) / COUNT(*), 2) AS return_rate,
    ARRAY_JOIN(ARRAY_AGG(DISTINCT return_reason), ', ') AS return_reasons
FROM refund_table
GROUP BY sku, category
HAVING ROUND(SUM(CAST(return_flag AS DOUBLE)) / COUNT(*), 2) > 0.15
ORDER BY return_rate DESC;
