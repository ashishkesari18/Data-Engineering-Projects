from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_logs(num=100):
    driver_ids = ['DR' + str(fake.random_number(digits=3, fix_len=True)) for _ in range(10)]
    regions = ['Seattle', 'Portland', 'San Francisco', 'Los Angeles']
    doors = ['DOOR' + str(i).zfill(2) for i in range(1, 6)]
    statuses = ['success', 'fail']
    access_types = ['scheduled', 'manual']

    logs = []
    now = datetime.now()
    for i in range(num):
        ts = now - timedelta(minutes=random.randint(0, 10000))
        logs.append({
            "unlock_id": i + 1,
            "timestamp": ts.strftime('%Y-%m-%d %H:%M:%S'),
            "driver_id": random.choice(driver_ids),
            "door_id": random.choice(doors),
            "region": random.choice(regions),
            "status": random.choices(statuses, weights=[0.85, 0.15])[0],
            "access_type": random.choice(access_types)
        })
    return pd.DataFrame(logs)

if __name__ == "__main__":
    df = generate_logs(100)
    df.to_csv("data/smartlock_access_logs.csv", index=False)
    print("✅ smartlock_access_logs.csv generated successfully.")
