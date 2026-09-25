import sqlite3
import pandas as pd
from src.ingestion.ingest_events import run_pipeline

input_path = "data/raw/events.csv"
output_path = "data/processed/cleaned_events.csv"

def create_events_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_id TEXT PRIMARY KEY,
            service_name TEXT,
            event_type TEXT,
            status_code INTEGER,
            response_time_ms INTEGER,
            event_timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_events_into_db(df, db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for _, row in df.iterrows():
         cursor.execute('''
            INSERT INTO events (event_id, service_name, event_type, status_code, response_time_ms, event_timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (row['event_id'], row['service_name'], row['event_type'], row['status_code'], row['response_time_ms'], row['event_timestamp']))    
   



    
if __name__ == "__main__":
    db_path = "data/observability.db"
    create_events_table(db_path)
    cleaned_df = run_pipeline(input_path, output_path)
    insert_events_into_db(cleaned_df, db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

