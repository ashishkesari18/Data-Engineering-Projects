-- 1. Unoptimized Query (Flat Table)
SELECT COUNT(*) FROM click_logs.click_logs_flat
WHERE region = 'Texas' AND event_date = DATE '2025-07-22';

-- 2. Optimized Query (Partitioned Table)
SELECT COUNT(*) FROM click_logs.click_logs_partitioned
WHERE region = 'Texas' AND event_date = DATE '2025-07-22';

-- 3. Compare total user visits per region (Flat Table)
SELECT region, COUNT(*) AS total_visits
FROM click_logs.click_logs_flat
GROUP BY region
ORDER BY total_visits DESC;

-- 4. Compare total user visits per region (Partitioned Table)
SELECT region, COUNT(*) AS total_visits
FROM click_logs.click_logs_partitioned
GROUP BY region
ORDER BY total_visits DESC;

-- 5. Hourly visits for a specific day (Flat Table)
SELECT hour(timestamp) AS hour_of_day, COUNT(*) AS total_clicks
FROM click_logs.click_logs_flat
WHERE event_date = DATE '2025-07-22'
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- 6.Distinct pages visited by region (Partitioned Table)
SELECT region, COUNT(DISTINCT page) AS unique_pages
FROM click_logs.click_logs_partitioned
GROUP BY region;
