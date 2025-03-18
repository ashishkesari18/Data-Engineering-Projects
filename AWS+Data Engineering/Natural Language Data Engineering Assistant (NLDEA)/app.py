import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
from execute_query import run_athena_query, get_athena_query_results, generate_visualization_code, display_generated_chart
import io
import base64
import re
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def generate_query(natural_language):
    prompt = f"""
    Convert this into an SQL query for AWS Athena. 
    The table name is 'orders'. 
    The column for order totals can be calculated by multiplying the unit price and quantity.
    The column containing the product description is 'Description'.
    The column containing the country is 'Country'.
    Country names are case sensitive.
    When comparing dates, ensure to use the parse_datetime function to cast the date string to a timestamp. 
    If you are unsure of the table or column names, use the 'orders' table. 
    {natural_language}
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    generated_text = response.text

    sql_match = re.search(r"(```sql|```)(.*?)(```|$)", generated_text, re.DOTALL | re.IGNORECASE)
    if sql_match:
        sql_query = sql_match.group(2).strip()
    else:
        sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"]
        for keyword in sql_keywords:
            if keyword in generated_text.upper():
                sql_query = generated_text.strip()
                break
        else:
            sql_query = None

    if sql_query:
        sql_query = re.sub(r"^[^a-zA-Z0-9]+|[^a-zA-Z0-9;]+$", "", sql_query).strip()
        if not sql_query.endswith(';'):
            sql_query += ';'
        sql_query = sql_query.split(';')[0].strip() + ';'

        sql_query = sql_query.replace("description", "Description")
        sql_query = sql_query.replace("country", "Country")

    return sql_query

st.title("Natural Language Data Engineering Assistant")

user_input = st.text_input("Enter your query in plain English:")

if user_input:
    query = generate_query(user_input)
    if query:
        st.write("Generated SQL Query:", query)

        query_id = run_athena_query(query)

        if query_id:
            st.write(f"Query Running: {query_id}")
            result_df = get_athena_query_results(query_id)
            if result_df is not None:
                st.dataframe(result_df)
                if st.button("Generate Visualization"):
                    code = generate_visualization_code(result_df, user_input)
                    display_generated_chart(result_df, code)
            else:
                st.write("Query failed.")
        else:
            st.write("Failed to execute query.")
    else:
        st.write("Could not generate a valid SQL Query.")