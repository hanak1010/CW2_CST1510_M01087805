import pandas as pd
from app.data.db import connect_database

def insert_incident(incident_id, date, incident_type, severity, status, description, reported_by=None):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                INSERT INTO cyber_incidents
                (incident_id, date, incident_type, severity, status, description, reported_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (incident_id, date, incident_type, severity, status, description, reported_by))
        conn.commit() 
        conn.close()
        return True, "Incident created successfully"
    except Exception as e:
        conn.close()
        print(f"Error creating incident {incident_id}: {e}")
        return False, str(e)



def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY incident_id DESC",
        conn
    )
    conn.close()
    return df

def update_incident_status(incident_id, new_status):
    """ Update the status of an incident."""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                    UPDATE cyber_incidents SET status = ? WHERE incident_id = ?""", (new_status, incident_id))
        conn.commit()
        return True, "Status updated successfully"
    except Exception as e:
        print(f"Error updating incident {incident_id}: {e}")
        return False, str(e)

def delete_incident(incident_id):
    """
    Delete an incident from the database.
    """
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute(""" 
        DELETE FROM cyber_incidents WHERE incident_id = ?""",(incident_id,))
        conn.commit()
        deleted_rows = cursor.rowcount
        conn.close()
        
        if deleted_rows > 0 :
            return True, f"Successfully deleted incident {incident_id}."
        else:
            return False, f"Failed to delete incident {incident_id}."
    except Exception as e:
        conn.close()
        print(f"Error deleting incident {incident_id}: {e}")
        return False, f"Error deleting incident: {e}"

# ANALYTICAL QUERIES

def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df 

def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df
