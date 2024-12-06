from experta import *
import math

# -- USER INPUTS --
# We're on the fourth of december
# My salary is : 2500Dt 
# I would like to save 3000Dt (Target amount), Goal description (vacation : going to Japan)
# This goal should be achieved by June 2025
# My current savings are : 100Dt (Zaweli allah ghaleb)
# I spend on rent : 800Dt, on groceries 300Dt, on transport 100Dt, leisure 250Dt, animal needs : 100Dt 

# -- Expert system output --
# 1- classify the expenses based on the 50-30-20 rule
# 2- Calculate savings rate
# 3- Feasibilitycheck :  if income > expenses + savings goals (rate per month) =>
#   if yes : Good, continue with that expenses rate
#   if no : propose a budget adjustment to meet savings goals ex. Reduce leisure by 10%
# 4 - if yes in (3) Milestone generation 
# 5 - progress tracking
# 6- charts


# List of Mandatory (Vital) Expenses
vital_expenses = [
    "rent",
    "utilities",
    "groceries",
    "transportation",
    "insurance",
    "medical",
    "education",
    "loan_repayment",
    "pet_expenses",
]

# List of Non-Mandatory (Optional) Expenses
non_mandatory_expenses = [
    "leisures",
    "gaming",
    "dining_out",
    "vacation",
    "hobbies",
    "subscriptions",
    "shopping",
    "gym_membership",
    "beauty_care",
    "alcohol",
    "socializing",
    "events",
]
result = {}

class Finances(Fact):
    """Fact containing information about the financial situation."""
    pass

class SavingsGoalTracker(KnowledgeEngine):

    @Rule(Fact(monthly_income=MATCH.income), Fact(monthly_expenses=MATCH.expenses))
    def calculate_savings_rate(self, income, expenses):
        """Calculates the monthly savings rate."""
        savings_rate = income - expenses
        result["savings_rate"] = (f"Calculated savings rate: {savings_rate}")
        self.declare(Fact(savings_rate=savings_rate))

    @Rule(
        Fact(savings_rate=MATCH.savings_rate),
        Fact(target_amount=MATCH.target),
        Fact(timeline=MATCH.timeline),
    )
    def feasibility_check(self, savings_rate, target, timeline):
        """Checks if the savings goal is achievable within the timeline."""
        required_rate = target / timeline
        if savings_rate >= required_rate:
            self.declare(Fact(goal_achievable=True))
            result["feasibility_check"]="Goal is achievable."
        else:
            self.declare(Fact(suggest_adjustments=True))
            result["feasibility_check"]=("Goal is not achievable. Consider budget adjustments.")

    @Rule(Fact(goal_achievable=True), Fact(target_amount=MATCH.target), Fact(timeline=MATCH.timeline))
    def generate_milestones(self, target, timeline):
        """Generates monthly milestones to track progress."""
        monthly_milestone = target / timeline
        self.declare(Fact(monthly_milestone=monthly_milestone))
        result["milestone"]= (f"To reach your goal, save {monthly_milestone:.2f} per month.")

    @Rule(Fact(current_savings=MATCH.savings), Fact(monthly_milestone=MATCH.milestone))
    def track_progress(self, savings, milestone):
        """Tracks progress against the savings milestones."""
        if savings == milestone :
            result["progress"]=("Congratulations! You've achieved your monthly milestone.")
        if savings > milestone:
            #TODO : When current saving > milestone => -- na9es milestone eli 
            # Si (we keep the same milestone) => you overpass the goal -- yofdholek flous ba3ed el goal -- 
            # Or we can na9sou milestone 
            result["progress"]=("Congratulations! You've achieved your monthly milestone.")
        else:
            result["progress"]=(f"You are behind. You need to save at least {milestone - savings:.2f} more this month.")

    @Rule(Fact(suggest_adjustments=True))
    def suggest_budget_adjustments(self):
        """Suggests budget adjustments to meet savings goals."""
        # TODO: Add how to adjust
        result["budget_adjustement"]= "Consider reducing discretionary expenses to increase your savings rate."

def verifyExpenseIsMandatory(expense_name):
    return expense_name in vital_expenses

def apply_50_30_20_rule(income, vital_expenses, non_vital_expenses):
    """Applies the 50-30-20 rule to classify spending."""
    essentials_limit = 0.5 * income
    discretionary_limit = 0.3 * income
    savings_limit = 0.2 * income

    actual_essentials = sum(vital_expenses.values())
    actual_discretionary = sum(non_vital_expenses.values())
    actual_savings = income - (actual_essentials + actual_discretionary)

    result["rule_50_30_20"] = {
        "recommended": [essentials_limit, discretionary_limit, savings_limit],
        "actual": [actual_essentials, actual_discretionary, actual_savings],
    }

def create_financial_data (
        vital_expenses_data, non_vital_expenses_data, goal_description, income, saving_target, saving, saving_timeline 
        ):
    engine = SavingsGoalTracker()

    finance_data = {}

    finance_data['vital_expenses'] = vital_expenses_data
    finance_data['non_vital_expenses'] = non_vital_expenses_data
    finance_data['goal_description'] = goal_description
    finance_data['income'] = income 
    finance_data['saving_target'] = saving_target
    finance_data['saving'] = saving
    finance_data['saving_timeline'] = saving_timeline

    engine.declare(Finances(**finance_data))

    return finance_data

def main(
        vital_expenses_data, non_vital_expenses_data, goal_description, income, saving_target, saving, saving_timeline 
    ):

    finance_data = create_financial_data(
        vital_expenses_data, non_vital_expenses_data, goal_description, income, saving_target, saving, saving_timeline 
    )
    # Initialize the expert system
    engine = SavingsGoalTracker()
    engine.reset()


    # Tests
    # User-defined inputs
    # income = 2500  # Monthly salary
    # current_savings = 100  # Current savings
    # target_savings = 3000  # Savings target
    # goal_timeline = 18  # Months (December 2024 to June 2025)

    # Expenses
    # vital_expenses_data = {
    #     "rent": 800,
    #     "groceries": 300,
    #     "transportation": 100,
    #     "pet_expenses": 100,
    # }
    # non_vital_expenses_data = {
    #     "leisures": 250,
    # }

    # Calculating total expenses
    total_expenses = sum(finance_data["vital_expenses"].values()) + sum(finance_data["non_vital_expenses"].values())

    # Declare facts for the expert system
    engine.declare(Fact(monthly_income=income))
    engine.declare(Fact(current_savings=saving))
    engine.declare(Fact(target_amount=saving_target))
    engine.declare(Fact(timeline=saving_timeline))
    engine.declare(Fact(monthly_expenses=total_expenses))

    # Run the expert system
    print("Running the Savings Goal Tracker Expert System...\n")
    engine.run()

    # Test the 50-30-20 rule analysis
    # results = apply_50_30_20_rule(income, vital_expenses_data, non_vital_expenses_data)
    # essentials_limit, discretionary_limit, savings_limit = results["recommended"]
    # actual_essentials, actual_discretionary, actual_savings = results["actual"]

    # print("\n--- 50-30-20 Rule Analysis ---")
    # print("Recommended Spending:")
    # print(f"  Essentials: {essentials_limit:.2f} DT")
    # print(f"  Discretionary: {discretionary_limit:.2f} DT")
    # print(f"  Savings: {savings_limit:.2f} DT")
    # print("\nActual Spending:")
    # print(f"  Essentials: {actual_essentials:.2f} DT")
    # print(f"  Discretionary: {actual_discretionary:.2f} DT")
    # print(f"  Current Savings: {actual_savings:.2f} DT")
    for elt in result.keys() :
        if elt == "rule_50_30_20":
            print(result[elt]["recommended"])
            print(result[elt]["actual"])
        else :
            print(result[elt])

if __name__ == "__main__":
    main()
