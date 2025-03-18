import boto3
from botocore.exceptions import ClientError
import os
import pandas as pd
import google.generativeai as genai
import matplotlib.pyplot as plt
import io
import base64
import time
import re
import streamlit as st


os.environ["GOOGLE_API_KEY"] = "AIzaSyAW6257a2u2xH6od9v4q9q5_xdU_Dze9GU"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def run_athena_query(query):
    try:
        session = boto3.Session()
        client = session.client('athena', region_name='us-east-1')
        response = client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': 'nl_dea'},
            ResultConfiguration={'OutputLocation': 's3://nl-dea-results/'}
        )
        return response["QueryExecutionId"]
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

def get_athena_query_results(query_execution_id):
    client = boto3.client('athena', region_name='us-east-1')
    while True:
        response = client.get_query_execution(QueryExecutionId=query_execution_id)
        status = response['QueryExecution']['Status']['State']
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(1)
    if status == 'SUCCEEDED':
        result_location = response['QueryExecution']['ResultConfiguration']['OutputLocation']
        s3_client = boto3.client('s3')
        bucket_name = result_location.split('/')[2]
        key = '/'.join(result_location.split('/')[3:])
        try:
            obj = s3_client.get_object(Bucket=bucket_name, Key=key)
            result_df = pd.read_csv(obj['Body'])
            return result_df
        except ClientError as e:
            print(f"Error retrieving S3 object: {e}")
            return None
    else:
        return None

def generate_visualization_code(df, user_prompt):
    prompt = f"""Given this pandas DataFrame:\n{df.head()}\n\nUser asked for a visualization for: {user_prompt}.\n\nThink step by step. First determine the most appropriate chart type (bar, line, scatter, pie) for this data and user request. If no chart is appropriate, explain why and give the user suggestions on what kind of data is needed for a chart. Then generate Python code using Matplotlib or Seaborn to create that chart, only if a chart is appropriate. If no chart is appropriate, return "NO_CHART" and the explanation. \nOnly provide the python code, or "NO_CHART" and explanation, do not provide any other explanation. Ensure the generated Python code is syntactically correct and uses the matplotlib.pyplot and seaborn libraries. Do not include any extra characters before or after the code block."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    if response.candidates and response.candidates[0].finish_reason == 4:
        st.error("The model refused to generate a response due to potential copyright issues. Please rephrase your query.")
        return "COPYRIGHT_ERROR"
    return response.text

def display_generated_chart(df, code):
    if code == "COPYRIGHT_ERROR":
        return
    if "NO_CHART" in code:
        explanation = code.split("NO_CHART")[1].strip()
        st.write(explanation)
        return
    try:
        code = re.sub(r'```(?:python)?\n?', '', code)
        code = re.sub(r'```', '', code)
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        code = re.sub(r"hue='viridis'", "", code)
        code = re.sub(r"palette=([^,)]+)", r"legend=False", code)
        exec(code, globals(), locals())
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        st.image(f"data:image/png;base64,{img_base64}")
        plt.clf()
    except Exception as e:
        st.error(f"Error generating visualization: {e}")
        st.code(code, language='python')