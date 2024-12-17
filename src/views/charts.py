import streamlit as st
import pandas as pd
import json , re
import plotly.express as px
import os


# Page Title
st.title("📊 Charts Dashboard")
st.write("Welcome to the Charts Dashboard! Explore insights with interactive charts.")

username = st.session_state["authenticated_user"]


# Chart for solution proposed from the expert advisor (with timelines)
def display_line_charts(data):
    print()
    st.subheader("Proposed monthly savings with timeline")
    
    # Extract the two saving plans and their respective lengths
    length_1 = int(data["budget_adjustement_solution_1"][1][-2:])
    length_2 = int(data["budget_adjustement_solution_2"][1][-2:])
    
    # Determine the maximum length
    max_length = max(length_1, length_2)
    
    # Fill shorter arrays with 0
    first_saving_plan = [data["budget_adjustement_solution_1"][0]] * length_1 + [0] * (max_length - length_1)
    second_saving_plan = [data["budget_adjustement_solution_2"][0]] * length_2 + [0] * (max_length - length_2)
    
    # Create a DataFrame
    chart_data = pd.DataFrame(
        {
            "Month": list(range(1, max_length + 1)),  # X-axis for months
            "Needed savings per month": first_saving_plan,
            "Current savings per month": second_saving_plan,
        }
    )
     # Create a Plotly chart with axis labels
    fig = px.line(
        chart_data, 
        x="Month", 
        y=["Needed savings per month", "Current savings per month"],
        labels={"value": "Savings Amount (TND)", "variable": "Saving Plan"},
        title=data["goal_description"]
    )
    fig.update_yaxes(title_text="Savings Amount (TND)")  # Y-axis label
    fig.update_xaxes(title_text="Months")             # X-axis label
    
    st.plotly_chart(fig)
    
    # Plot the line chart
    # st.line_chart(chart_data, x="Month", y=["First saving plan", "Second saving plan"])




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
    st.plotly_chart(proportion_chart, use_container_width=True)

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

        if not data or not data[username]:
            st.warning("Please fill in the form on the advisor page to be able to visualize charts", icon="⚠️")

        else:
            # chart logic
            rule_50_30_20_chart(data[username])
            if data[username].get("result").get("budget_adjustement_solution_1") and data[username].get("result").get("budget_adjustement_solution_2"):
                display_line_charts(data[username]["result"])
            if data[username].get("vital_expenses"):  # Safely check if key exists and is not empty
                vital_expenses_by_category(data[username])
            if data[username].get("non_vital_expenses"):  # Safely check if key exists and is not empty
                non_vital_expenses_by_category(data[username])
            income_pie_chart(data[username])

except json.JSONDecodeError:
    st.write("Error: result.json is not properly formatted. Please check the file content.")
except Exception as e:
    st.write(f"An unexpected error occurred: {e}")


# Footer
st.markdown("---")
st.write("🔍 Insights powered by Fin Genius App")