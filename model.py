import csv
import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

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
    df.dtypes
    print(df.tail())

def catgeorize_for_ml(file_path):
    matches=pd.read_csv(file_path)
    #add venue codes to numerically measure venue (home and away)
    matches["venue_code"]=matches["venue"].astype("category").cat.codes
    #add opponent codes to numerically measure opponent
    matches["opp_code"]=matches["opponent"].astype("category").cat.codes
    #numerify time
    matches["hours"]=matches["time"].str.replace(":.+","",regex=True)
    # What day of the week
    matches["date"] = pd.to_datetime(matches["date"])
    matches["day_code"] = matches["date"].dt.dayofweek
    #checks if team won, 1 if they won, 0 if they lost
    matches["target"]=(matches["result"]=="W").astype("int")

    return matches

def training(file_path):
    matches=pd.read_csv(file_path)
    rf=RandomForestClassifier(n_estimators=50,min_samples_split=10,random_state=1)
    train_set=matches["date"]<"2022-01-01"
    test_set=matches["date"]>="2022-01-01"
    predictors=["venue_code","opp_code","hours","day_code"]
    rf.fit(train_set["predictors"],train_set["target"])



matches_new=catgeorize_for_ml('matches.csv')
print(matches_new.head())
reading_file('matches.csv')