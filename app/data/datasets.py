import pandas as pd
from app.data.db import connect_database

def insert_dataset(id, dataset_name, category, source, last_updated, record_count, file_size_mb):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datasets_metadata
        (id, dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id, dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit() 
    
    conn.close()
    return id

def get_all_datasets():
    """Get all datasets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def update_datasets(conn, id, new_category, new_source, new_last_updated):
    """ Update a dataset."""
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE datasets_metadata SET category = ?, source = ?, last_updated = ? WHERE id = ?""", (new_category, new_source, new_last_updated, id))
    conn.commit()
    return cursor.rowcount

def delete_dataset(conn, id):
    """
    Delete an dataset from the database.
    """
    cursor = conn.cursor()
    cursor.execute(""" 
    DELETE FROM datasets_metadata WHERE id = ?""",(id,))
    conn.commit()
    return cursor.rowcount