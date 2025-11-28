from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service.auth_func import register_user, login_user
from app.services.user_service.migration import migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents
from app.data.importing import load_all_csv_data
from app.data.importing import DB_PATH


# Main demo
def main():
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)
    
    # 1. Setup database
    conn = connect_database()
    create_all_tables(conn)
        
    # 2. Migrate users
    migrate_users_from_file(conn)
    
    # 3. Test authentication
    success, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)
    
    success, msg = login_user("alice", "SecurePass123!")
    print(msg)
    
    # 4. Test CRUD
    incident_id = insert_incident(
        "2024-11-05",
        "Phishing",
        "High",
        "Open",
        "Suspicious email detected",
        "alice"
    )
    print(f"Created incident #{incident_id}")
    
    # 5. Query data
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")

    # Close connection
    conn.close()

if __name__ == "__main__":
    main()