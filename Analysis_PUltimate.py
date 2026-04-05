#### Penultimate week (3/29/26)
#### - Add penultimate data
#### - Am I able to remake & enhance original script?

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

# INTRO
# - Get and load data
file_name = "data/Nutrition_Raw_Data_260329.csv"
df = pd.read_csv(file_name)

df.head(5)
df.tail(5)

# DATA MANAGEMENT 1
# - Convert date dividers
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# - Define Day 0
start_date = pd.to_datetime("2025-12-29")

# - Add column that gives week number
df["Week_Number"] = ((df["Date"] - start_date).dt.days // 7) + 1

# DATA MANAGEMENT 2
# - Define Nutrition categories
nutrition_categories = ["Calories", "Protein", "Carbohydrate", "Fat"]

# - Group by week and get averages
# -- reset_index() to place week_number back with columns and drop side index
# -- round() and astype(int) condensed for this script
weekly_avg = df.groupby("Week_Number")[nutrition_categories].mean().round(0).astype(int).reset_index()

# - Save data to CSV
# -- index=False prevents index noise in CSV
# weekly_avg.to_csv("weekly_nutrition_summary_PUltimate.csv", index=False)

# VISUALIZATION 1
# - 1. Set Global Style
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 10
})

# - 2. Setup Figure and Axes
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

# - 3. Plot Calories (Primary Axis)
ax1.plot(weekly_avg["Week_Number"], weekly_avg["Calories"],
         label="Calories", color="black", linewidth=2, marker='o')
ax1.set_ylabel("CALORIES (kcal)", weight='bold')
ax1.set_xlabel("WEEK NUMBER", weight='bold')

# 4. Plot Macros (Secondary Axis)
macro_colors = {"Protein": "tab:blue", "Carbohydrate": "tab:green", "Fat": "tab:red"}
for macro in ["Protein", "Carbohydrate", "Fat"]:
    ax2.plot(weekly_avg["Week_Number"], weekly_avg[macro],
             label=macro, color=macro_colors[macro], alpha=0.6, linestyle="-")

ax2.set_ylabel("MACROS (g)", color="tab:gray", weight='bold')

# - 5. Clean Up Limits & Ticks
# -- Scale X-ticks
ax1.set_xticks(weekly_avg["Week_Number"])

# -- Scale Y-ticks
ax1.set_ylim(weekly_avg['Calories'].min() * 0.9,
             weekly_avg['Calories'].max() * 1.1)
ax2.set_ylim(weekly_avg[['Protein', 'Carbohydrate', 'Fat']].values.min() * 0.9,
             weekly_avg[['Protein', 'Carbohydrate', 'Fat']].values.max() * 1.1)

# - 6. Title & Legend
# -- Title
plt.title('WEEKLY NUTRITION TRENDS', loc='left', fontsize=14, weight='bold', pad=20)

# -- Legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc="upper left", frameon=True)

# - 7. Finalize plot
ax1.grid(axis="x", linestyle=":", alpha=0.6)
fig.tight_layout()

# - 8. Save plot
# plt.savefig("nutrition_trends_W13.png", dpi=300, bbox_inches='tight')
# plt.close()

# - 9. Show plot instead of save
# plt.show()


# NUTRITION ANALYZER
# - Analyze by user start and end date
class NutritionAnalyzer:
    # Initialize user dataframe
    def __init__(self, analyzer_start, analyzer_end):
        # 1. Load original dataframe
        analyzer_df = df.copy()

        # 2. Set user boundaries
        self.start = pd.to_datetime(analyzer_start, format='%m/%d/%Y')
        self.end = pd.to_datetime(analyzer_end, format='%m/%d/%Y')
        # - Boundaries kept as string
        self.start_str = self.start.strftime('%m/%d/%Y')
        self.end_str = self.end.strftime('%m/%d/%Y')

        # 3. Create the "Scoped" Dataframe
        self.df = analyzer_df[(analyzer_df['Date'] >= self.start) & (analyzer_df['Date'] <= self.end)].copy()
        self.df_holder = self.df.copy()

        # 4. Check initializer
        print(f"Project Initialized: {len(self.df)} days loaded from {self.start_str} to {self.end_str}.\n")

    # Function to view averages
    def show_summary(self, dfs_to_view):
        print("--- SUMMARY ---")
        for i, dataframe in enumerate(dfs_to_view):
            # 1. Identify Range
            start_date = dataframe['Date'].iloc[0].strftime('%m/%d/%Y')
            end_date = dataframe['Date'].iloc[-1].strftime('%m/%d/%Y')

            print(f"Range {i + 1}: {start_date} to {end_date}")

            # 2. Calculate and Print Stats
            stats = dataframe[['Calories', 'Protein', 'Carbohydrate', 'Fat']].mean().round(0).astype(int)
            print(stats)
            print("-" * 15)
        print("-" * 30)

    # Function to view data
    def show_data(self, dfs_to_view):
        print("--- DATA ---")
        for i, dataframe in enumerate(dfs_to_view):
            start_date = dataframe['Date'].iloc[0].strftime('%m/%d/%Y')
            end_date = dataframe['Date'].iloc[-1].strftime('%m/%d/%Y')

            print(f"Dataset {i + 1} ({start_date} - {end_date}):")
            print(dataframe)
            print("-" * 20)
        print("-" * 30)

    # Function to break data
    def break_date(self, r1_end, r2_start):
        # 1. Convert inputs to datetime objects
        r1_end_dt = pd.to_datetime(r1_end, format='%m/%d/%Y')
        r2_start_dt = pd.to_datetime(r2_start, format='%m/%d/%Y')

        # 2. Slice the main dataframe into two segments
        # - Range 1:  Original start to new split point
        self.df_range1 = self.df[self.df['Date'] <= r1_end_dt].copy()
        # -- String Range 1
        self.df_range1_start_str = self.df_range1['Date'].iloc[0].strftime('%m/%d/%Y')
        self.df_range1_end_str = self.df_range1['Date'].iloc[-1].strftime('%m/%d/%Y')

        # - Range 2: New second start point to original end
        self.df_range2 = self.df[self.df['Date'] >= r2_start_dt].copy()
        # -- String Range 2
        self.df_range2_start_str = self.df_range2['Date'].iloc[0].strftime('%m/%d/%Y')
        self.df_range2_end_str = self.df_range2['Date'].iloc[-1].strftime('%m/%d/%Y')

        # 3. Verification
        print(f"\n--- DATA SPLIT COMPLETE ---")
        print(f"Range 1: {len(self.df_range1)} days ("
              f"{self.df_range1_start_str} - {self.df_range1_end_str})")
        print(f"Range 2: {len(self.df_range2)} days ("
              f"{self.df_range2_start_str} - {self.df_range2_end_str})")
        print("-" * 30 + "\n")

    # Function to reset data
    def reset_data(self):
        self.df = self.df_holder.copy()

        # Clean up the broken ranges so Choice 1 goes back to 'Single View'
        if hasattr(self, 'df_range1'):
            del self.df_range1
            del self.df_range2

        original_start = self.df['Date'].iloc[0].strftime('%m/%d/%Y')
        original_end = self.df['Date'].iloc[-1].strftime('%m/%d/%Y')

        print("\n--- DATA RESET ---")
        print(f"Dataframe restored to original scope: {original_start} - {original_end}")
        print("-" * 30 + "\n")





# INTERACTIVE CONSOLE
# - Start interaction
print("--- Nutrition Analyzer ---")
analyzer_starter = input("Would you like to analyze a timeframe? (y/n): ").lower()

if analyzer_starter == 'y':
    # 1. Receive dates for analysis
    #start = input("Start Date (MM/DD/YYYY): ")
    #end = input("End Date (MM/DD/YYYY): ")
    start = "01/09/2026"
    end = "03/09/2026"

    # - Initialize analyzer
    analysis = NutritionAnalyzer(start, end)

    # 2. Provide analyzer options
    while True:
        print("--- Analyzer Menu ---")
        print("1. View Average(s)")
        print("2. View Raw Data")
        print("3. Break Dates")
        print("9. Reset Data")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            if choice == '1':
                # 1. Check if the broken ranges actually exist in the class yet
                if hasattr(analysis, 'df_range1') and hasattr(analysis, 'df_range2'):
                    # Send the list of broken ranges
                    analysis.show_summary([analysis.df_range1, analysis.df_range2])
                else:
                    # Send the single main dataframe in a list
                    analysis.show_summary([analysis.df])
        elif choice == '2':
            if hasattr(analysis, 'df_range1'):
                analysis.show_data([analysis.df_range1, analysis.df_range2])
            else:
                analysis.show_data([analysis.df])
        elif choice == '3':
            print(f"Current data runs from {analysis.start_str} - {analysis.end_str}")
            range1_end = input("Enter Range-1 End Date (MM/DD/YYYY): ")
            range2_start = input("Enter Range-2 Start Date (MM/DD/YYYY): ")
            analysis.break_date(range1_end, range2_start)
        elif choice == '9':
            analysis.reset_data()
        elif choice == '0':
            print("Exiting Menu...")
            break
        else:
            print("Invalid selection. Try again.")

else:
    print("Session Terminated.")

