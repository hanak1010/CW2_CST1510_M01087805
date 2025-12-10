import pandas as pd
from app.data.db import connect_database

def insert_ticket(priority, status, category, subject, description, created_date, resolved_date, assigned_to, created_at, resolution_time_hours):
    """Insert new ticket."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets
        (priority, status, category, subject, description, created_date, resolved_date, assigned_to, created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (priority, status, category, subject, description, created_date, resolved_date, assigned_to, created_at, resolution_time_hours))
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return ticket_id

def get_all_tickets():
    """Get all tickets as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def update_ticket(conn, ticket_id, new_priority,  new_status, new_assigned_to, resolution_date=None):
    """ Update the priority, status, assigned_to and resolution_date of a ticket."""
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE it_tickets SET priority = ?, status = ?, assigned_to = ?, resolved_date = ? WHERE ticket_id = ?""", (new_priority,  new_status, new_assigned_to, resolution_date, ticket_id))
    conn.commit()
    return cursor.rowcount

def delete_ticket(conn, ticket_id):
    """
    Delete a ticket from the database.
    """
    cursor = conn.cursor()
    cursor.execute(""" 
    DELETE FROM it_tickets WHERE ticket_id = ?""",(ticket_id,))
    conn.commit()
    return cursor.rowcount

# ANALYTICAL QUERIES

def get_tickets_by_category_count(conn):
    """
    Count tickets by category.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM it_tickets
    GROUP BY category
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_high_priority_by_status(conn):
    """
    Count high priority tickets by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM it_tickets
    WHERE priority = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_ticket_categories_with_many_cases(conn, min_count=5):
    """
    Find ticket categories with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT category, COUNT(*) as count
    FROM it_tickets
    GROUP BY category
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df
