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
    
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Failed to download .pkl file from GitHub.")
        return None

    file_like = io.BytesIO(response.content)
    data = pickle.load(file_like)
    
    return data


def main():
    st.title("Healthcare Analytics Dashboard")

    global summary_df, result_set_dict, cat_desc 
    data = load_pickle_from_github()
    summary_df = data["summary_df"]
    result_set_dict = data["result_set_dict"]
    cat_desc = data["cat_desc"]

category = st.selectbox(
        "View insights by category",  # Label above the dropdown
        ["Doctor", "Patient", "Medical Procedure", "Billing"]  # Options
    )    

if __name__ == "__main__":
    main()