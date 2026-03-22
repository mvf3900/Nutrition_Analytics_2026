#### Nutrition Data Analysis from Jan 1 2026
import pandas as pd

# Since the file is in the SAME folder as this script,
# we don't need the whole "C:\Users\..." path!
file_name = "Nutrition_Raw_Data_260322.csv"

# Load the data
df = pd.read_csv(file_name)

# Let's see the first 3 days of your 2026 journey
print("--- January 1st Start ---")
print(df.head(3))

# Calculate your average calories so far
avg_cals = df['Calories'].mean()
print(f"\nAverage Daily Intake: {avg_cals:.0f} kcal")