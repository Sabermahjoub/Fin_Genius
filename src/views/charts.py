import streamlit as st
import pandas as pd
import json , re
import plotly.express as px
import os


# Page Title
st.title("📊 Charts Dashboard")
st.write("Welcome to the Charts Dashboard! Explore insights with interactive charts.")


def vital_expenses_by_category(data):
    st.subheader("Vital Expenses by category")
    chart_data = pd.DataFrame(
            {
                "Category": data["vital_expenses"].keys(),
                "Expense value": data["vital_expenses"].values(),
            }
        )
    bar_chart1 = px.bar(
        chart_data,
        x="Category",
        y="Expense value",
        title="Vital expenses by Category",
        color="Category",
        template="plotly_dark",
        text_auto=True
    )
    st.plotly_chart(bar_chart1, use_container_width=True)

def non_vital_expenses_by_category(data):
    st.subheader("Non Vital Expenses by category")
    chart2_data = pd.DataFrame(
            {
                "Category": data["non_vital_expenses"].keys(),
                "Expense value": data["non_vital_expenses"].values(),
            }
        )
    bar_chart2 = px.bar(
        chart2_data,
        x="Category",
        y="Expense value",
        title="Non-vital expenses by Category",
        color="Category",
        template="plotly_dark",
        text_auto=True
    )
    st.plotly_chart(bar_chart2, use_container_width=True)

def vital_expenses_proportion(data):
    st.subheader("Proportion of Vital Expenses by Category")
    chart_data = pd.DataFrame(
            {
                "Category": data["vital_expenses"].keys(),
                "Expenses": data["vital_expenses"].values(),
                "Income": [data["income"]] * len(data["vital_expenses"].keys())
            }
        )
    chart_data["Proportion (%)"] = (chart_data["Expenses"] / chart_data["Income"]) * 100
    pie_chart1 = px.pie(
        chart_data,
        names="Category",
        values="Proportion (%)",
        title="Proportion of Expenses by Category",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(pie_chart1, use_container_width=True)

def income_pie_chart(data):
    st.subheader("Income Proportion by Category")
    expenses=data["non_vital_expenses"]
    expenses.update(data["vital_expenses"])
    match = re.search(r":\s*(\d+)", data["result"]["savings_rate"])
    if match:
        savings_rate = int(match.group(1))
        expenses.update({"savings rate" : savings_rate})
    chart_data = pd.DataFrame(
            {
                "Category": expenses.keys(),
                "Expenses": expenses.values(),
                "Income": [data["income"]] * len(expenses.keys())
            }
        )
    chart_data["Proportion (%)"] = (chart_data["Expenses"] / chart_data["Income"]) * 100
    proportion_chart = px.pie(
        chart_data,
        names="Category",
        values="Proportion (%)",
        title="Income Proportion by Category",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(proportion_chart, use_container_width=True, key=1)

def rule_50_30_20_chart(data):

    #Grouped Bar chart
    st.subheader("Rule 50_30_20 - Actual vs Recommended")

    if data["result"].get("follow_recommendations_warning"):
        st.warning(data["result"]["follow_recommendations_warning"], icon="⚠️")
    elif data["result"].get("follow_recommendations_success"):
        st.success(data["result"]["follow_recommendations_success"], icon="✅")

    chart_data = pd.DataFrame({
        "Category": ["Essentials", "Discretionary", "Savings"],
        "Actual": data["result"]["rule_50_30_20"]["actual"],
        "Recommended": data["result"]["rule_50_30_20"]["recommended"]
    })

    # Melt DataFrame to long format for grouped bar chart
    data_melted = chart_data.melt(id_vars="Category", value_vars=["Actual", "Recommended"], 
                            var_name="Type", value_name="Value")
    bar_chart = px.bar(
        data_melted,
        x="Category",
        y="Value",
        color="Type",
        barmode="group",  # Group bars side by side
        title="Comparison of Actual vs Recommended Values",
        labels={"Value": "Amount (DNT)"},
        template="plotly_dark",
        text_auto=True
    )
    st.plotly_chart(bar_chart, use_container_width=True)

# Open and read the JSON file
# Check if the file is empty or invalid
def is_file_empty_or_invalid(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return False
    return True

try:
    file_path = 'result.json'

    # Check for empty file
    if is_file_empty_or_invalid(file_path):
        st.warning("Please fill in the form on the advisor page to be able to visualize charts", icon="⚠️")
    else:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Check if data is an empty object or invalid
        if not data:
            st.warning("Please fill in the form on the advisor page to be able to visualize charts", icon="⚠️")
        else:
            # chart logic
            rule_50_30_20_chart(data)
            if data.get("vital_expenses"):  # Safely check if key exists and is not empty
                vital_expenses_by_category(data)
            if data.get("non_vital_expenses"):  # Safely check if key exists and is not empty
                non_vital_expenses_by_category(data)
            income_pie_chart(data)

except json.JSONDecodeError:
    st.write("Error: result.json is not properly formatted. Please check the file content.")
except Exception as e:
    st.write(f"An unexpected error occurred: {e}")


# Footer
st.markdown("---")
st.write("🔍 Insights powered by Fin Genius App")