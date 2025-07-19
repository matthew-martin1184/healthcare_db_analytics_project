import streamlit as st
import pandas as pd
import pickle
import requests
import io
import matplotlib as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from streamlit_dashboard.utils.tabs import Tabs

# Set the page title and layout
st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    #layout="wide",
    #initial_sidebar_state="expanded"
)

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
        "View insights by category.",  # Label above the dropdown
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

    selected_pretty_name = st.selectbox(
        label="Select an insight to view",
        options=pretty_names,
        key='insights_selectbox_key'
    )

    return {
        pretty_name_to_key[selected_pretty_name]: 
        filtered_dict[pretty_name_to_key[selected_pretty_name]]
    }

def display_description(insight_dict):
    insight_data = list(insight_dict.values())[0]

    show_long = st.toggle("Show detailed description.", value=False,
                          key=f"{list(insight_dict.keys())[0]}_toggle")
    if show_long:
        st.write(insight_data.get("long_description", "No long description available."))
    else:
        st.write(insight_data.get("description", "No short description available."))

def set_tabs(insights_dict):
        #insights_container = Tabs(insights_dict)
        return Tabs(insights_dict)

def main():
    st.title("Healthcare Analytics Dashboard")
    st.write("This dashboard is currently in development.")

    # Instantiate global variables: queries dict and cat_desc dict
    global queries, cat_desc 
    data = load_pickle_from_github()
    queries = data["queries"]
    cat_desc = data["cat_desc"]

    # Select insight category and filter queries dict
    filtered_dict = set_category()

    # Select insights to view from selected category and filter filtered_dict
    insights_dict = set_insights(filtered_dict)

    # Display the insight description
    display_description(insights_dict)

    container = set_tabs(insights_dict)
    container.display()

    ## driver code
    st.write(insights_dict)



if __name__ == "__main__":
    main()

'''
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
    
    selected_pretty_name = st.selectbox(
        label="Select an insight to view",
        options=pretty_names,
        key='insights_selectbox_key'
    )

    # Build and return a filtered nested dictionary
    filtered_selection = {
        pretty_name_to_key[selected_pretty_name]: filtered_dict[pretty_name_to_key[selected_pretty_name]]
}

    return filtered_selection

def set_tab(insights_dict):

    insights_dict_formatted_list = []

    for key, value in insights_dict.items():
        insight_dict = {}
        if "pretty_name" in value:
            pretty_name = value["pretty_name"]
            value_copy = {k: v for k, v in value.items() if k != "pretty_name"}
            insight_dict[pretty_name] = value_copy

        tab_names.append(pretty_name)
        insights_dict_formatted_list.append(insight_dict)

    if not tab_names:
        st.warning("No insights available to display.")
        return [], []    

    tabs_st = st.tabs(tab_names)

    return insights_dict_formatted_list
        
def build_tabs(insight_dict, tabs):
    tab_objs = []
    for insight, tab in zip(insight_dict, tabs):
        with tab:
            tab_obj = Tab(insight, tab)
            tab_obj.display_description()
            tab_obj.set_options()
            
        tab_objs.append(tab_obj)
    return tab_objs    


def main():
    st.title("Healthcare Analytics Dashboard")
    st.write("This dashboard is currently in development.")

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
    #st.write(insights_dict)

    insight_dict = set_tab(insights_dict)

    if insights_dict:
        insight_data = list(insights_dict.values())[0]  # Get the one selected insight
        insight_title = list(insights_dict.keys())[0]

        st.subheader(insight_data.get("pretty_name", insight_title))

        tab_obj = Tab({insight_title: insight_data}, None)
        tab_obj.display_description()
        tab_obj.set_options()
    else:
        st.warning("No insight selected or available.")
    

    #tabs = build_tabs(insights)

if __name__ == "__main__":
    main()
'''