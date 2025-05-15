import streamlit as st
import pandas as pd
import os
import pickle
import matplotlib as plt

file_path = os.path.join(os.path.dirname(__file__), "..", "data", "dataframes.pkl")
with open(file_path, "rb") as f:
    data = pickle.load(f)

query_df = data['query_df']
doctor_result_dict = data['doctor_result_dict']
patient_result_dict = data['patient_result_dict']
procedure_result_dict = data['procedure_result_dict']
billing_result_dict = data['billing_result_dict']

# Title
st.title("Healthcare Analytics Dashboard")

category = st.selectbox(
    "View insights by category",  # Label above the dropdown
    ["Doctor", "Patient", "Medical Procedure", "Billing"]  # Options
)

# Conditional content based on selection
if category == "Doctor":
    st.write("These insights focus on provider workload, capacity, and performance, helping identify how effectively doctor resources are being utilized and whether any are over or under-worked.")
elif category == "Patient":
    st.write("These insights analyze patient-centric metrics, shedding light on how patients utilize services and the nature of the patient population. They help identify high-demand patients, patient turnover, and complexity of cases, informing how patient load drives resource needs.")
elif category == "Medical Procedure":
    st.write("These insights focus on medical procedures - how often they are performed, who performs them, and how they contribute to workload and revenue. Understanding procedure frequency and distribution helps in assessing whether the hospital is equipped to meet procedural demand and if certain procedures strain resources or generate significant income.")
elif category == "Billing":
    st.write("These insights connect clinical activity to financial outcomes, highlighting how patient visits and procedures translate into billing. They help rank the revenue contribution by doctor and patient, uncover trends over time, and identify peak revenue periods, informing both operational and financial decisions.")
