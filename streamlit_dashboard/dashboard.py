import streamlit as st
import pandas as pd
import os
import pickle
import requests
import io
import matplotlib as plt
from utils.tab_builder import TabBuilder


@st.cache_data
def load_pickle_from_github():
    url = "https://raw.githubusercontent.com/matthew-martin1184/healthcare_db_analytics_project/main/data/dataframes.pkl"
    
    # Load serialized data from GitHub
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Failed to download .pkl file from GitHub.")
        return None

    file_like = io.BytesIO(response.content)
    data = pickle.load(file_like)
    
    return data

def set_category():

    def filter_by_source_file(source_file):
        filtered_dict = {
            key: value
            for key, value in queries.items()
            if isinstance(value, dict) and value.get("source_file") == source_file
        }
        return filtered_dict

    def set_source_file():
        if category == "Doctor":
            return 'doctor_queries.sql'
        elif category == "Patient":
            return 'patient_queries.sql'
        elif category == "Medical Procedure":
            return 'procedure_queries.sql'
        elif category == "Billing":
            return 'billing_queries.sql'
        else:
            raise ValueError("Invalid category selected")

    category = st.selectbox(
        "View insights by category",  # Label above the dropdown
        ["Doctor", "Patient", "Medical Procedure", "Billing"]  # Options
    )
    st.write(cat_desc[category])

    return filter_by_source_file(set_source_file())

def set_insights(filtered_dict):
    # Map pretty_name to parent key
    pretty_name_to_key = {
        v["pretty_name"]: k
        for k, v in filtered_dict.items()
        if "pretty_name" in v
    }

    # Multiselect uses pretty_name labels
    pretty_names = list(pretty_name_to_key.keys())
    
    selected_pretty_names = st.multiselect(
        label="Select up to 4 insights to view",
        options=pretty_names,
        max_selections=4,
        key='insights_multiselect_key'
    )

    # Build and return a filtered nested dictionary
    filtered_selection = {
        pretty_name_to_key[name]: filtered_dict[pretty_name_to_key[name]]
        for name in selected_pretty_names
    }

    return filtered_selection


def main():
    # Set the page title and layout
    st.set_page_config(
        page_title="Healthcare Analytics Dashboard",
        #layout="wide",
        #initial_sidebar_state="expanded"
    )

    # Instantiate global variables: queries dict and cat_desc dict
    global queries, cat_desc 
    data = load_pickle_from_github()
    queries = data["queries"]
    cat_desc = data["cat_desc"]
  
    # Select insight category and filter queries dict
    filtered_dict = set_category()

    # Select insights to view from selected category and filter filtered_dict
    insights_dict = set_insights(filtered_dict)

    ##################  DRIVER CODE  ##################
    st.write(insights_dict)
    

    #tabs = build_tabs(insights)

if __name__ == "__main__":
    main()