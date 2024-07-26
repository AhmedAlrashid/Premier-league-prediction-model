import csv
import sqlite3
import pandas as pd

def dataset_to_database(file_path, encoding = 'utf-8'):
    with open(file_path, 'r', encoding = encoding) as the_file:
        reader = csv.reader(the_file)
        header = next(reader)  # Extract the header row
        columns = ', '.join(header)
        
        # Create an in-memory SQLite database
        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        
        # Create table with appropriate column names
        cursor.execute(f'CREATE TABLE premier_league ({columns})')
        
        # Prepare the insert statement
        placeholders = ', '.join('?' * len(header))
        insert_query = f'INSERT INTO premier_league ({columns}) VALUES ({placeholders})'
        
        # Insert each row into the table
        for row in reader:
            cursor.execute(insert_query, row)
        connection.commit()        
        cursor.execute('SELECT * FROM premier_league')
        rows = cursor.fetchall()
        connection.close()

def reading_file(file_path):
    df=pd.read_csv(file_path)
    print(df.tail())


reading_file('results.csv')