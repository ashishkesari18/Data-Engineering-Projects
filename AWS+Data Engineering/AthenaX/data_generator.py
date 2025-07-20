import pandas as pd
import random
from faker import Faker
from datetime import datetime

fake = Faker()

def generate_hr_signals(num_records=1000000):
    signal_types = ['promotion_flag', 'manager_feedback', 'mentorship_completion', 'leadership_score']
    data = []

    for _ in range(num_records):
        employee_id = random.randint(10000, 99999)
        signal_type = random.choice(signal_types)
        timestamp = fake.date_time_between(start_date='-2y', end_date='now')
        value = ''

        if signal_type == 'promotion_flag':
            value = random.choice(['promoted', 'not_promoted'])
        elif signal_type == 'manager_feedback':
            value = random.choice(['positive', 'neutral', 'negative'])
        elif signal_type == 'mentorship_completion':
            value = random.choice(['completed', 'in_progress', 'not_started'])
        elif signal_type == 'leadership_score':
            value = round(random.uniform(1.0, 5.0), 2)

        data.append([employee_id, signal_type, timestamp.strftime("%Y-%m-%d %H:%M:%S"), value])

    df = pd.DataFrame(data, columns=['employee_id', 'signal_type', 'timestamp', 'value'])
    df.to_csv('athenax_hr_signals.csv', index=False)
    print(" HR signal data generated → athenax_hr_signals.csv")

if __name__ == "__main__":
    generate_hr_signals()
