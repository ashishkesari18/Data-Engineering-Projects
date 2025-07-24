import pandas as pd

def run_glue_etl(input_path, output_path):
    df = pd.read_csv(input_path)

    # Cleaning and transformation
    df.dropna(subset=["user_id", "event_type"], inplace=True)
    df["event_type"] = df["event_type"].str.lower().str.strip()
    df["user_segment"] = df["user_segment"].fillna("Unknown")

    # Write transformed data
    df.to_csv(output_path, index=False)
    print(f"Glue job simulated: cleaned data written to {output_path}")
