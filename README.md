# FinGenius 🤖💰

Welcome to FinGenius - Your Expert System-Powered Financial Planning Assistant

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.0%2B-red)
![Experta](https://img.shields.io/badge/experta-1.9.4-green)

## 📌 Table of Contents
- [Overview](#overview)
- [Features](#features)
  - [Savings Goal Tracking](#savings-goal-tracking)
  - [Budget Allocation](#budget-allocation)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

FinGenius is an intelligent financial planning assistant that combines the power of expert systems with a user-friendly interface. Built using Python, Streamlit, and Experta, it helps users make informed financial decisions through advanced rule-based analysis and charts visualizations.

![screenshot](Demo_images/Home.png)

## Features

### Savings Goal Tracking

FinGenius helps you set and achieve your financial goals through intelligent tracking and recommendations.

**Key Features:**
- Custom savings goal creation
- Progress tracking with interactive visualizations
- Smart milestone generation
- Automated feasibility assessments
- Budget adjustment recommendations
- Interactive charts

**Expert System Rules:**
```python
# Rule example: Milestones generation
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
```

### Budget Allocation

Optimize your spending with expert-driven budget recommendations using the 50-30-20 rule.

**Key Features:**
- Smart expense categorization
- Personalized budget breakdowns
- Real-time budget feasibility checks
- Intelligent spending calculus


## Installation

1. Clone the repository:
```bash
git clone https://github.com/Sabermahjoub/Fin_Genius.git
cd fingenius
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run src/main-app.py
```

2. Access the web interface at `http://localhost:8501`

3. Use the sidebar to navigate between features:
   - Advisor (Savings Goal Tracker + Budget Allocator)
   - Charts


## Dependencies

- Python 3.8+
- Streamlit
- Experta
- Pandas
- Plotly
- Python-dateutil

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Made with ❤️ by [Saber & Maha]
