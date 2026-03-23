#### Nutrition Data Analysis from Jan 1 2026
import pandas as pd

# Intro
# - Get and load data
file_name = "Nutrition_Raw_Data_260322.csv"
df = pd.read_csv(file_name)

# - See the first 3 days
print("--- January 1st Start ---")
print(df.head(3))

# - Calculate average calories so far
avg_cals = df['Calories'].mean()
print(f"\nAverage Daily Calories: {avg_cals:.0f} cal")

# Data play
# - Convert Date to type datetime
df['Date'] = pd.to_datetime(df['Date'])

# - Get month name from Date
df['Month'] = df['Date'].dt.month_name()

# - Define order of months
month_order = ["January", "February", "March"]
# - Define Nutrition categories
nutrition_categories = ["Calories", "Protein", "Carbohydrate", "Fat"]

# - Group by months and get mean
# -- .dt.month to get month from Date
monthly_avg = df.groupby('Month')[['Calories', 'Protein', 'Carbohydrate', 'Fat']].mean().reset_index()

# - Order months
monthly_avg['Month'] = pd.Categorical(monthly_avg['Month'], categories=month_order, ordered=True)
monthly_avg = monthly_avg.sort_values('Month').reset_index(drop=True)

# - Round averages to whole number
monthly_avg[nutrition_categories] = monthly_avg[nutrition_categories].round(0).astype(int)

print(monthly_avg)

# Data Play 2
# - Reload data cause didn't change variable from data play 1
original_df = pd.read_csv(file_name)

# - Add data from December
dec_data = {
    'Date': ['2025-12-29', '2025-12-30', '2025-12-31'],
    'Calories': [2065, 1434, 1684],
    'Protein': [87, 58, 76],
    'Carbohydrate': [239, 137, 230],
    'Fat': [80, 68, 52]
}

# - Turn into dataframe
df_dec = pd.DataFrame(dec_data)

# - Stack December with original dataframe
complete_df = pd.concat([df_dec, original_df], ignore_index=True)

# - Convert Date to datetime
complete_df['Date'] = pd.to_datetime(complete_df['Date'])

# - Define Day 0
start_date = pd.to_datetime("2025-12-29")

# - Add column that gives week number
complete_df["Week_Number"] = ((complete_df["Date"] - start_date).dt.days // 7) + 1

# - Group by week and get averages
# -- reset_index() to place week_number back with columns and drop side index
weekly_avg = complete_df.groupby("Week_Number")[nutrition_categories].mean().reset_index()

# - Round averages to whole number
weekly_avg[nutrition_categories] = weekly_avg[nutrition_categories].round(0).astype(int)

print(weekly_avg)