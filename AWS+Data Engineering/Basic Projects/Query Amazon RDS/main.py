from queries import run_postgresql_queries, run_mysql_queries

def main():
    # Choose which database to run queries on:
    print("Running queries on PostgreSQL database...")
    run_postgresql_queries()
    
    # Uncomment the following line to run MySQL queries instead
    # run_mysql_queries()

if __name__ == "__main__":
    main()
