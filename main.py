import streamlit as st

# Required connections
from app.data.db import connect_database
from app.services.user_service.auth_func import (register_user, login_user, validate_password, validate_username, Passwordstrength)
from app.data.incidents import (insert_incident, get_all_incidents, update_incident_status, delete_incident)
from app.data.datasets import (get_all_datasets, insert_dataset, update_datasets, delete_dataset)
from app.data.tickets import (get_all_tickets, insert_ticket, update_ticket, delete_ticket)

conn = connect_database("DATA/intelligence_platform.db")

st.set_page_config(page_title= "Login / Register", page_icon="🔑", layout="wide")

# ---Session state intialization---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ''
if "role" not in st.session_state:
    st.session_state.role = ''

# When user is logged in, sidebar made visible 
if st.session_state.logged_in:

    st.sidebar.title("👤 Your Profile")
    st.sidebar.markdown(f"**User:**{st.session_state.username}")
    st.sidebar.markdown(f"**Role:** :green[{st.session_state.role.title()}]")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ''
        st.session_state.role = ''
        st.rerun()

st.sidebar.subheader("Dashboard Navigation")

# When user is not logged in
if not st.session_state.logged_in:
    st.title("🛡️ Intelligence Platform")
    st.markdown("***Please Login or Register to view the dashboards***")
    
    # Using tabs for login and registering a user
    tab_login, tab_register = st.tabs(["Login", "Register"])

    # LOGIN TAB
    with tab_login:
        st.subheader("Login")
        with st.form("Login Form"):
            login_username = st.text_input("Username", key="login_user")
            login_password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if not login_username or not login_password:
                    st.error("Error, please enter both username and password.")
                else:
                    success, msg = login_user(login_username, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = login_username
                        
                        # Get the role of the user from users database
                        conn = None
                        try:
                            conn = connect_database()
                            cursor = conn.cursor()

                            cursor.execute("SELECT role From users WHERE username = ?", (login_username, ))
                            user_role = cursor.fetchone()

                            if user_role:
                                st.session_state.role = user_role[0]
                            else:
                                st.session_state.role = 'user'
                                st.warning("No role found, 'user' given as default.")
                        except Exception as e:
                            st.error(f"Error fetching role: {e}")
                            st.session_state.logged_in = False 
                        finally:
                            if conn:
                                conn.close()
                        
                        if st.session_state.logged_in:
                            st.switch_page("pages/01_cyber_incidents.py")
                            
                        else:
                            st.error(msg)
        
    # REGISTER TAB
    with tab_register:
        st.subheader("Register")

        with st.form("Register Form"):
            new_username = st.text_input("Choose a username", key="register_username")
            new_password = st.text_input("Choose a password", type="password", key="register_password")
            confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")
            new_role = st.selectbox("Role", ["user", "analyst", "admin"], key="new_role")
            
            # To show strength of password
            if new_password:
                strength = Passwordstrength(new_password).check_strength()
                if strength == "Weak":
                    st.warning(f"Password Strength: {strength}")
                elif strength == "Moderate":
                    st.info(f"Password Strength: {strength}")
                else:
                    st.success(f"Password Strength: {strength}")

                valid, msg = validate_password(new_password)
                if not valid:
                    st.error(msg)
                else:
                    st.success(msg)

            submitted = st.form_submit_button("Create new account")

        if  submitted:
            
            if not new_username or not new_password:
                st.warning("Please fill in all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
                
            else:
                 
                is_valid, username_msg = validate_username(new_username)
                if not is_valid:
                    st.error(username_msg)
                else:
                    success, msg = register_user(new_username, new_password, new_role)

                    if success:
                        st.success("Account created! You can now log in from the Login tab.")
                    else:
                        st.error(msg)
                 
else:
    st.title(f"🔓Welcome! {st.session_state.username} ({st.session_state.role.title()})")
    st.info("Use the sidebar to navigate to Cyber Incidents, Datasets or IT Tickets Dashboard.")
    
 