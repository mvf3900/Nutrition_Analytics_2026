#### 2026/04/08
#### Analyzer Engine - Version 2
#### - Contains Interface functions


import pandas as pd
from analyzer_engine_2 import NutritionAnalyzer

# INTRO
# - Get, load, and manage data
file_name = "data/Nutrition_Raw_Data_260503.csv"
df = pd.read_csv(file_name)

# - Convert date dividers
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# - Define Range Ends
start_date = pd.to_datetime(df['Date'].iloc[0])
end_date = pd.to_datetime(df['Date'].iloc[-1])

# - Add column that gives week number and month
df["Week_Number"] = ((df["Date"] - start_date).dt.days // 7) + 1
df["Month"] = df['Date'].dt.to_period('M')

# - Map choices for nutrition
# - Map choices for direction
nutrition_map = {'1': 'Calories',
                 '2': 'Protein',
                 '3': 'Carbohydrate',
                 '4': "Fat"}
direction_map = {'1': 'Above',
                 '2': 'Below'}


# DATE FUNCTIONS
# Function: Format Date
def date_formatter(user_date):
    if len(user_date) == 10:
        return user_date
    elif len(user_date) == 6:
        formatted_date = f"{user_date[:2]}/{user_date[2:4]}/20{user_date[4:]}"
        return formatted_date
    else:
        return None


# Function: Validate Date
def validate_date(prompt, s_range=start_date, e_range=end_date):
    while True:
        raw_input = input(prompt)
        formatted = date_formatter(raw_input)

        # Check Format
        if formatted is not None:
            check_date = pd.to_datetime(formatted, format='%m/%d/%Y')

            # Check Range
            if s_range <= check_date <= e_range:
                # Break loop for successful check
                return formatted
            else:
                # Error messages
                print(f"Error: Date {formatted} is out of range.")
                print(f"*** CSV Range: {s_range.strftime('%m/%d/%Y')} - {e_range.strftime('%m/%d/%Y')}.")
        else:
            print("Error: Input must be MMDDYY or MM/DD/YYYY. Try again.")


# INTERACTIVE CONSOLE
# 1. Initial program
# - Initialize interaction
print("-" * 5 + " NUTRITION ANALYZER " + "-" * 5)

# - Provide date range
user_start_date = validate_date("Start Date (MM/DD/YYYY): ")
user_end_date = validate_date("End Date (MM/DD/YYYY): ")
#user_start_date = "12/29/2025"
#user_end_date = "04/05/2026"

# - Initialize analyzer
analysis = NutritionAnalyzer(user_start_date, user_end_date, df)

# 2. Interface
# - Provide analyzer options
while True:
    print("--- ANALYZER MENU ---")
    print("1. View Average(s)")
    print("2. View Raw Data")
    print("3. Break Dates")
    print("4. Remove Outliers")
    print("5. Plot Averages (Bar)")
    print("6. Plot Data (Line)")
    print("9. Reset Data")
    print("0. Exit")

    # - Receive user selection
    choice = input("Enter an option: ")

    # 3. Respond to user selection
    if choice == '1':
        # Shows averages of ranges
        analysis.show_summary()
    elif choice == '2':
        # Shows data of ranges
        analysis.show_data()
    elif choice == '3':
        # Break dataframe by multiple ranges
        print(f"Input data runs from {analysis.start_str} - {analysis.end_str}")

        # - Receive user split option and initialize split list
        breaker_choice = input("Enter split option:"
                               "\n1. Manual"
                               "\n2. Months"
                               "\n3. Weeks\n")
        split_dates = []
        # - 1. Manual split
        if breaker_choice == '1':
            break_range_tracker = 1
            while True:
                # - Receive user date ranges
                raw_start = input(f'Press enter to continue or (1) for done: ')
                if raw_start == '1':
                    break

                break_start = validate_date(f"Enter Range {break_range_tracker} Start: ")
                break_end = validate_date(f"Enter Range {break_range_tracker} End: ")

                if break_start and break_end:
                    split_dates.append(f"{break_start} - {break_end}")
                    break_range_tracker += 1
                else:
                    print("Invalid range dates. Try again.")
        # - 2. Split by Months
        elif breaker_choice == '2':
            unique_months = analysis.df['Month'].unique()
            for period in unique_months:
                month_data = analysis.df[analysis.df['Month'] == period]
                start = month_data['Date'].min().strftime('%m/%d/%Y')
                end = month_data['Date'].max().strftime('%m/%d/%Y')
                split_dates.append(f"{start} - {end}")
        # - 3. Split by Weeks
        elif breaker_choice == '3':
            unique_weeks = analysis.df['Week_Number'].unique()
            for period in unique_weeks:
                week_data = analysis.df[analysis.df['Week_Number'] == period]
                start = week_data['Date'].min().strftime('%m/%d/%Y')
                end = week_data['Date'].max().strftime('%m/%d/%Y')
                split_dates.append(f"{start} - {end}")
        else:
            print("Invalid selection. Aborting breaker.")
        # - Send dates for further analysis
        analysis.break_date(split_dates)
    elif choice == '4':
        # Remove nutrition outliers
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
    elif choice == '5':
        analysis.plot_averages()
    elif choice == '6':
        # Nutrition selection
        # - Receive nutrition and outlier amount
        n_choice = input("Enter nutrition selection: "
                         "\n1. Calories"
                         "\n2. Protein"
                         "\n3. Carbohydrate"
                         "\n4. Fat\n")
        if n_choice in nutrition_map:
            # Passing the string 'Calories', 'Protein', etc.
            analysis.plot_lines(nutrition_map[n_choice])
        else:
            print("Invalid selection. Returning to menu.")
    elif choice == '9':
        # Reset dataframe to original inputs
        analysis.reset_data()
    elif choice == '0':
        # - Exit analyzer
        print("Exiting Menu...")
        break
    else:
        print("Invalid selection. Try again.")
