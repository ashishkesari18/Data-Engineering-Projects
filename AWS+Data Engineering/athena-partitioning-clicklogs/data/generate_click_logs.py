import pandas as pd
import random
from faker import Faker
import uuid

fake = Faker()
num_rows = 500

data = {
    "event_date": [fake.date_between(start_date='-15d', end_date='today') for _ in range(num_rows)],
    "region": [random.choice(["Texas", "California", "New York", "Florida", "Washington"]) for _ in range(num_rows)],
    "user_id": [str(uuid.uuid4())[:8] for _ in range(num_rows)],
    "page": [random.choice(["Home", "Product", "Search", "Cart", "Checkout"]) for _ in range(num_rows)],
    "timestamp": [fake.date_time_between(start_date='-15d', end_date='now') for _ in range(num_rows)]
}

df = pd.DataFrame(data)
df.to_csv("click_logs.csv", index=False)
print("✅ click_logs.csv generated successfully.")
