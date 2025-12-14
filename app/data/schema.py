# Hana Mundambra
# M01087805

# Create users table
def create_users_table(conn):
    """
    Create the users table if it doesn't exist.
    """
    cursor = conn.cursor()
    
    # SQL statement to create users table
    create_table_sql = """
    create table if not exists users (
        id integer primary key autoincrement,
        username text not null unique,
        password_hash text not null,
        role text default 'user',
        created_at timestamp default current_timestamp
    )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print(" ✅ Users table created successfully!")   

# Create cyber_incidents table
def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table.
    """
    cursor = conn.cursor()
    
    # SQL statement to create cyber incidents table
    create_table_sql = """ 
    create table if not exists cyber_incidents (
        incident_id integer primary key,
        date text,
        incident_type text,
        severity text,
        status text,
        description text,
        reported_by text, 
        created_at timestamp default current_timestamp,
        foreign key (reported_by) references users(username)
    )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Cyber Incidents table created successfully!")    

# Create datasets_metadata table
def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table.
    """
    cursor = conn.cursor()
    
    # SQL statement
    create_table_sql = """
    create table if not exists datasets_metadata (
        id integer primary key autoincrement,
        dataset_name TEXT NOT NULL,
        category TEXT,
        source TEXT,
        last_updated TEXT,
        record_count INTEGER,
        file_size_mb REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )    
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Data sets metadata table created successfully!")    
    

# Create it_tickets table
def create_it_tickets_table(conn):
    """
    Create the it_tickets table.
    """
    cursor = conn.cursor()

    # SQL statement
    create_table_sql = """
    create table if not exists it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL, 
        priority TEXT, 
        status TEXT, 
        category TEXT, 
        subject TEXT NOT NULL,
        description TEXT,
        created_date TEXT,
        resolved_date TEXT,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolution_time_hours INTEGER
    )    
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ IT Tickets table created successfully!")  

# Create all tables at once
def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn) 