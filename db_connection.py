# db_connection.py
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus  # Add this to handle special characters in password

# Replace these with your PostgreSQL credentials
DB_USER = "postgres"
DB_PASSWORD = "Pratik@9021"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "social_book"

# Create connection URL - fixed the string formatting and encoded the password
DATABASE_URL = f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
try:
    engine = create_engine(DATABASE_URL)
    print("Successfully connected to the database!")

    # Test query - replace with your actual table name
    query = """
    SELECT * FROM pg_tables 
    WHERE schemaname = 'public';
    """
    
    with engine.connect() as connection:
        result = connection.execute(text(query))
        rows = result.fetchall()
        
        print("\nAvailable tables in your database:")
        for row in rows:
            print(row)

except Exception as e:
    print(f"Error: {e}")