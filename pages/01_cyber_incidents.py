# Hana Mundambra
# M01087805

# Importing required modules
import streamlit as st  # For website creation
import pandas as pd     # To display database tables
import plotly.express as px # For creating graph
import datetime # Required module for date inputs

from app.data.db import connect_database
from app.data.incidents import (insert_incident, get_all_incidents, update_incident_status, delete_incident) # CRUD functions
from gemini_api import ask_gemini # AI Integration

st.set_page_config(page_title="Cyber Incidents", page_icon="👮‍♂️", layout = "wide")

# If user not logged in, switch to main page
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("main.py")   # switch to the first page
    st.stop()
else:
    user_role = st.session_state.role
    current_username = st.session_state.username 

    # Header for dashboard
    st.title("Cyber Incidents Dashboard")
    st.subheader(f"Access Level: {user_role.title()}")
    
    # Read only access for normal users
    st.header("Cyber Threats Data Overview")
 
    # Display data
    incident_data = get_all_incidents()
    st.dataframe(incident_data, use_container_width=True, hide_index=True)

    # Rights for admin and analyst (CRUD/ Update)
    if user_role in ["admin", "analyst"]:

        st.header("Updated Access: Incident Management")

        # When user is an admin
        if user_role == "admin":
            available_tabs = ["➕ Create Incident", "📝 Update Incident", "🗑️ Delete Incident"]
        else: # Analyst user gets read and update access only
            available_tabs = ["📝 Update Incident"]
        
        tabs = st.tabs(available_tabs)

        tab_update = tabs[-1] if len(tabs) == 1 else tabs[1]

        # CREATE (Admin Only)
        if user_role ==  "admin":
            tab_create = tabs[0]
            with tab_create:
                with st.form("create_cyber_incidents_form", clear_on_submit=True):
                    st.subheader("Add New Cyber Incident")

                    st.info(f"Reported By: {current_username}")
                    # Required input fields
                    incident_id = st.text_input("Enter Incident ID")
                    date = st.date_input("Date Detected", value=datetime.date.today(), format= "DD/MM/YYYY")
                    incident_type = st.selectbox("Type", ["Phishing", "Malware", "DDoS","Misconfiguration", "Unauthorized Access", "Ransomware", "Other"])
                    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
                    status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
                    description = st.text_area('Description') 
                                   

                    submitted = st.form_submit_button("Create New Incident Record")
                     
                if submitted:
                    if not incident_id:
                        st.error("Incident ID is a required field.")
                    else: 
                        date_str = date.strftime('%d/%m/%Y')
                        reported_by = current_username
                        success, message = insert_incident(incident_id, str(date), incident_type, severity, status, description, reported_by)
                        if success:
                           st.success(f"Incident {incident_id} succesfully created. {message}")
                        else:
                           st.error(f"Failed to create incident: {message}")
        # UPDATE (admin and analyst)                
        with tab_update:
            st.subheader("Update Cyber Incident")

            incident_ids = (incident_data['incident_id'].tolist() if not incident_data.empty else ["No incidents found"])

            with st.form("update_cyber_incident_form"):
                incident_to_update = st.selectbox("Select Incident ID to Update", incident_ids)
                new_status = st.selectbox("Update Status", ["Open", "In Progress", "Resolved", "Closed"], key="update_status")
 
                update_submited = st.form_submit_button("Update Incident Record")
                
                if update_submited and incident_to_update != "No incidents found":
                    updates = {
                        'status' : new_status
                    }

                    success, message = update_incident_status(incident_to_update, new_status)
                    if success:
                        st.success(f"Status for Incident {incident_to_update} successfully updated to {new_status}.")
                    else:
                        st.error(f"Failed to update incident status: {message}")

        # DELETE (admin only)
        if user_role == "admin":
            tab_delete = tabs[2]
            with tab_delete:
                st.subheader("Delete Cyber Incident")

                incident_del = (incident_data['incident_id'].tolist() if not incident_data.empty else ["No incidents found"])

                with st.form("delete_incident_form"):
                    incident_to_del = st.selectbox("Select Incident ID to delete", incident_del)
                    confirm_delete = st.checkbox(f"I confirm I want to **PERMANENTLY DELETE** Incident **{incident_to_del}**")
                    delete_submitted = st.form_submit_button("Delete Incident")
                    if delete_submitted and confirm_delete and incident_to_del != "No incidents found":
                        success, message = delete_incident(incident_to_del)
                        if success:
                            st.success(f"Incident {incident_to_del} successfully deleted.")
                        else:
                            st.error(f"Failed to delete incident : {message}")
                    elif delete_submitted and not confirm_delete:
                        st.warning("Make sure you confirm deletion by checking the box")

    elif user_role == 'user':
        st.info("You have **Read-Only** access to the dashboard.")
     

    # MAIN PAGE (Available to all)
    st.header("Cyber Threats Trend Analysis")
    
    # Displaying chart using plotly to identify the threat with most incident records
    df = incident_data.copy()
    
    # Making a dataframe with just these headers
    data = df.groupby(["incident_type", "status", "severity"]).size().reset_index(name='count')

    # Ordering according to severity
    severity_order = ["Low", "Medium", "High", "Critical"]
    data['severity'] = pd.Categorical(data['severity'], categories=severity_order, ordered=True)
    
    # Find incidents that are open or in progress
    open_data = data[data["status"].isin(["Open", "In Progress"])] 

    # Building a stacked bar graph
    graph = px.bar(
        data,
        x="incident_type", # Category in x-axis
        y="count", # Count in y axis
        color="severity", # Stacking by severity
        pattern_shape="status",
        pattern_shape_map={
            "Open": "/", # Slash means open
            "In Progress": ".", # Dot means in progress
            "Resolved": "", # No pattern
            "Closed": "" # No pattern
        },
        title="Cyber Incident Trends: Spike in Phishing & Response Bottleneck Overview",
        labels={"incident_type": "Incident Category", "count": "Number of Incidents"},
        barmode="stack"
    ) 
    # Creating legend
    graph.update_layout(
        legend_title="Severity & Status",
        height=550,
        xaxis_title="Incident Category",
        bargap=0.3
    )

    st.plotly_chart(graph, use_container_width=True) 

    # AI Integration
    st.header("Ask about Cyber Incidents")
    
    question = st.text_input("Ask a question about cyber incidents:")

    if question:
        answer = ask_gemini(user_input=question, user_role=user_role, dashboard_type="cyber_incidents", df=incident_data)
        st.write(answer)