import streamlit as st
from datetime import datetime
import sys, os

sys.path.append(os.path.abspath("src"))
import expert

if "result" not in st.session_state:
    st.session_state.result = {}  # Initialize with None

@st.dialog("Expert System Result")
def display_result(result):
    # Add a header with nice styling
    st.markdown("### 📊 Financial Analysis Results")
    st.markdown("---")

    # Create columns for better layout
    for elt in result.keys():
        if elt == "rule_50_30_20":
            # Rule 50/30/20 section with better visualization
            st.markdown("#### 💰 Budget Rule Analysis (50/30/20)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📈 Recommended Distribution")
                for category, value in zip(['Essentials', 'Discretionary', 'Savings'], result[elt]["recommended"]):
                    st.metric(
                        label=category,
                        value=f"{value:.1f}%",
                        delta=f"{value - result[elt]['actual'][result[elt]['recommended'].index(value)]:.1f}%"
                    )

            with col2:
                st.markdown("##### 📊 Your Current Distribution")
                for category, value in zip(['Essentials', 'Discretionary', 'Savings'], result[elt]["actual"]):
                    st.progress(value/100)
                    st.caption(f"{category}: {value:.1f}%")

            st.markdown("---")
            
        else:
            # Other results with card-like presentation
            with st.container():
                st.markdown(f"#### 📋 {elt.replace('_', ' ').title()}")
                st.info(str(result[elt]))
                st.markdown("---")
    
    # Add helpful context at the bottom
    with st.expander("💡 Understanding Your Results"):
        st.markdown("""
        - **50/30/20 Rule**: A budgeting principle where:
            - 50% goes to essential expenses
            - 30% goes to discretionary spending
            - 20% goes to savings
        - **Green arrows** indicate you're meeting or exceeding targets
        - **Red arrows** show areas that need attention
        """)



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

st.title("💡 Financial Advisor")

st.markdown("### 📋 Provide Your Details Below")
st.markdown("---")

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

# Expenses categories multiselect outside the form
options = st.multiselect(
    "Select all your expense categories",
    expert.vital_expenses + expert.non_mandatory_expenses,
    [],
    help="Choose all the categories of expenses applicable to you.",
)

# Form for user inputs
with st.form("ExpertForm"):
    st.markdown("#### Income and Savings")
    col1, col2 = st.columns(2)

    with col1:
        # Income input
        income = st.number_input(
            "What's your monthly income",
            value=None,
            placeholder="Enter your salary...",
            help="Provide your net monthly income after taxes.",
        )
        if st.session_state.errors["income"]:
            st.error(f"❌ {st.session_state.errors['income']}")

    with col2:
        # Saving input
        saving = st.number_input(
            "What's your current savings",
            value=None,
            placeholder="Enter your savings...",
            help="Provide the total amount of your current savings.",
        )
        if st.session_state.errors["saving"]:
            st.error(f"❌ {st.session_state.errors['saving']}")

    st.markdown("#### Financial Goals")
    # Goal description input
    goal_description = st.text_input(
        "Goal Description",
        "",
        placeholder="E.g., Buy a car, Save for a house...",
        help="Describe your financial goal briefly.",
    )
    if st.session_state.errors["goal_description"]:
        st.error(f"❌ {st.session_state.errors['goal_description']}")

    # Savings target
    saving_target = st.number_input(
        "Target Amount",
        value=None,
        placeholder="Enter your target savings amount...",
        help="Specify the total amount you aim to save for this goal.",
    )
    if st.session_state.errors["saving_target"]:
        st.error(f"❌ {st.session_state.errors['saving_target']}")

    # Savings timeline
    saving_timeline = st.date_input(
        "Target Timeline",
        None,
        help="Pick the date by which you plan to achieve this goal.",
    )
    if st.session_state.errors["saving_timeline"]:
        st.error(f"❌ {st.session_state.errors['saving_timeline']}")

    st.markdown("#### Expense Details")
    # Dynamically create inputs for expense categories
    vital_expenses_data = {}
    non_vital_expenses_data = {}

    for expense_category in options:
        expense_cost = st.number_input(
            expense_category,
            value=None,
            placeholder="Enter the cost...",
            help=f"Provide the cost associated with {expense_category}.",
        )
        if (
            expense_category in st.session_state.errors["expenses"]
            and st.session_state.errors["expenses"][expense_category]
        ):
            st.error(f"❌ {st.session_state.errors['expenses'][expense_category]}")

        if expert.verifyExpenseIsMandatory(expense_category):
            vital_expenses_data[expense_category] = expense_cost
        else:
            non_vital_expenses_data[expense_category] = expense_cost

    # Submit button
    st.markdown("---")
    submit_button = st.form_submit_button(label="🚀 Submit")

# Handle form submission and validation
if submit_button:
    # Reset error messages
    st.session_state.errors = {
        "income": "",
        "saving": "",
        "goal_description": "",
        "saving_target": "",
        "saving_timeline": "",
        "expenses": {},
    }

    # Validate inputs
    has_errors = False

    if income is None or income <= 0:
        st.session_state.errors["income"] = "Income must be a positive number."
        has_errors = True

    if saving is None or saving < 0:
        st.session_state.errors["saving"] = "Savings must be a non-negative number."
        has_errors = True

    if not goal_description.strip():
        st.session_state.errors["goal_description"] = "Goal description cannot be empty."
        has_errors = True

    if saving_target is None or saving_target <= 0:
        st.session_state.errors["saving_target"] = "Target must be a positive number."
        has_errors = True

    if saving_timeline is None:
        st.session_state.errors["saving_timeline"] = "Please select a timeline."
        has_errors = True

    for category, cost in {**vital_expenses_data, **non_vital_expenses_data}.items():
        if cost is None or cost <= 0:
            st.session_state.errors["expenses"][category] = "Cost must be a positive number."
            has_errors = True

    # Process the form if no errors
    if not has_errors:
        result = expert.main(
            vital_expenses_data,
            non_vital_expenses_data,
            goal_description,
            income,
            saving_target,
            saving,
            get_Timeline(saving_timeline),
        )
        st.session_state.result = {
            "data": result,
            "done": True,
        }
        st.success("✅ Form submitted successfully! View results below.")
    else:
        st.warning("⚠️ Please fix the errors and try again.")