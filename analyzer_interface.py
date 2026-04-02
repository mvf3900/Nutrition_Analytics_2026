#### 2026/04/02
#### Analyzer Engine
#### - Analysis_PUltimate Split 2
#### - Contains Interface functions


import pandas as pd
from analyzer_engine import NutritionAnalyzer

# INTRO
# - Get, load, and manage data
file_name = "Nutrition_Raw_Data_260329.csv"
df = pd.read_csv(file_name)

# - Convert date dividers
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# - Define Day 0
start_date = pd.to_datetime("2025-12-29")

# - Add column that gives week number
df["Week_Number"] = ((df["Date"] - start_date).dt.days // 7) + 1

# INTERACTIVE CONSOLE
# 1. Initial program
# - Initialize interaction
print("-" * 5 + " NUTRITION ANALYZER " + "-" * 5)

# - Provide date range
# user_start_date = input("Start Date (MM/DD/YYYY): ")
# user_end_date = input("Start Date (MM/DD/YYYY): ")
user_start_date = "01/09/2026"
user_end_date = "03/09/2026"

# - Initialize analyzer
analysis = NutritionAnalyzer(user_start_date, user_end_date, df)

# 2. Interface
# - Provide analyzer options
while True:
    print("--- Analyzer Menu ---")
    print("1. View Average(s)")
    print("2. View Raw Data")
    print("3. Break Dates")
    print("9. Reset Data")
    print("0. Exit")

    # - Receive user selection
    choice = input("Enter an option: ")

    # - Respond to user selection
    if choice == '1':
        # Show averages of datasets
        if hasattr(analysis, 'df_range1') and hasattr(analysis, 'df_range2'):
            # - Send list of broken ranges
            analysis.show_summary([analysis.df_range1, analysis.df_range2])
        else:
            # - Send list of single range
            analysis.show_summary([analysis.df])
    elif choice == '2':
        # Show raw datasets
        if hasattr(analysis, 'df_range1'):
            analysis.show_data([analysis.df_range1, analysis.df_range2])
        else:
            analysis.show_data([analysis.df])
    elif choice == '3':
        # Break dataframe by multiple ranges
        print(f"Current data runs from {analysis.start_str} - {analysis.end_str}")

        # - Receive user date breaks
        range1_end = input("Enter Range-1 End Date (MM/DD/YYYY): ")
        range2_start = input("Enter Range-2 Start Date (MM/DD/YYYY): ")

        # - Send dates for further analysis
        analysis.break_date(range1_end, range2_start)
    elif choice == '9':
        # Reset dataframe to original inputs
        analysis.reset_data()
    elif choice == '0':
        # - Exit analyzer
        print("Exiting Menu...")
        break
    else:
        print("Invalid selection. Try again.")


