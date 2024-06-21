import pandas as pd
from sqlalchemy import create_engine

# Read the CSV file
file_path = 'FBref_player_stats.csv'
df = pd.read_csv(file_path)

# Define the connection parameters
user = 'postgres'
password = 'admin'
host = 'localhost'
port = '5433'
database = 'PLapp'

# Create the connection string
connection_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

# Create the database engine
engine = create_engine(connection_string)

# Define the table name
table_name = 'player_stats'

# Write the DataFrame to the PostgreSQL table
df.to_sql(table_name, engine, if_exists='replace', index=False)
