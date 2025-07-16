### 1. Top Abandoned Products

SELECT 
    productid, COUNT(*) AS abandon_count
FROM 
    cart_analytics_db.raw_events
WHERE 
    eventtype = 'cart_remove'
GROUP BY 
    productid
ORDER BY 
    abandon_count DESC
LIMIT 5;

### 2. Abandoned Carts (No Checkout)

WITH added AS (
  SELECT userid, productid
  FROM cart_analytics_db.raw_events
  WHERE eventtype = 'cart_add'
),
purchased AS (
  SELECT userid, productid
  FROM cart_analytics_db.raw_events
  WHERE eventtype = 'checkout_complete'
)
SELECT a.userid, a.productid
FROM added a
LEFT JOIN purchased p
  ON a.userid = p.userid AND a.productid = p.productid
WHERE p.productid IS NULL;
