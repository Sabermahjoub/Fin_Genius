import streamlit as st
from datetime import datetime
import sys, os

sys.path.append(os.path.abspath("src"))
import expert

def get_Timeline(date_string):
    # Get the current date
    current_date = datetime.now()
    months_difference = 0

    # Calculate the difference in years and months
    years_difference = date_string.year - current_date.year
    if years_difference == 0:
        return date_string.month - current_date.month
    elif years_difference >= 2:
        months_difference += years_difference * 12
    remaining_months_untill_end_year_current_date = 12 - current_date.month
    months_difference += date_string.month + remaining_months_untill_end_year_current_date

    return months_difference

st.title("Advisor")

# Initialize session state for form validation
if "errors" not in st.session_state:
    st.session_state.errors = {
        "income": "",
        "saving": "",
        "goal_description": "",
        "saving_target": "",
        "saving_timeline": "",
        "expenses": {}
    }

# Move multiselect outside the form
options = st.multiselect(
    "Select all your expenses categories",
    expert.vital_expenses + expert.non_mandatory_expenses,
    [],
)

# Form for inputs
with st.form("ExpertForm"):
    # Income input
    income = st.number_input(
        "What's your monthly income", value=None, placeholder="Type a salary..."
    )
    if st.session_state.errors["income"]:
        st.error(st.session_state.errors["income"])

    # Saving input
    saving = st.number_input(
        "What's your actual saving", value=None, placeholder="Type an amount..."
    )
    if st.session_state.errors["saving"]:
        st.error(st.session_state.errors["saving"])

    # Goal description input
    goal_description = st.text_input("What is your goal description", "")
    if st.session_state.errors["goal_description"]:
        st.error(st.session_state.errors["goal_description"])

    # Savings target
    saving_target = st.number_input(
        "What's your saving target", value=None, placeholder="Type an amount..."
    )
    if st.session_state.errors["saving_target"]:
        st.error(st.session_state.errors["saving_target"])

    # Savings timeline
    saving_timeline = st.date_input("What's the saving goal timeline", None)
    if st.session_state.errors["saving_timeline"]:
        st.error(st.session_state.errors["saving_timeline"])

    # Dictionaries to store expense data
    vital_expenses_data = {}
    non_vital_expenses_data = {}

    # Dynamically create inputs for expense categories
    for expense_category in options:
        expense_cost = st.number_input(
            expense_category, value=None, placeholder="Type a cost..."
        )
        if expense_category in st.session_state.errors["expenses"] and st.session_state.errors["expenses"][expense_category]:
            st.error(st.session_state.errors["expenses"][expense_category])
        
        if expert.verifyExpenseIsMandatory(expense_category):
            vital_expenses_data[expense_category] = expense_cost
        else:
            non_vital_expenses_data[expense_category] = expense_cost

    # Submit button
    submit_button = st.form_submit_button(label="Submit")

# Handle form submission and validation
if submit_button:
    # Reset error messages
    st.session_state.errors = {
        "income": "",
        "saving": "",
        "goal_description": "",
        "saving_target": "",
        "saving_timeline": "",
        "expenses": {}
    }

    # Validate inputs
    has_errors = False

    # Validate income
    if income is None or income <= 0:
        st.session_state.errors["income"] = "Income must be a positive number."
        has_errors = True

    # Validate savings
    if saving is None or saving < 0:
        st.session_state.errors["saving"] = "Saving must be a non-negative number."
        has_errors = True

    # Validate goal description
    if not goal_description.strip():
        st.session_state.errors["goal_description"] = "Goal description cannot be empty."
        has_errors = True

    # Validate saving target
    if saving_target is None or saving_target <= 0:
        st.session_state.errors["saving_target"] = "Saving target must be a positive number."
        has_errors = True

    # Validate saving timeline
    if saving_timeline is None:
        st.session_state.errors["saving_timeline"] = "Saving timeline must be selected."
        has_errors = True

    # Validate expense categories
    if options:
        for category, cost in {**vital_expenses_data, **non_vital_expenses_data}.items():
            if cost is None or cost <= 0:
                st.session_state.errors["expenses"][category] = "Cost must be a positive number."
                has_errors = True

    # If no errors, process the form
    if not has_errors:
        expert.main(
            vital_expenses_data,
            non_vital_expenses_data,
            goal_description,
            income,
            saving_target,
            saving,
            get_Timeline(saving_timeline),
        )
    
    # Force a rerun to show errors immediately
    st.rerun()