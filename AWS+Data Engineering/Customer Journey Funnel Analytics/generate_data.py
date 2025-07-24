
import pandas as pd
import random
from datetime import datetime, timedelta

user_ids = [f"U{str(i).zfill(4)}" for i in range(1, 501)]
event_types = ["ad_click", "product_view", "cart_add", "checkout"]
devices = ["mobile", "desktop", "tablet"]
sources = ["facebook", "google", "instagram", "twitter", "linkedin"]

data = []
for user_id in user_ids:
    base_time = datetime(2025, 7, 22, random.randint(8, 20), random.randint(0, 59), random.randint(0, 59))
    device = random.choice(devices)
    source = random.choice(sources)

    journey = []
    for i, event in enumerate(event_types):
        if random.random() < 0.85:
            journey.append((user_id, event, base_time + timedelta(minutes=i*random.randint(1, 3)), device, source))
        else:
            break
    data.extend(journey)

df = pd.DataFrame(data, columns=["user_id", "event_type", "timestamp", "device", "source"])
df.to_csv("customer_journey_events.csv", index=False)
