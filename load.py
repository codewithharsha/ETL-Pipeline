from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

user = 'root'
password = '2002'
host = 'localhost'
port = '3306'
database = 'etl_pipeline'

# Create connection engine
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

try:
    with engine.connect() as connection:
        print(" MySQL connection successful!")
        data = pd.read_csv('processed_border_crossing_data.csv')
        # Push to MySQL table (creates it if not exists)
        table_name = 'border_crossing_data'
        data.to_sql(table_name, con=engine, index=False, if_exists='replace')
        print("Data Loaded successfully!!")

except SQLAlchemyError as e:
    print("MySQL connection failed:")
    print(str(e))
