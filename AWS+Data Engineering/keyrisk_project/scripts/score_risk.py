import pandas as pd

def score_driver_risk(df):
    scores = {}
    for driver in df['driver_id'].unique():
        driver_logs = df[df['driver_id'] == driver]
        fail_count = len(driver_logs[driver_logs['status'] == 'fail'])
        total = len(driver_logs)
        risk_score = round((fail_count / total) * 100, 2)
        scores[driver] = risk_score
    return scores

if __name__ == "__main__":
    df = pd.read_csv("data/smartlock_access_logs.csv")
    scores = score_driver_risk(df)
    for driver, score in scores.items():
        print(f"Driver {driver} Risk Score: {score}%")
