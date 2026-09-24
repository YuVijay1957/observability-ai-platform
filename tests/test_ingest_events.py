import pandas as pd
import pytest 


from src.ingestion.ingest_events import get_new_events, remove_duplicates, validate_columns



def test_remove_duplicates():
    df = pd.DataFrame({
        'event_id': ['evt_001', 'evt_002', 'evt_001', 'evt_003']})
    cleaned_df = remove_duplicates(df)
    assert len(cleaned_df) == 3
    assert cleaned_df['event_id'].tolist() == ['evt_001', 'evt_002', 'evt_003']
def test_remove_duplicates_when_no_duplicates():
    df = pd.DataFrame({
        'event_id': ['evt_001', 'evt_002', 'evt_003']
    })
    cleaned_df = remove_duplicates(df)
    assert len(cleaned_df) == len(df)
def test_remove_duplicates_when_all_duplicates():
        df = pd.DataFrame({
             'event_id': ['evt_001', 'evt_001', 'evt_001'],
             'response_time_ms': [100, 200, 300]
        })
        cleaned_df = remove_duplicates(df)
        assert len(cleaned_df) == 1
        assert cleaned_df['event_id'].tolist() == ['evt_001']   
        assert cleaned_df['response_time_ms'].tolist() == [100]
def test_validate_columns_when_all_columns_exist():
     df = pd.DataFrame({
         'event_id': ['evt_001'],   
         'service_name': ['checkout-service']})
     required_columns = ['event_id', 'service_name']
     validated_df = validate_columns(df, required_columns)    
     assert validated_df.equals(df) 
def test_validate_columns_when_missing_columns():
     df = pd.DataFrame({
            'event_id': ['evt_001']})
     required_columns = ['event_id', 'service_name']    
     with pytest.raises(ValueError):  
         validate_columns(df, required_columns)
def test_get_new_events():
    incoming_df = pd.DataFrame({
        'event_id': ['evt_001', 'evt_002', 'evt_003']})
    existing_df = pd.DataFrame({
        'event_id': ['evt_001', 'evt_002'],
        'service_name': ['checkout-service', 'payment-service']
    })
    new_events_df = get_new_events(incoming_df, existing_df)
    assert len(new_events_df) == 1
    assert new_events_df['event_id'].tolist() == ['evt_003']