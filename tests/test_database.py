import pandas as pd
import pytest 
import sqlite3


from src.storage.database import create_events_table, insert_events_into_db

def test_create_events_table(tmp_path):
    db_path= tmp_path / "test.db"
    create_events_table(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    result = cursor.fetchone()
    assert result is not None
    conn.close()

def test_create_events_table_when_table_already_exists(tmp_path):
    db_path = tmp_path / "test.db"
    create_events_table(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("insert into events (event_id) values ('evt_001')")
    conn.commit()
    conn.close()    
    create_events_table(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * from events") 
    result = cursor.fetchall()
    assert result == [('evt_001', None, None, None, None, None)]
    conn.close()

def test_insert_events_into_db(tmp_path):
    db_path = tmp_path / "test.db"
    create_events_table(db_path)
    df = pd.DataFrame({
        'event_id': ['evt_001', 'evt_002'],
        'service_name': ['checkout-service', 'payment-service'],
        'event_type': ['request', 'request'],
        'status_code': [200, 500],
        'response_time_ms': [150, 300],
        'event_timestamp': ['2026-09-22T09:00:01', '2026-09-22T09:00:04']
    })
    insert_events_into_db(df, db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    result = cursor.fetchall()  
    assert len(result) == 2
    assert result[0][0] == 'evt_001'    
    assert result[1][0] == 'evt_002'
    conn.close()

def test_insert_duplicate_event_raises_error(tmp_path):
    db_path = tmp_path / "test.db"
    create_events_table(db_path)
    df=pd.DataFrame({
        'event_id': ['evt_001','evt_001'],
        'service_name': ['checkout-service','payment-service'],
        'event_type': ['request','request'],
        'status_code': [200,500],
        'response_time_ms': [150, 300],
        'event_timestamp': ['2026-09-22T09:00:01', '2026-09-22T09:00:04']})
    with pytest.raises(sqlite3.IntegrityError):
        insert_events_into_db(df, db_path)

   
   