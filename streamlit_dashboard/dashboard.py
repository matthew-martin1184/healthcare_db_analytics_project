import streamlit as st
import pandas as pd
import pickle
import matplotlib as plt

file_path = "data/dataframes.pkl"
with open(file_path, "rb") as f:
    data = pickle.load(f)

query_df = data['query_df']
doctor_result_dict = data['doctor_result_dict']
patient_result_dict = data['patient_result_dict']
procedure_result_dict = data['procedure_result_dict']
billing_result_dict = data['billing_result_dict']

st.title("Healthcare Analytics Dashboard")
