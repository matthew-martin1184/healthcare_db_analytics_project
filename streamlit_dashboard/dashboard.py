import streamlit as st
import pandas as pd
import os
import pickle
import matplotlib as plt

@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "dataframes.pkl")
    with open(file_path, "rb") as f:
        data = pickle.load(f)

    return data['summary_df'], data['result_set_dict'], data["cat_desc"]


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

    insights = st.multiselect(label="Select insights to view", 
                              options=cat_df["query_name"].unique(),
                              default=None, format_func=lambda x: name_map.get(x, x),

                              )
    return insights

def main():
    st.title("Healthcare Analytics Dashboard")

    global summary_df, result_set_dict, cat_desc 
    summary_df, result_set_dict, cat_desc = load_data()

    category = st.selectbox(
        "View insights by category",  # Label above the dropdown
        ["Doctor", "Patient", "Medical Procedure", "Billing"]  # Options
    )
    st.write(cat_desc[category])
    cat_df = set_category_filter(category)

    set_insights(cat_df)

    insights_list = st.multiselect(label="Select insights to view", 
                              options=cat_df["query_name"].unique(),
                              default=None, format_func=lambda x: x['pretty_name']
                              )



if __name__ == "__main__":
    main()
