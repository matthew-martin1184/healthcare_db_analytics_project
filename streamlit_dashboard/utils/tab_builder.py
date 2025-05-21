import streamlit as st
import pickle

class TabBuilder:
    def __init__(self, tab, pretty_name):
        self.tab = tab
        self.pretty_name = pretty_name

        st.write(f"Testing the **{self.pretty_name}** tab.")