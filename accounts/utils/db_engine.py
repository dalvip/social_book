from sqlalchemy import create_engine

DATABASE_URI = 'postgresql://postgres:Pratik@9021@localhost:5432/social_book'

engine = create_engine(DATABASE_URI)

def fetch_data():
    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM uploaded_files LIMIT 10;")
        for row in result:
            print(row)