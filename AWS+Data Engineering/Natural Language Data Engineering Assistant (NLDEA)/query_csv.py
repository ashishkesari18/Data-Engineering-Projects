import pandas as pd
import re

def clean_and_query_csv(csv_file, query, output_file=None):
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file, encoding='ISO-8859-1')

    df.columns = df.columns.str.strip().str.replace(r'[^\w\s]', '', regex=True)

    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).apply(lambda x: ''.join(char for char in x if char.isprintable()).strip())
            df[col] = df[col].apply(lambda x: re.sub(r'\s+', ' ', x))

    df['CustomerID'] = pd.to_numeric(df['CustomerID'], errors='coerce')
    df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

    print("Cleaned Columns in the CSV file:", df.columns)
    print("First few rows of the data:")
    print(df.head())

    try:
        result_df = df.query(query)
        if output_file: #save the file if a name is provided.
            df.to_csv(output_file, index=False)
            print(f"Cleaned data saved to {output_file}")
        return result_df
    except KeyError as e:
        print(f"KeyError: The column '{e.args[0]}' was not found in the data.")
        return None
    except Exception as e:
        print(f"An error occurred while querying: {e}")
        return None

if __name__ == "__main__":
    csv_file = "data.csv"
    query = "CustomerID == 17850.0 and UnitPrice > 2"
    output_file = "cleaned_data.csv"

    result_df = clean_and_query_csv(csv_file, query, output_file=output_file)

    if result_df is not None and not result_df.empty:
        print(result_df)
    else:
        print("No matching records found.")