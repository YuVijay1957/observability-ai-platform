import pandas as pd
import logging
from pathlib import Path 

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def read_events(file_path):
    df = pd.read_csv(file_path)
    return df   

def validate_columns(df, required_columns):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns: 
        raise ValueError(f"Missing required columns: {missing_columns}")
    return df
def remove_duplicates(df):
        rows_before = len(df)
        df = df.drop_duplicates(subset=['event_id'], keep='first') 
        logging.info(f"Duplicates removed: {rows_before - len(df)}")
        return df


def write_events(df, output_path, has_existing_data):
    if has_existing_data:
        df.to_csv(output_path, mode='a', header=False, index=False)
    else:
        df.to_csv(output_path, index=False)
    logging.info(f"Rows written: {len(df)}")

def get_new_events(incoming_df, existing_df):
    # Identify new events by checking which event_ids are not in the existing DataFrame
    new_events_df = incoming_df[~incoming_df['event_id'].isin(existing_df['event_id'])]
    return new_events_df


def run_pipeline(input_path, output_path):
    logging.info("Pipeline started")  

    required_columns =    ["event_id",
    "service_name",
    "event_type",
    "status_code",
    "response_time_ms",
    "event_timestamp"]
    
    # Read events from CSV
    df = read_events(input_path)
    logging.info(f"Rows read: {len(df)}")

    # Validate required columns
    df = validate_columns(df, required_columns)
    

    df = remove_duplicates(df)

    has_existing_data = False

    if Path(output_path).exists():
        try:
            existing_df = read_events(output_path)
            has_existing_data = True
            df = get_new_events(df, existing_df)
        except pd.errors.EmptyDataError:      
            logging.warning("Existing processed file is empty. Treating as a fresh load.")
    logging.info(f"New events: {len(df)}")  

    # Write cleaned events to output CSV
    write_events(df, output_path, has_existing_data)
    logging.info("Pipeline completed successfully")
    return df  # Return the cleaned DataFrame for further use if needed

if __name__ == "__main__":
    input_path = "data/raw/events.csv"
    output_path = "data/processed/cleaned_events.csv"
    try:                            
        run_pipeline(input_path, output_path)
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")  
        raise   


