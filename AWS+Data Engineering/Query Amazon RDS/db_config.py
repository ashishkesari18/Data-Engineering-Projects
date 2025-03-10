import psycopg2

# AWS RDS Configuration
DB_HOST = "amazon-db.**************.rds.amazonaws.com"  # Your RDS hostname
DB_NAME = "****"  # The database you want to connect to (make sure it's the correct name)
DB_USER = "****"       # Your RDS username
DB_PASS = "***"  # Your RDS password
DB_PORT = "5432"       # Default port for PostgreSQL

# Function to Connect to PostgreSQL & Execute Queries
def connect_postgresql():
    try:
        # Attempting to connect to the specific database `amazon-db`
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,  # Ensure we are connecting to `amazon-db` here
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        print("Connected to Amazon RDS PostgreSQL database!")
        return conn  # Return the connection object here
    except Exception as e:
        print("Error:", e)
        return None
