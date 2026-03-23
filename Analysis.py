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
