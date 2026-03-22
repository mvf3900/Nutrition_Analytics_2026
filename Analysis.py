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

monthly_avg = df.groupby(df['Date'].dt.month)[[
    'Calories', 'Protein', 'Carbohydrate', 'Fat']].mean()
