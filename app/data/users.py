# Hana Mundambra
# M01087805

import sqlite3
from app.data.db import connect_database

# To get user from the database
def get_user_by_username(username):
    """Retrieve user by username."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user

# To insert a user to the table
def insert_user(username, password_hash, role='user'):
    """Insert new user."""
    conn = connect_database()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting user: {e}")
    finally:    
        conn.close()

    return True, f"User '{username}' inserted successfully!"  

# To update password
def update_user_password(conn, username, new_password_hash):
    """ Update the password."""
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE users SET password_hash = ? WHERE username = ?""", (new_password_hash, username))
    conn.commit()
    return cursor.rowcount  

# To update user role
def update_user_role(conn, username, new_role):
    """ Update role """
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE users SET role = ? WHERE username = ?""", (new_role, username)) 
    conn.commit()
    return cursor.rowcount  

# To delete user
def delete_user(conn, username):
    """Delete a user"""
    cursor = conn.cursor()
    cursor.execute(""" 
                   DELETE FROM users WHERE username = ?""", (username, ))
    conn.commit()
    return cursor.rowcount
