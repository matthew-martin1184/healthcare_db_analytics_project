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

def set_category_filter(category):
    if category == "Doctor":
        df = summary_df[summary_df["source_file"] == 'doctor_queries.sql']
    elif category == "Patient":
        df = summary_df[summary_df["source_file"] == 'patient_queries.sql']
    elif category == "Medical Procedure":
        df = summary_df[summary_df["source_file"] == 'procedure_queries.sql']
    elif category == "Billing":
        df = summary_df[summary_df["source_file"] == 'billing_queries.sql']
    else:
        raise ValueError("Invalid category selected")
    return df

def set_insights(cat_df):

    name_map = dict(zip(cat_df["query_name"], cat_df["pretty_name"]))

    insights = st.multiselect(label="Select up to 4 insights to view", 
                                options=cat_df["query_name"].unique(),
                                format_func=lambda x: name_map.get(x, x),
                                max_selections=4,
                                key='insights_multiselect_key'
                              )
    return insights

def set_tabs(insights_list):
    filtered_df = summary_df[summary_df["query_name"].isin(insights_list)]
    pretty_tabs = dict(zip(filtered_df["query_name"], filtered_df["pretty_name"]))
    pretty_list = list(pretty_tabs.values())
    pretty_list = [pretty_tabs[insight] for insight in insights_list if insight in pretty_tabs]

    tabs = []

    if insights_list:
        tabs = st.tabs(pretty_list)

        for tab, pretty_name in zip(tabs, pretty_list):
            with tab:
                tab = TabBuilder(tab, pretty_name)
'''

    if insights_list:
        tabs = st.tabs(pretty_list)

        for tab, pretty_name in zip(tabs, pretty_list):
            with tab:
                #st.write(f"This is the **{pretty_name}** tab.")
                with st.container():
                    desc = st.toggle(label="Detailed Description", key=f"toggle_key_{pretty_name}")
                    if desc:
                        st.write(filtered_df[filtered_df["pretty_name"] == pretty_name].iloc[0]["long_description"])
                    else:    
                        st.write(filtered_df[filtered_df["pretty_name"] == pretty_name].iloc[0]["description"])
                    st.markdown(f"###### Viewing options for {pretty_name} results")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        tab_results_table_cbox = st.checkbox(label="Show results table", value=True, key=f"tab_results_table_cbox_key_{pretty_name}")
                    with col2:
                        tab_results_plot_cbox = st.checkbox(label="Plot results", value=True, key=f"tab_results_plot_cbox_key_{pretty_name}")
                    with col3:
                        tab_deep_analysis_cbox = st.checkbox(label="Analysis options", value=False, key=f"tab_deep_analysis_cbox_key_{pretty_name}")
                    with col4:
                        tab_interpretation_cbox = st.checkbox(label="Interpretations", value=False, key=f"tab_interpretation_cbox_key_{pretty_name}")
    else:
        st.info("No insights available.")
    return tabs
'''
def main():
    st.title("Healthcare Analytics Dashboard")

    global summary_df, result_set_dict, cat_desc 
    data = load_pickle_from_github()
    summary_df = data["summary_df"]
    result_set_dict = data["result_set_dict"]
    cat_desc = data["cat_desc"]

    #st.sidebar.title("Dashboard Options")
    #st.sidebar.write("Select options for viewing and filtering insights")

    category = st.selectbox(
        "View insights by category",  # Label above the dropdown
        ["Doctor", "Patient", "Medical Procedure", "Billing"]  # Options
    )
    st.write(cat_desc[category])
    cat_df = set_category_filter(category)

    insights_list = set_insights(cat_df)
    #st.write("TEST#######", insights_list)

    tabs = set_tabs(insights_list)




if __name__ == "__main__":
    main()
