# Hana Mundambra
# M01087805

import pandas as pd
from app.data.db import connect_database

# Function for inserting a dataset to the table
def insert_dataset(dataset_name, category, source, last_updated, record_count, file_size_mb):
    """Insert new dataset."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit() 
    new_id = cursor.lastrowid
    return True, f"Dataset {dataset_name} created successfully with ID: {new_id}." 
    conn.close()

# Function to read all the data from table
def get_all_datasets():
    """Get all datasets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

# Function to update a dataset
def update_datasets(id, new_name, new_category, new_source, new_last_updated):
    """ Update a dataset."""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                    UPDATE datasets_metadata SET dataset_name = ?,  category = ?, source = ?, last_updated = ? WHERE id = ?""", (new_name, new_category, new_source, new_last_updated, id))
        conn.commit()
        rows = cursor.rowcount
        conn.close
        return rows
    except Exception as e:
        conn.close()
        print(f"Error updating dateset {id}: {e}")
        return 0

# Function to delete a dataset
def delete_dataset(conn, id):
    """
    Delete an dataset from the database.
    """
    cursor = conn.cursor()
    cursor.execute(""" 
    DELETE FROM datasets_metadata WHERE id = ?""",(id,))
    conn.commit()
    return cursor.rowcount