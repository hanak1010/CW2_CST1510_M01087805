# Hana Mundambra
# M01087805

# Required modules
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

from app.data.db import connect_database
from app.data.tickets import (insert_ticket, get_all_tickets, update_ticket, delete_ticket)
from gemini_api import ask_gemini

st.set_page_config(page_title="IT Tickets", page_icon="👩‍💻", layout = "wide")

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
    st.title("IT Tickets Dashboard")
    st.subheader(f"Access Level: {user_role.title()}")
    
    # Read only access for normal users
    st.header("IT Service Desk Performance Analysis")

    # Display the table
    tickets_data = get_all_tickets()
    st.dataframe(tickets_data, use_container_width=True, hide_index=True)
    
     # Rights for admin and analyst (CRUD/ Update)
    if user_role in ["admin", "analyst"]:

        st.header("Updated Access: Data Governance")

        # User is an admin
        if user_role == "admin":
            available_tabs = ["➕ Create Ticket", "📝 Update Ticket", "🗑️ Delete Ticket"]
        else: # Analyst gets read and update access only
            available_tabs = ["📝 Update Ticket"]

        tabs = st.tabs(available_tabs)

        tab_update = tabs[-1] if len(tabs) == 1 else tabs[1]

        # CREATE (Admin Only)
        if user_role ==  "admin":
            tab_create = tabs[0]
            with tab_create:
                with st.form("create_it_tickets_form", clear_on_submit=True):
                    st.subheader("Add New IT Ticket")

                    # Required input fields
                    ticket_id = st.text_input("Ticket ID")
                    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                    status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Waiting for User"])
                    category = st.selectbox("Category", ["Hardware Issue", "Software Issue", "Network Issue", "general"])
                    subject = "Ticket"
                    description = st.text_area('Description') 
                    created_date = st.date_input("Created Date", value=datetime.date.today(), format="DD/MM/YYYY")

                    add_resolved_date = st.checkbox("Add Resolved Date?")
                    if add_resolved_date:
                        resolved_date = st.date_input("Resolved Date", format="DD/MM/YYYY")
                    else:
                        resolved_date = None

                    assigned_to = st.selectbox("Assigned to", ["IT_Support_A", "IT_Support_B", "IT_Support_C"])
                    created_at = st.datetime_input("Created at", value=datetime.datetime.now(), format="DD/MM/YYYY")

                    resolution_time_hours = st.number_input(" Resolution Time (hours, Optional)", min_value=0, step=1, value=0, help="Enter 0 if ticket not resolved")
                    if resolution_time_hours == 0:
                        resolution_time_hours = None

                    submitted = st.form_submit_button("Register Ticket")

                if submitted:
                    if not ticket_id:
                        st.error("Ticket ID is a required field.")
                    else: 
                        # Check if ID already exists
                        conn = connect_database()
                        existing_id = conn.execute("SELECT 1 FROM it_tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
                        conn.close()

                        if existing_id:
                            st.error("This Ticket ID already exists. Please enter another one.")
                        else:
                            try:
                                    ticket_id = insert_ticket(ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to, created_at, resolution_time_hours)
                                    st.success(f"Ticket {ticket_id} succesfully created.")
                                    
                            except Exception as e:
                                st.error(f"Failed to register ticket: {e}")
        
        # UPDATE (admin and analyst)                
        with tab_update:
            st.subheader("Update Existing IT Ticket")
            
            if tickets_data.empty:
                st.warning("No tickets available to update.")
            else:
                # A selection list to choose from
                ticket_ids = tickets_data['ticket_id'].tolist() if not tickets_data.empty else ["No tickets found"]

                with st.form("update_tickets_form", clear_on_submit=False):
                    ticket_to_update = st.selectbox("Select ticket ID to Update", ticket_ids)
                    new_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], key="update_priority")
                    new_status = st.selectbox("Update Status", ["Open", "In Progress", "Resolved", "Closed"], key="update_status")
                    new_assigned_to = st.selectbox("Updated Assigned to", ["IT_Support_A", "IT_Support_B", "IT_Support_C"], key="update_assigned_to")
                    resolution_date = st.date_input("Resolved Date", format="DD/MM/YYYY")
                    
                                        
                    update_submited = st.form_submit_button("Update Dataset Record")
                    
                    if update_submited:
                        conn = connect_database()
                        
                        rows_affected = update_ticket(
                            conn,
                            ticket_to_update,
                            new_priority,
                            new_status,
                            new_assigned_to,
                            resolution_date
                        )

                        if rows_affected > 0:
                            st.success(f"Successfully updated Ticket Id {ticket_to_update}. {rows_affected} rows affected.")

                        else:
                            st.error(f"Failed to update Ticket ID {ticket_to_update}.")

        # DELETE (admin only)
        if user_role == "admin":
            tab_delete = tabs[2]
            with tab_delete:
                st.subheader("Delete IT Ticket")

                ticket_del = tickets_data['ticket_id'].tolist() if not tickets_data.empty else ["No tickets found"]

                with st.form("delete_ticket_form"):
                    ticket_to_del = st.selectbox("Select Ticket ID to delete", ticket_del)
                    confirm_delete = st.checkbox(f"I confirm I want to **PERMANENTLY DELETE** ticket **{ticket_to_del}**")
                    delete_submitted = st.form_submit_button("Delete Ticket")
                    if delete_submitted and confirm_delete and ticket_to_del != "No tickets found":
                        conn = connect_database()
                        success, message = delete_ticket(conn, ticket_to_del)
                        if success:
                            st.success(f"Ticket {ticket_to_del} successfully deleted.")
                        else:
                            st.error(f"Failed to delete ticket : {message}")
                    elif delete_submitted and not confirm_delete:
                        st.warning("Make sure you confirm deletion by checking the box")   


    # MAIN PAGE (Available to all)
    st.header("IT Service Desk Performance Analysis")
    
    # Displaying chart using plotly to identify the threat with most incident records
    df = tickets_data.copy()

    # Converting resolution time to numeric form
    df['resolution_time_hours'] = pd.to_numeric(df['resolution_time_hours'], errors='coerce')
    
    # Making a dataframe with just these headers
    data = df.groupby(["assigned_to", "status"]).size().reset_index(name='count')
     

    # Building a stacked bar graph
    graph = px.bar(
        data,
        x="assigned_to", # Category in x-axis
        y="count", # Count in y axis
        color="status", # Stacking by status
        title="IT Support Desk Performance: Ticket Status Breakdown",
        labels={"assigned_to": "IT Support Desk", "count": "Number of Tickets", "status" : "Ticket Status"},
        barmode="stack"
    ) 
    # Creating legend
    graph.update_layout(
        legend_title="Support Desk & Ticket Count",
        height=550,
        xaxis_title="Support Desk",
        yaxis_title="Ticket Count",
        bargap=0.3
    )

    st.plotly_chart(graph, use_container_width=True)

    # AI Integration
    st.header("Ask about IT Tickets")
    
    question = st.text_input("Ask a question about IT Tickets or general:")

    if question:
        answer = ask_gemini(user_input=question, user_role=user_role, dashboard_type="it_tickets", df=tickets_data)
        st.write(answer)