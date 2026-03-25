#### Nutrition Data Analysis from Jan 1 2026

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

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


# Data play 1
# - Convert Date to type datetime
df['Date'] = pd.to_datetime(df['Date'])

# - Get month name from Date
df['Month'] = df['Date'].dt.month_name()

# - Define order of months
month_order = ["January", "February", "March"]
# - Define Nutrition categories
nutrition_categories = ["Calories", "Protein", "Carbohydrate", "Fat"]

# - Group by months and get mean
# -- dt.month() to get month from Date
# -- reset_index() to lift back column headers
monthly_avg = df.groupby('Month')[['Calories', 'Protein', 'Carbohydrate', 'Fat']].mean().reset_index()

# - Order months
monthly_avg['Month'] = pd.Categorical(monthly_avg['Month'], categories=month_order, ordered=True)
monthly_avg = monthly_avg.sort_values('Month').reset_index(drop=True)

# - Round averages to whole number
monthly_avg[nutrition_categories] = monthly_avg[nutrition_categories].round(0).astype(int)

# print(monthly_avg) # Uncomment to see df


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

# print(weekly_avg) # Uncomment to see df


# Data Play 3
# - Generate plot for weekly averages
plt.figure(figsize=(8, 5))
plt.plot(weekly_avg['Week_Number'], weekly_avg['Calories'], marker='o', color='b', linestyle='-')
plt.title('Calories over Time')
plt.xlabel('Week Number')
plt.ylabel('Calories')
plt.grid(True)

# - Show plot
plt.show()


# Data Play 4
# - Generate plot with calories and macros
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]
plt.rcParams["font.size"] = 10
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = "Times New Roman"

# - Title
plt.title('NUTRITION', fontname='Times New Roman', fontsize=16, weight='bold', loc='left', pad=20)

# - Get axis limits
# -- For Calories
cal_min = weekly_avg['Calories'].min() * 0.9
cal_max = weekly_avg['Calories'].max() * 1.1

# -- For Macros
all_macros = weekly_avg[['Protein', 'Carbohydrate', 'Fat']]
macro_min = all_macros.values.min() * 0.9
macro_max = all_macros.values.max() * 1.1

# - Plot Calories
color_cal = 'black'
ax1.set_xlabel("WEEK NUMBER", fontname='Times New Roman', fontsize=12)
ax1.set_ylabel("CALORIES", fontname='Times New Roman', fontsize=12)
ax1.plot(weekly_avg["Week_Number"], weekly_avg["Calories"],
         label="Calories", color=color_cal, linestyle="-", alpha=1)
ax1.tick_params(axis="y", labelcolor=color_cal)
ax1.set_ylim(cal_min, cal_max)
# -- Set X axis ticks
weeks = weekly_avg["Week_Number"]
ax1.set_xticks(weeks)
ax1.set_xticklabels(weeks)

# - Plot Macros
color_mac = 'tab:gray'
ax2.set_ylabel("MACROS", fontname='Times New Roman', fontsize=12)
ax2.plot(weekly_avg["Week_Number"], weekly_avg["Protein"],
         label="Protein", color="tab:blue", linestyle="-", alpha=0.5)
ax2.plot(weekly_avg["Week_Number"], weekly_avg["Carbohydrate"],
         label="Carbohydrate", color="tab:green", linestyle="-", alpha=0.5)
ax2.plot(weekly_avg["Week_Number"], weekly_avg["Fat"],
         label="Fat", color="tab:red", linestyle="-", alpha=0.5)
ax2.tick_params(axis="y", labelcolor=color_mac)
ax2.set_ylim(macro_min, macro_max)

# - Get and set legend info
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

# -- Grid and ticks
ax1.tick_params(axis='both', which='major', labelsize=10)
ax2.tick_params(axis='y', labelsize=10)
ax1.grid(True, axis="x", linestyle=":", alpha=0.6)
ax2.grid(False)
fig.tight_layout()  # Forces label in figure

# - Show Plot
plt.show()
