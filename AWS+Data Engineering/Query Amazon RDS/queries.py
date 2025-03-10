from db_config import connect_postgresql

def run_postgresql_queries():
    try:
        
        conn = connect_postgresql()

        if conn is None:
            print("Failed to connect to the database. Exiting.")
            return  # Exit the function if the connection is not successful

        cursor = conn.cursor()

        # Create Amazon Employees Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS amazon_employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                department VARCHAR(50),
                role VARCHAR(100)
            );
        """)

        # Create Amazon Products Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS amazon_products (
                id SERIAL PRIMARY KEY,
                product_name VARCHAR(255),
                category VARCHAR(100),
                price DECIMAL(10, 2),
                rating FLOAT
            );
        """)
        conn.commit()
        print("Tables Created Successfully")

        # Insert Employee Data
        cursor.execute("INSERT INTO amazon_employees (name, age, department, role) VALUES ('Jeff Bezos', 60, 'Executive', 'Founder');")
        cursor.execute("INSERT INTO amazon_employees (name, age, department, role) VALUES ('Andy Jassy', 55, 'Management', 'CEO');")
        cursor.execute("INSERT INTO amazon_employees (name, age, department, role) VALUES ('Jane Doe', 30, 'Engineering', 'Software Engineer');")
        conn.commit()
        print("Employee Data Inserted")

        # Insert Product Data
        cursor.execute("INSERT INTO amazon_products (product_name, category, price, rating) VALUES ('Amazon Echo', 'Smart Home', 99.99, 4.5);")
        cursor.execute("INSERT INTO amazon_products (product_name, category, price, rating) VALUES ('Kindle Paperwhite', 'E-Reader', 129.99, 4.8);")
        cursor.execute("INSERT INTO amazon_products (product_name, category, price, rating) VALUES ('Fire TV Stick', 'Streaming Device', 39.99, 4.6);")
        conn.commit()
        print("Product Data Inserted")

        # Query Employee Data
        cursor.execute("SELECT * FROM amazon_employees;")
        employees = cursor.fetchall()
        print("\nAmazon Employees:")
        for emp in employees:
            print(emp)

        # Query Product Data
        cursor.execute("SELECT * FROM amazon_products;")
        products = cursor.fetchall()
        print("\nAmazon Products:")
        for product in products:
            print(product)

        # Query1 : Get all employees in the Engineering department
        cursor.execute("SELECT name, role FROM amazon_employees WHERE department = 'Engineering';")
        engineers = cursor.fetchall()
        print("\nEngineering Employees:")
        for eng in engineers:
            print(eng)

        # Query2: Get all products under $50
        cursor.execute("SELECT product_name, price FROM amazon_products WHERE price < 50;")
        affordable_products = cursor.fetchall()
        print("\nAffordable Amazon Products (Under $50):")
        for product in affordable_products:
            print(product)

        # Close Connection
        cursor.close()
        conn.close()
        print("\nDatabase Connection Closed")

    except Exception as e:
        print("Error:", e)
