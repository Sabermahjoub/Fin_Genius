import streamlit as st
import pandas as pd
import numpy as np
import json

# Open and read the JSON file
with open('result.json', 'r') as file:
    data = json.load(file)

def vital_expenses_bar_chart():
    chart_data = pd.DataFrame(
        {
            "categories": data["vital_expenses"].keys(),
            "expense value": data["vital_expenses"].values(),
        }
    )
    st.bar_chart(
        chart_data,
        x="categories",
        y="expense value",
        color=["#FF0000"],  # Optional
    )
def non_vital_expenses_bar_chart():
    chart_data = pd.DataFrame(
        {
            "categories": data["non_vital_expenses"].keys(),
            "expense value": data["non_vital_expenses"].values(),
        }
    )
    st.bar_chart(
        chart_data,
        x="categories",
        y="expense value",
        color=["#000H02"],  # Optional
    )

vital_expenses_bar_chart()
non_vital_expenses_bar_chart()
def vital_expenses_bar_chart():
    chart_data = pd.DataFrame(
        {
            "categories": data["vital_expenses"].keys(),
            "expense value": data["vital_expenses"].values(),
        }
    )
    st.bar_chart(
        chart_data,
        x="categories",
        y="expense value",
        color=["#FF0000"],  # Optional
    )
