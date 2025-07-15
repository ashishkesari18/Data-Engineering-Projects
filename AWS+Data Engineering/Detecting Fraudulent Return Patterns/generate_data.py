import pandas as pd
import numpy as np

np.random.seed(42)

#Generating Synthetic return data

df = pd.DataFrame({
    "customer_id": np.random.randint(1000, 2000, 10000),
    "product_id": np.random.randint(10000, 20000, 10000),
    "order_value": np.round(np.random.normal(100, 30, 10000), 2),
    "return_reason": np.random.choice(["Damaged", "Not Needed", "Wrong Item", "No Reason"], 10000),
    "return_count": np.random.poisson(2, 10000),
    "damaged_flag": np.random.choice([0, 1], 10000, p=[0.8, 0.2]),
    "days_since_last_return": np.random.randint(0, 180, 10000),
})

#Labeling as Fraud!!!

df['is_fraud'] = ((df['return_count']>4)&(df['damaged_flag']==1)).astype(int)

df.to_csv("synthetic_returns.csv", index= False)
print("Data saved as synthetic_returns.csv")