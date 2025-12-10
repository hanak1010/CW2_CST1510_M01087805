import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

from app.data.db import connect_database
from app.data.datasets import (insert_dataset, get_all_datasets, update_datasets, delete_dataset)
from gemini_api import ask_gemini

st.set_page_config(page_title="Datasets Metadata", page_icon="🔍", layout = "wide")

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
    st.title("Datasets Metadata Dashboard")
    st.subheader(f"Access Level: {user_role.title()}")
    
    # Read only access for normal users
    st.header("Dataset Resource Consumption Overview")

    # Display the table
    dataset_data = get_all_datasets()
    st.dataframe(dataset_data, use_container_width=True, hide_index=True)

    # Rights for admin and analyst (CRUD/ Update)
    if user_role in ["admin", "analyst"]:

        st.header("Updated Access: Data Governance")

        # User is an admin
        if user_role == "admin":
            available_tabs = ["➕ Create Dataset", "📝 Update Dataset", "🗑️ Delete Dataset"]
        else: # Analyst gets read and update access only
            available_tabs = ["📝 Update Dataset"]

        tabs = st.tabs(available_tabs)

        tab_update = tabs[-1] if len(tabs) == 1 else tabs[1]

        # CREATE (Admin Only)
        if user_role ==  "admin":
            tab_create = tabs[0]
            with tab_create:
                with st.form("create_datasets_metadata_form", clear_on_submit=True):
                    st.subheader("Add New Dataset")
                    # Required input fields
                    dataset_name = st.text_input("Dataset Name")
                    category = st.selectbox("Category", ["Churn Data", "Fraud Details", "Network Logs", "Threat Intelligence", "Source Data"])
                    source = st.selectbox("Source", ["data_scientist", "cyber_admin", "it_admin"])
                    last_updated = st.date_input("Last Updated Date", format="DD/MM/YYYY")
                    record_count = st.number_input("Record Count", min_value=0, step=1000, value=None, placeholder="Leave blank if unknown", key="record_count_input")
                    file_size_mb = st.number_input("File size in mb", min_value=0.0, step=0.1, value=None, placeholder="Leave blank if unknown", key="file_size_mb_input")              

                    submitted = st.form_submit_button("Register Dataset")

                if submitted:
                    if not dataset_name:
                        st.error("Dataset Name is a required field.")
                    else: 
                        last_updated_str = last_updated.strftime('%d/%m/%Y')
                        try:
                            success, message = insert_dataset(dataset_name, category, source, last_updated_str, record_count, file_size_mb)
                            if success:
                                st.success(f"Dataset {dataset_name} succesfully created. {message}")
                            else:
                                st.error(f"Failed to register dataset: {message}")
                        except TypeError as e:
                                st.error(f"Error: {e}")

        # UPDATE (admin and analyst)                
        with tab_update:
            st.subheader("Update Existing Dataset Metadata")
            
            if dataset_data.empty:
                st.warning("No datasets available to update.")
            else:
                # A selection list to choose from
                dataset_choices = dataset_data.apply(lambda row: f"{row['id']} - {row['dataset_name']}", axis=1).tolist()

                # Selection box
                selected_dataset_label = st.selectbox("Select Dataset ID and Name to Update", dataset_choices, key="dataset_select")

                selected_id = int(selected_dataset_label.split(' - ')[0])
                current_data = dataset_data[dataset_data['id'] == selected_id].iloc[0]

                with st.form("update_dataset_form", clear_on_submit=False):
                    st.markdown(f"**Dataset Name:** '{current_data['dataset_name']}' (Cannot be modified)")
                    new_name = current_data['dataset_name']  
                    new_category = st.selectbox("Update category", ["Churn Data", "Fraud Details", "Network Logs", "Threat Intelligence", "Source Data"], key="update_category")
                    new_source =  st.selectbox("Source", ["data_scientist", "cyber_admin", "it_admin"], key="update_source_select")
                    
                    # Convert last_updated string to a date object
                    try:
                        current_date_obj = datetime.datetime.strptime(current_data['last_updated'], '%d/%m/%Y').date()
                    except (ValueError, TypeError):
                        current_date_obj = datetime.date.today()
                    
                    new_last_updated = st.date_input("Last updated date Modified", value=current_date_obj, format="DD/MM/YYYY", key="update_date_input")
                    
                    update_submited = st.form_submit_button("Update Dataset Record")
                    
                    if update_submited:
                        new_last_updated_str = new_last_updated.strftime('%d/%m/%Y')
                        rows_affected = update_datasets(
                            selected_id,
                            new_name,
                            new_category,
                            new_source,
                            new_last_updated_str
                        )

                        if rows_affected > 0:
                            st.success(f"Successfully updated Dataset Id {selected_id}. {rows_affected} rows affected.")

                        else:
                            st.error(f"Failed to update Dataset ID {selected_id}.")

        # DELETE (admin only)
        if user_role == "admin":
            tab_delete = tabs[2]
            with tab_delete:
                st.subheader("Delete Dataset Record")

                dataset_del = dataset_data['id'].tolist() if not dataset_data.empty else ["No datasets found"]

                with st.form("delete_dataset_form"):
                    dataset_to_del = st.selectbox("Select Dataset ID to delete", dataset_del)
                    confirm_delete = st.checkbox(f"I confirm I want to **PERMANENTLY DELETE** dataset**{dataset_to_del}**")
                    delete_submitted = st.form_submit_button("Delete Dataset")
                    if delete_submitted and confirm_delete and dataset_to_del != "No datasets found":
                        conn = connect_database()
                        rows_affected = delete_dataset(conn, dataset_to_del)
                        if rows_affected > 0:
                            st.success(f"Dataset {dataset_to_del} successfully deleted.")
                        else:
                            st.error(f"Failed to delete dataset : {dataset_to_del}")
                    elif delete_submitted and not confirm_delete:
                        st.warning("Make sure you confirm deletion by checking the box")

    elif user_role == 'user':
        st.info("You have **Read-Only** access to the dashboard.")


    # MAIN DASHBOARD (seen by all)
    st.header("Dataset Resource Management")

    # Displaying chart to visualise the dataset that has the most record
    df = dataset_data.copy() 

    df['record_count'] = pd.to_numeric(df['record_count'], errors='coerce').fillna(0)
 
    # converting data to long format (changing only record_count)
    data = df.melt(
        id_vars=["dataset_name", "category", "source"],
        value_vars=["record_count"],
        var_name="metric",
        value_name="value"
    )

    # Renaming metric 
    data["metric"] = data["metric"].replace({"record_count": "Record Count"})

    # Create the stacked bar with patterns
    graph = px.bar(
        data,
        x="category",
        y="value",
        color="metric",
        pattern_shape="source",
        pattern_shape_map={
            "data_scientist": "/",
            "cyber_admin": ".",
            "it_admin": ""
        },
        title="Dataset Consumption Trends",
        labels={
            "category": "Dataset Category",
            "value": "Record Count",
            "metric": "Metric",
            "source": "Uploaded By"
        },
        barmode="stack"
    )

    graph.update_layout(
        legend_title="Dataset Source & Record count",
        height=550,
        xaxis_title="Dataset Category",
        bargap=0.3
    )

    st.plotly_chart(graph, use_container_width=True)

    # AI Integration
    st.header("Ask about Datasets Metadata")
    
    question = st.text_input("Ask a question about Datasets metadata or general:")

    if question:
        answer = ask_gemini(user_input=question, user_role=user_role, dashboard_type="datasets", df=dataset_data)
        st.write(answer)