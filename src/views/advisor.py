import streamlit as st
from datetime import datetime
import sys, os

sys.path.append(os.path.abspath("src"))
import expert

import pandas as pd
import numpy as np

def get_Timeline(date_string):

    # Get the current date
    current_date = datetime.now()
    months_difference = 0

    # Calculate the difference in years and months
    years_difference = date_string.year - current_date.year
    if years_difference == 0:
        return date_string.month - current_date.month
    elif years_difference >= 2:
        months_difference += years_difference* 12
    remaining_months_untill_end_year_current_date =  12 - current_date.month 
    months_difference += date_string.month + remaining_months_untill_end_year_current_date

    return months_difference

st.title("Advisor")

# Initialize error message holders in session state
if "income_error" not in st.session_state:
    st.session_state.income_error = ""
if "saving_error" not in st.session_state:
    st.session_state.saving_error = ""
if "goal_description_error" not in st.session_state:
    st.session_state.goal_description_error = ""
if "saving_target_error" not in st.session_state:
    st.session_state.saving_target_error = ""
if "saving_timeline_error" not in st.session_state:
    st.session_state.saving_timeline_error = ""
if "expense_errors" not in st.session_state:
    st.session_state.expense_errors = {}

# Form for inputs
with st.form("ExpertForm"):
    # Income input
    income = st.number_input(
        "What's your monthly income", value=None, placeholder="Type a salary..."
    )
    if st.session_state.income_error:
        st.error(st.session_state.income_error)
    # st.markdown(
    #     f"<span style='color: red;'>{st.session_state.income_error}</span>",
    #     unsafe_allow_html=True,
    # )


    saving = st.number_input(
        "What's your actual saving", value=None, placeholder="Type an amount..."
    )
    # Current saving
    if st.session_state.saving_error:
        st.error(st.session_state.saving_error)
    # st.markdown(
    #     f"<span style='color: red;'>{st.session_state.saving_error}</span>",
    #     unsafe_allow_html=True,
    # )

    # Goal description input
    goal_description = st.text_input("What is your goal description", "")
    # st.markdown(
    #     f"<span style='color: red;'>{st.session_state.goal_description_error}</span>",
    #     unsafe_allow_html=True,
    # )
    if st.session_state.goal_description_error:
        st.error(st.session_state.goal_description_error)

    # Savings target
    saving_target = st.number_input(
        "What's your saving target", value=None, placeholder="Type an amount..."
    )
    # st.markdown(
    #     f"<span style='color: red;'>{st.session_state.saving_target_error}</span>",
    #     unsafe_allow_html=True,
    # )
    if st.session_state.saving_target_error:
        st.error(st.session_state.saving_target_error)

    # Savings timeline
    saving_timeline = st.date_input("What's the saving goal timeline", None)
    st.write(saving_timeline)
    # st.markdown(
    #     f"<span style='color: red;'>{st.session_state.saving_timeline_error}</span>",
    #     unsafe_allow_html=True,
    # )
    if st.session_state.saving_timeline_error:
        st.error(st.session_state.saving_timeline_error)

    # Expense category selection
    options = st.multiselect(
        "Select all your expenses categories",
        expert.vital_expenses + expert.non_mandatory_expenses,
        [],
    )

    # Dictionaries to store expense data
    vital_expenses_data = {}
    non_vital_expenses_data = {}

    # Dynamically create inputs for expense categories
    for expense_category in options:
        expense_cost = st.number_input(
            expense_category, value=None, placeholder="Type a cost..."
        )
        if expense_category not in st.session_state.expense_errors:
            st.session_state.expense_errors[expense_category] = ""

        if st.session_state.expense_error[expense_category]:
            st.error(st.session_state.expense_error[expense_category])
        # st.markdown(
        #     f"<span style='color: red;'>{st.session_state.expense_errors[expense_category]}</span>",
        #     unsafe_allow_html=True,
        # )
        if expert.verifyExpenseIsMandatory(expense_category):
            vital_expenses_data[expense_category] = expense_cost
        else:
            non_vital_expenses_data[expense_category] = expense_cost

    # Submit button
    submit_button = st.form_submit_button(label="Submit")

# Validation logic: Only execute if the form is submitted
if submit_button:
    # Reset error messages
    st.session_state.income_error = ""
    st.session_state.saving_error = ""
    st.session_state.goal_description_error = ""
    st.session_state.saving_target_error = ""
    st.session_state.saving_timeline_error = ""
    st.session_state.expense_errors = {category: "" for category in options}

    # Validate income
    if income is None or income <= 0:
        st.session_state.income_error = "Income must be a positive number."

    # Validate savings
    if saving is None or saving < 0:
        st.session_state.saving_error = "Saving must be a non-negative number."

    # Validate goal description
    if not goal_description.strip():
        st.session_state.goal_description_error = "Goal description cannot be empty."

    # Validate saving target
    if saving_target is None or saving_target <= 0:
        st.session_state.saving_target_error = "Saving target must be a positive number."

    # Validate saving timeline
    if saving_timeline is None:
        st.session_state.saving_timeline_error = "Saving timeline must be selected."

    # Validate expense categories
    if options:
        for category, cost in {**vital_expenses_data, **non_vital_expenses_data}.items():
            if cost is None or cost <= 0:
                st.session_state.expense_errors[category] = "Cost must be a positive number."

# Process the form submission if there are no errors
if submit_button and not any(
    [
        st.session_state.income_error,
        st.session_state.saving_error,
        st.session_state.goal_description_error,
        st.session_state.saving_target_error,
        st.session_state.saving_timeline_error,
    ]
) and not any(st.session_state.expense_errors.values()):
    expert.main(
        vital_expenses_data,
        non_vital_expenses_data,
        goal_description,
        income,
        saving_target,
        saving,
        get_Timeline(saving_timeline),
    )


# chart_data = pd.DataFrame(
#     {
#         "col1": list(range(20)),
#         "col2": np.random.randn(20),
#         "col3": np.random.randn(20),
#     }
# )

# st.bar_chart(
#     chart_data,
#     x="col1",
#     y=["col2", "col3"],
#     color=["#FF0000", "#0000FF"],  # Optional
#)