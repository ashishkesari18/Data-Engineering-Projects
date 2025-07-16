import requests
import random
import time

# Replace with your actual API Gateway endpoint:
API_URL = 'https://572z6qg6yi.execute-api.us-east-1.amazonaws.com/cart-event'

users = [f"user_{i}" for i in range(1, 21)]
products = ['MACBOOK_PRO_2023', 'IPHONE_15', 'AIRPODS_MAX', 'PS5', 'NINTENDO_SWITCH']
events = ['cart_add', 'cart_remove', 'checkout_complete']
reasons = ['Too expensive', 'Found better deal', 'Changed mind', 'Prefer different color']

for _ in range(100):
    user = random.choice(users)
    product = random.choice(products)
    event_type = random.choices(events, weights=[0.5, 0.3, 0.2])[0]  # More add/remove than checkout

    payload = {
        "user_id": user,
        "product_id": product,
        "event_type": event_type
    }

    if event_type == 'cart_remove':
        payload['reason'] = random.choice(reasons)

    response = requests.post(API_URL, json=payload)
    print(f"Sent: {payload} → Status: {response.status_code}")
    time.sleep(0.5)  # Slow down to simulate real users






