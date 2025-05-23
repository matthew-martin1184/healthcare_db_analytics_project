import streamlit as st
import pandas as pd

class Tab:
    def __init__(self, insight, tab):
        self.insight_name, self.insight_dict = next(iter(insight.items()))
        self.tab_container = tab

    def display_description(self):
        #st.write("Insight contents:", self.insight)
        show_long = st.toggle("Show detailed description", value=False,
                              key=f"{self.insight_name}_toggle")
        if show_long:
            st.write(self.insight_dict["long_description"])
        else:
            st.write(self.insight_dict["description"])

    def set_options(self):
        col1, col2, col3 = st.columns(3)
        with col1:
            self.show_table = st.checkbox(
                "Display insight table", value=True, key=f"{self.insight_name}_show_table"
            )
        with col2:
            self.show_plot = st.checkbox(
                "Plot insight results", value=False, key=f"{self.insight_name}_show_plot"
            )
        with col3:
            self.show_summary = st.checkbox(
                "Display insight interpretation", value=False, key=f"{self.insight_name}_show_summary"
            )