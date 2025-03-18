import google.generativeai as genai
import os

os.environ["GOOGLE_API_KEY"] = "***********"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def generate_query(natural_language):
    prompt = f"Convert this into an SQL query: {natural_language}"
    
    # Use an available model
    model = genai.GenerativeModel("gemini-2.0-flash")  # Faster response
    # model = genai.GenerativeModel("gemini-2.0-pro-exp")  # Higher quality output
    
    response = model.generate_content(prompt)
    return response.text

query = generate_query("Show top 5 customers by total purchase in the last 6 months")
print(query)
