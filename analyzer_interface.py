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
user_start_date = input("Start Date (MM/DD/YYYY): ")
user_end_date = input("Start Date (MM/DD/YYYY): ")
#user_start_date = "01/09/2026"
#user_end_date = "03/09/2026"

# - Initialize analyzer
analysis = NutritionAnalyzer(user_start_date, user_end_date, df)

# 2. Interface
# - Provide analyzer options
while True:
    print("--- Analyzer Menu ---")
    print("1. View Average(s)")
    print("2. View Raw Data")
    print("3. Break Dates")
    print("4. Remove Outliers")
    print("9. Reset Data")
    print("0. Exit")

    # - Receive user selection
    choice = input("Enter an option: ")

    # - Respond to user selection
    if choice == '1':
        analysis.show_summary()
    elif choice == '2':
        analysis.show_data()
    elif choice == '3':
        # Break dataframe by multiple ranges
        print(f"Current data runs from {analysis.start_str} - {analysis.end_str}")

        # - Receive user date ranges
        split_dates = []
        while True:
            d = input("Enter date range (MM/DD/YYYY - MM/DD/YYYY) or 'done': ")
            if d == 'done':
                break
            split_dates.append(d)

        # - Send dates for further analysis
        analysis.break_date(split_dates)
    elif choice == '4':
        # Remove nutrition outliers
        # - Map choices
        nutrition_map = {'1': 'Calories',
                         '2': 'Protein',
                         '3': 'Carbohydrate',
                         '4': "Fat"}
        direction_map = {'1': 'Above',
                         '2': 'Below'}

        # - Receive nutrition and outlier amount
        n_choice = input("Enter nutrition selection: "
                         "\n1. Calories"
                         "\n2. Protein"
                         "\n3. Carbohydrate"
                         "\n4. Fat\n")
        t_choice = input("Enter threshold amount: ")
        d_choice = input("Enter removal direction: "
                         "\n1. Above"
                         "\n2. Below\n")

        # - Send user selections
        if n_choice in nutrition_map and d_choice in direction_map:
            selected_n = nutrition_map[n_choice]
            selected_d = direction_map[d_choice]
            selected_t = float(t_choice)

            analysis.remove_outliers(selected_n, selected_t, selected_d)
        else:
            print("Invalid selection. Aborting filter.")

    elif choice == '9':
        # Reset dataframe to original inputs
        analysis.reset_data()
    elif choice == '0':
        # - Exit analyzer
        print("Exiting Menu...")
        break
    else:
        print("Invalid selection. Try again.")
