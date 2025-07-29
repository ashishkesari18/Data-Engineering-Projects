-- 1. Count failed unlocks per driver
SELECT driver_id, COUNT(*) AS failed_attempts
FROM smartlock_access_logs
WHERE status = 'fail'
GROUP BY driver_id
ORDER BY failed_attempts DESC;

-- 2. Drivers with most late-night unlocks (after 9PM)
SELECT driver_id, COUNT(*) AS late_night_unlocks
FROM smartlock_access_logs
WHERE hour(timestamp) > 21
GROUP BY driver_id
ORDER BY late_night_unlocks DESC;

-- 3. Unlock attempts by region
SELECT region, COUNT(*) AS total_unlocks
FROM smartlock_access_logs
GROUP BY region
ORDER BY total_unlocks DESC;

-- 4. Total unlock attempts by hour
SELECT hour(timestamp) AS unlock_hour, COUNT(*) AS unlock_count
FROM smartlock_access_logs
GROUP BY unlock_hour
ORDER BY unlock_hour;

-- 5. Access type distribution by driver
SELECT driver_id, access_type, COUNT(*) AS access_count
FROM smartlock_access_logs
GROUP BY driver_id, access_type
ORDER BY driver_id, access_count DESC;
