import pandas as pd
import random
from faker import Faker
import uuid

fake = Faker()
num_rows = 100

data = {
    "customer_id": [str(uuid.uuid4())[:8] for _ in range(num_rows)],
    "name": [fake.name() for _ in range(num_rows)],
    "email": [fake.email() for _ in range(num_rows)],
    "phone": [fake.phone_number() for _ in range(num_rows)],
    "region": [random.choice(["Texas", "California", "Florida", "New York", "Washington"]) for _ in range(num_rows)],
    "total_sales": [round(random.uniform(50.0, 1000.0), 2) for _ in range(num_rows)]
}

df = pd.DataFrame(data)
df.to_csv("sales_data.csv", index=False)
print("sales_data.csv generated successfully.")
