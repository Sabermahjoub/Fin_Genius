from experta import *
from datetime import datetime
from dateutil.relativedelta import relativedelta

# -- USER INPUTS --
# We're on the fourth of december
# My salary is : 2500Dt 
# I would like to save 3000Dt (Target amount), Goal description (vacation : going to Japan)
# This goal should be achieved by June 2025
# My current savings are : 100Dt 
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

class Finances(Fact):
    """Fact containing information about the financial situation."""
    pass

class SavingsGoalTracker(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.result = {}

    @Rule(Fact(goal_description=MATCH.goal), Fact(monthly_income=MATCH.income), Fact(monthly_expenses=MATCH.expenses))
    def calculate_savings_rate(self, goal, income, expenses):
        """Calculates the monthly savings rate."""
        savings_rate = max(income - expenses,0)
        self.result["goal_description"]=goal
        self.result["savings_rate"] = (f"Calculated savings rate: {savings_rate}")
        self.declare(Fact(savings_rate=savings_rate))

    @Rule(
        Fact(savings_rate=MATCH.savings_rate),
        Fact(target_amount=MATCH.target),
        Fact(timeline=MATCH.timeline),
        Fact(current_savings=MATCH.savings)
    )
    def feasibility_check(self, savings_rate, target, timeline, savings):
        """Checks if the savings goal is achievable within the timeline."""
        required_rate = target / timeline
        if savings_rate >= required_rate:
            self.declare(Fact(goal_achievable=True))
            self.declare(Fact(goal_achievable_without_saving=True))
            self.declare(Fact(suggest_adjustments=False))
            self.result["feasibility_check"]="Goal is achievable without considering your current savings."
        elif savings >= (target-savings)/timeline:
            self.declare(Fact(goal_achievable=True))
            self.result["feasibility_check"]="Goal is achievable only when considering your current savings."
        else:
            self.declare(Fact(suggest_adjustments=True))
            self.declare(Fact(goal_achievable=False))
            self.result["feasibility_check"]=("Goal is not achievable within the given timeline. Consider budget adjustments.")

    @Rule(Fact(goal_achievable_without_saving=True), 
          Fact(target_amount=MATCH.target), 
          Fact(timeline=MATCH.timeline), 
          Fact(current_savings=MATCH.savings),
          Fact(savings_rate=MATCH.savings_rate))
    def generate_milestones_without_savings(self, target, timeline, savings, savings_rate):
        """Generates monthly milestones without considering the current savings to track progress."""
        monthly_milestone_without_savings =  target / timeline
        monthly_milestone = (target-savings) / timeline
        self.declare(Fact(monthly_milestone=monthly_milestone_without_savings))
        if savings_rate > monthly_milestone:
            self.declare(Fact(savings_exceeds_milestone=True))
        self.result["milestone"]= (f"""To reach your goal, you need to save {monthly_milestone_without_savings:.2f} per month.
            When considering your current savings, you can reach your goal saving only {monthly_milestone:.2f} per month.""")
        
    @Rule(Fact(savings_exceeds_milestone=True))
    def savings_exceeds_milestone(self):
        """Savings exceeds the milestone."""
        self.result["savings_exceeds_milestone"]="You can save more than the required amount."

    @Rule(Fact(goal_achievable=True), Fact(target_amount=MATCH.target), Fact(timeline=MATCH.timeline), Fact(current_savings=MATCH.savings))
    def generate_milestones(self, target, timeline, savings):
        """Generates monthly milestones to track progress."""
        if(savings == target):
            self.result["milestone"]= f"""Your savings match exactly your savings target. No need for further savings. \n"""
        elif(savings > target):
            self.result["milestone"]= f"""You have enough current savings to satisfy your goal. You will save {savings-target:.2f} TND . \n"""
        else:
            monthly_milestone = (target-savings) / timeline
            self.declare(Fact(monthly_milestone=monthly_milestone))
            self.result["milestone"]= (f"To reach your goal, save {monthly_milestone:.2f} per month.")

    # @Rule(Fact(current_savings=MATCH.savings), Fact(monthly_milestone=MATCH.milestone))
    # def track_progress(self, savings, milestone):
    #     """Tracks progress against the savings milestones."""
    #     if savings == milestone :
    #         result["progress"]=("Congratulations! You've achieved your monthly milestone.")
    #     if savings > milestone:
    #         result["progress"]=("Congratulations! You've achieved your monthly milestone.")
    #     else:
    #         result["progress"]=(f"You are behind. You need to save at least {milestone - savings:.2f} more this month.")
    @Rule (Fact(monthly_income=MATCH.income),
          Fact(vital_expenses = MATCH.vital_expenses),
          Fact(non_vital_expenses = MATCH.non_vital_expenses))
    def calculate_rule(self, income, vital_expenses, non_vital_expenses):
        rule_50_30_20 = apply_50_30_20_rule(self.result, income, vital_expenses, non_vital_expenses)
        if rule_50_30_20["actual"][0] > 1.5*rule_50_30_20["recommended"][0]:
            self.declare(Fact(essentials_over=True))
        if rule_50_30_20["actual"][1] < 0.3*rule_50_30_20["recommended"][1]:
            self.declare(Fact(discretionary_under_30=True))
        self.result["rule_50_30_20"] = rule_50_30_20

    @Rule(Fact(suggest_adjustments=True), 
          Fact(savings_rate=MATCH.savings_rate),
          Fact(target_amount=MATCH.target),
          Fact(timeline=MATCH.timeline),
          Fact(non_vital_expenses = MATCH.non_vital_expenses),
          Fact(current_savings=MATCH.savings),
          )
    def suggest_budget_adjustments(self, target, savings, non_vital_expenses, savings_rate, timeline):
        """Suggests budget adjustments to meet savings goals."""
        
        if(savings_rate == 0) :
            self.result["budget_adjustement"]= f"""This saving goal is impossible. Consider being more realistic or maybe steal a bank 😏. \n"""
        else:
            total_needed = target - savings
            monthly_needed = total_needed / timeline
            additional_needed = monthly_needed - savings_rate
            months_needed = (int) (total_needed / savings_rate)
            now = datetime.now()
            result_date = now + relativedelta(months=months_needed)
            formatted_date = result_date.strftime("%Y-%m")  # 'YYYY-MM'

            if sum(non_vital_expenses.values()) > 0 : 
                reduce_disctretionary = "Consider reducing discretionary expenses to increase your savings rate."
            else :
                reduce_disctretionary = ""

            self.result["budget_adjustement_solution_1"] = [monthly_needed, (datetime.now() + relativedelta(months=timeline)).strftime("%Y-%m")]
            self.result["budget_adjustement_solution_2"] = [savings_rate,formatted_date]
            print("First solution  : ", self.result["budget_adjustement_solution_1"])
            print("Second solution  : ", self.result["budget_adjustement_solution_2"])

            self.result["budget_adjustement"]= f"""{reduce_disctretionary} You need to monthly save {monthly_needed:.2f}, but you are only saving {savings_rate:.2f} that means you need to save an additional {additional_needed:.2f} per month.
            Otherwise, your goal will be reached, approximately, in {formatted_date}."""

def verifyExpenseIsMandatory(expense_name):
    return expense_name in vital_expenses

def apply_50_30_20_rule(result,income, vital_expenses, non_vital_expenses):
    """Applies the 50-30-20 rule to classify spending."""
    essentials_limit = 0.5 * income
    discretionary_limit = 0.3 * income
    savings_limit = 0.2 * income

    actual_essentials = sum(vital_expenses.values())
    actual_discretionary = sum(non_vital_expenses.values())
    actual_savings = max(income - (actual_essentials + actual_discretionary) , 0)

    if (actual_savings >= savings_limit):
        if "follow_recommendations_warning" in result.keys():
            del result["follow_recommendations_warning"]
        print("ACTUAL SAVING ", actual_savings)
        print("NOT  SAVING ", savings_limit)
        follow_recommendations_message = "Your actual distribution is better than the one recommended by the 50/30/20 rule, Good job! \n"
        if (actual_discretionary>discretionary_limit):
            follow_recommendations_message += "You can save even more if you limit your discretionary expenses."
        result["follow_recommendations_success"] = follow_recommendations_message
    else :
        if "follow_recommendations_success" in result.keys():
            del result["follow_recommendations_success"]
        result["follow_recommendations_warning"] = "We recommend you to follow the 50/30/20 rule to have more savings."
    
    return {
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
    finance_data['goal_description']=goal_description

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

    # Calculating total expenses
    total_expenses = sum(finance_data["vital_expenses"].values()) + sum(finance_data["non_vital_expenses"].values())

    # Declare facts for the expert system
    engine.declare(Fact(monthly_income=income))
    engine.declare(Fact(current_savings=saving))
    engine.declare(Fact(target_amount=saving_target))
    engine.declare(Fact(timeline=saving_timeline))
    engine.declare(Fact(monthly_expenses=total_expenses))
    engine.declare(Fact(vital_expenses = vital_expenses_data))
    engine.declare(Fact(non_vital_expenses = non_vital_expenses_data))
    engine.declare(Fact(goal_description = goal_description))


    # Run the expert system
    print("Running the Savings Goal Tracker Expert System...\n")
    engine.run()

    print("\nExpert System Output:")
    for elt in engine.result.keys() :
        if elt == "rule_50_30_20":
            print("rule 50_30_20 : [essentials, discretionary, savings]")
            print("recommended = ", engine.result[elt]["recommended"])
            print("actual = ", engine.result[elt]["actual"])
        else :
            print(engine.result[elt])
    return engine.result 


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

    # # User-defined inputs
    # income = 2500  # Monthly salary
    # current_savings = 100  # Current savings
    # target_savings = 3000  # Savings target
    # goal_timeline = 18  # Months 

    # # Expenses
    # vital_expenses_data = {
    #     "rent": 800,
    #     "groceries": 300,
    #     "transportation": 100,
    #     "pet_expenses": 100,
    # }
    # non_vital_expenses_data = {
    #     "leisures": 250,
    # }


if __name__ == "__main__":
    main()
