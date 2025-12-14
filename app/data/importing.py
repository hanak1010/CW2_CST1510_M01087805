# Hana Mundambra
# M01087805

import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path

# Define paths
DATA_DIR = Path("DATA")
DB_PATH = DATA_DIR / "intelligence_platform.db"
 
# Create DATA folder if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

print(" Imports successful!")
print(f" DATA folder: {DATA_DIR.resolve()}")
print(f" Database will be created at: {DB_PATH.resolve()}")

# load csv file to table

def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.
    """
    csv_file = Path(csv_path)
    if not csv_file.exists():
        print(f"CSV file not found: {csv_file}")
        return 0
    try:
        df = pd.read_csv(csv_file)
        
        # Matching csv headers to table for cyber_incidents
        if table_name == "cyber_incidents":
            df.rename(columns={
                "timestamp": "date" ,
                "category": "incident_type"
            }, inplace=True)
            if "reported_by" not in df.columns:
                df["reported_by"] = None
            if "created_at" not in df.columns:
                df["created_at"] = pd.Timestamp.now()
        
        # Matching csv headers to table for datasets
        elif table_name == "datasets_metadata":
            rename_columns = ["rows", "uploaded_by", "upload_date"]
            if all (col in df.columns for col in rename_columns):
                df.rename(columns={
                  "rows" : "record_count",
                  "uploaded_by": "source",
                  "upload_date": "last_updated"
                  }, inplace=True)
    
            if "columns" in df.columns:
                df.drop(columns=["columns"], inplace=True)

            for col in ["last_updated", "file_size_mb"]:
                if col not in df.columns:
                    df[col] = None
            if "created_at" not in df.columns:
                    df["created_at"] = pd.Timestamp.now()
        
        # Matching csv file headers for it tickets
        elif table_name == "it_tickets":
            if "created_at" in df.columns:
                df["created_at"] = pd.to_datetime(df["created_at"])
                df["created_date"] = pd.to_datetime(df["created_at"]).dt.date.astype(str)

                # Calculate resolved_date
                if "resolution_time_hours" in df.columns:
                    df["resolved_date"] = df.apply(
                        lambda row: (row["created_at"] + pd.to_timedelta(row["resolution_time_hours"], unit="h")).date().isoformat()
                        if row["status"] == "Resolved" else None, #type: ignore
                        axis=1
                    )
            if "category" not in df.columns:
                df["category"] = "general" # assigning a default category
            if "subject" not in df.columns:
             df["subject"] = df["description"].str.split().str[0]
             
        print(f"Loading {len(df)} rows from {csv_file.name} into table '{table_name}'")
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        
        print(f"☑️ Successfully loaded {len(df)} rows from {csv_file.name} to table: {table_name}")
        return len(df)
    except sqlite3.IntegrityError as e:
        # Errors incase of failure in loading
        print(f"FATAL SQL ERROR loading {csv_file.name} into {table_name}: {e}")
        return 0
    except Exception as e:
        print(f"Failed to load CSV file {csv_file.name}. General Error: {e}")
        return 0

def load_all_csv_data(conn):
    
    # Load all csv files to their respective tables and return total no. of rows loaded
    total_rows = 0 

    # Load cyber incidents
    total_rows += load_csv_to_table(conn, Path("DATA/cyber_incidents.csv"), "cyber_incidents")

    # Load datasets metadata
    total_rows += load_csv_to_table(conn, Path("DATA/datasets_metadata.csv"), "datasets_metadata")

    # Load tickets
    total_rows += load_csv_to_table(conn, Path("DATA/it_tickets.csv"), "it_tickets")
    
    return total_rows
    