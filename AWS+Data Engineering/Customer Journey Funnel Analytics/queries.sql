
WITH funnel AS (
  SELECT event_type, COUNT(DISTINCT user_id) AS users
  FROM customer_journey_events
  GROUP BY event_type
),
steps AS (
  SELECT 'ad_click' AS step_order, 'ad_click' AS step_name,
         (SELECT users FROM funnel WHERE event_type = 'ad_click') AS users
  UNION ALL
  SELECT 'product_view', 'product_view',
         (SELECT users FROM funnel WHERE event_type = 'product_view')
  UNION ALL
  SELECT 'cart_add', 'cart_add',
         (SELECT users FROM funnel WHERE event_type = 'cart_add')
  UNION ALL
  SELECT 'checkout', 'checkout',
         (SELECT users FROM funnel WHERE event_type = 'checkout')
),
base AS (
  SELECT * FROM steps
),
with_conversion AS (
  SELECT 
    step_name,
    users,
    (SELECT users FROM base WHERE step_name = 'ad_click') AS base_users
  FROM base
)
SELECT 
  step_name AS step,
  users,
  ROUND(100.0 * users / base_users, 2) AS conversion_rate_percent
FROM with_conversion;
