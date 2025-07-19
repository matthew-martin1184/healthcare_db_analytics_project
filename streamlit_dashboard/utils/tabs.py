import streamlit as st
import pandas as pd

class Tabs:
    def __init__(self, insights_dict):
        self.insight_data = list(insights_dict.values())[0]
        self.table = self.insight_data.get('result_set', None)
        #self.tab_names = ['Table']
        #self.tab_objs = []
        #self.create_tabs()
        

    def display(self):
        table_tab, = st.tabs(['Table'])

        with table_tab:
            self.render_table()

    def render_table(self):
        if self.table is not None:
            st.dataframe(self.table)

