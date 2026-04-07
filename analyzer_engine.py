#### 2026/04/02
#### Analyzer Engine
#### - Analysis_PUltimate Split 1
#### - Contains NutritionAnalyzer

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# Set environment and style for graphs
matplotlib.use('TkAgg')
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "font.size": 10
})


# Create analyzer functions
class NutritionAnalyzer:
    # Initialize dataframe and user dates
    def __init__(self, analyzer_start, analyzer_end, dataframe):
        # Initialize user dates
        self.start = pd.to_datetime(analyzer_start, format='%m/%d/%Y')
        self.end = pd.to_datetime(analyzer_end, format='%m/%d/%Y')

        # - Boundaries kept as string
        self.start_str = self.start.strftime('%m/%d/%Y')
        self.end_str = self.end.strftime('%m/%d/%Y')

        # Initialize dataframe
        # - Include holder for data reset
        # - Include sub range list for multiple datasets
        self.df = dataframe[(dataframe['Date'] >= self.start) & (dataframe['Date'] <= self.end)].copy()
        self.df_holder = self.df.copy()
        self.sub_ranges = []

    # Helper: Get date range string of dataframes
    def _get_date_range_str(self, dataframe):
        if dataframe.empty:
            return "No Data"
        start = dataframe['Date'].iloc[0].strftime('%m/%d/%Y')
        end = dataframe['Date'].iloc[-1].strftime('%m/%d/%Y')
        return f"{start} - {end}"

    # Function: Show summary (averages) of data
    def show_summary(self):
        print("-" * 5 + " SUMMARY " + "-" * 5)

        # - Utilize dataframe(s)
        dfs_to_view = self.sub_ranges if self.sub_ranges else [self.df]

        for i, dataframe in enumerate(dfs_to_view):
            # 1. Identify range
            range_str = self._get_date_range_str(dataframe)
            print(f"Dataset {i + 1}: {range_str}")

            # 2. Calculate and print stats
            stats = dataframe[['Calories', 'Protein', 'Carbohydrate', 'Fat']].mean().round(0).astype(int)
            print(stats.to_string())
            print("-" * 20)
        print("-" * 30)

    # Function: Show raw data
    def show_data(self):
        print("-" * 5 + " DATA " + "-" * 5)

        # - Utilize dataframe(s)
        dfs_to_view = self.sub_ranges if self.sub_ranges else [self.df]

        for i, dataframe in enumerate(dfs_to_view):
            # 1. Identify range
            range_str = self._get_date_range_str(dataframe)
            print(f"Dataset {i + 1}: {range_str}")

            # 2. Print dataframes
            print(dataframe)
            print("-" * 20)
        print("-" * 30)

    # Function: Break data
    def break_date(self, date_list):
        self.sub_ranges = []

        # Check and format user date list
        for date_list_str in date_list:
            try:
                # Split the string by the hyphen
                start_str, end_str = date_list_str.split(" - ")

                # Convert to datetime
                r_start = pd.to_datetime(start_str.strip(), format='%m/%d/%Y')
                r_end = pd.to_datetime(end_str.strip(), format='%m/%d/%Y')

                new_range = self.df[(self.df['Date'] >= r_start) & (self.df['Date'] <= r_end)].copy()

                if not new_range.empty:
                    self.sub_ranges.append(new_range)
                    print(f"Added Range: {self._get_date_range_str(new_range)}")
                else:
                    print(f"Warning: No data found for {date_list_str}")
            except Exception as e:
                print(f"Error parsing '{date_list_str}': {e}. Use format MM/DD/YYYY - MM/DD/YYYY")

        print(f"Total Sub-ranges Created: {len(self.sub_ranges)}")

        # 3. Verification
        print("-" * 5 + " DATA SPLIT COMPLETE " + "-" * 5)
        for i, dataframe in enumerate(self.sub_ranges):
            range_str = self._get_date_range_str(dataframe)
            print(f"Range {i + 1}: {len(dataframe)} days | {range_str}")
        print("-" * 30)

    # Function: Remove outliers
    def remove_outliers(self, nutrition, threshold, direction):
        # 1. State user filtering selections
        print(f"FILTERING: {direction} {threshold} in {nutrition}")

        # 2. Filter main dataframe
        initial_df_len = len(self.df)
        if direction == "Above":
            self.df = self.df[self.df[nutrition] <= threshold].copy()
        else:
            self.df = self.df[self.df[nutrition] >= threshold].copy()

        if not self.sub_ranges:
            excluded = initial_df_len - len(self.df)
            range_str = self._get_date_range_str(self.df)
            print(f"Main Dataset ({range_str}): Removed {excluded} days ({len(self.df)} remaining).")

        # 3. Filter sub-range dataframes
        # - Filter by user selections
        for i in range(len(self.sub_ranges)):
            # - Get initial amount of days
            initial_len = len(self.sub_ranges[i])

            # - Filter selections
            if direction == "Above":
                cleaned = self.sub_ranges[i][self.sub_ranges[i][nutrition] <= threshold].copy()
            else:
                cleaned = self.sub_ranges[i][self.sub_ranges[i][nutrition] >= threshold].copy()

            # - Re-assign cleaned data
            self.sub_ranges[i] = cleaned

            # - Retrieve days removed
            excluded = initial_len - len(cleaned)

            # - Get date string
            range_str = self._get_date_range_str(cleaned)

            # - State filtering product
            print(f"Dataset {i + 1} ({range_str}): Removed {excluded} days ({len(cleaned)} remaining).")

        print("-" * 30)

    # Function: Plot averages
    def plot_averages(self):
        # 1. Identify which data to use
        dfs_to_view = self.sub_ranges if self.sub_ranges else[self.df]
        macro_cats = ['Protein', 'Carbohydrate', 'Fat']

        # 2. Setup figure, internal values, and initial aes
        # - Internal values
        bar_width = 0.15
        center_offset = ((len(dfs_to_view) - 1) * bar_width) / 2
        current_cal_max = 0
        current_macro_max = 0

        # - Initial aes
        cmap = plt.get_cmap('GnBu')
        colors = [cmap(i) for i in [0.4, 0.6, 0.8, 0.9]]

        # - Figure
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax2 = ax1.twinx()

        # 3. Calculate and plot
        for i, dataframe in enumerate(dfs_to_view):
            if dataframe.empty:
                continue

            # - Get date ranges and color dataframes
            range_label = self._get_date_range_str(dataframe)
            color = colors[i % len(colors)]

            # - Calories plot
            cal_val = dataframe['Calories'].mean()
            ax1.bar(0 + (i * bar_width), cal_val, width=bar_width,
                    label=range_label, color=color, alpha=0.8, edgecolor='black', linewidth=0.5)

            # - Macros plot
            macro_vals = dataframe[macro_cats].mean()
            x_macros = [1.5 + j + (i * bar_width) for j in range(len(macro_cats))]
            ax2.bar(x_macros, macro_vals, width=bar_width,
                    color=color, alpha=0.7, edgecolor='black', linewidth=0.5)

            # - Track max Y-lim
            current_cal_max = max(current_cal_max, cal_val)
            current_macro_max = max(current_macro_max, macro_vals.max())
        # 4. Style plot
        # - Divider
        plt.axvline(x=0.75, color='black', linestyle='-', linewidth=1.5)
        # - Calories plot
        ax1.set_ylabel("CALORIES (kcal)", weight='bold')
        ax1.set_ylim(0, current_cal_max.max() * 1.3)
        # - Macros plot
        ax2.set_ylabel("MACROS (grams)", weight='bold', color='dimgray')
        ax2.set_ylim(0, current_macro_max * 1.1)
        # - Global Format
        tick_positions = [
            0 + center_offset,  # Calories center
            1.5 + center_offset,  # Protein center
            2.5 + center_offset,  # Carbs center
            3.5 + center_offset  # Fat center
        ]
        ax1.set_xticks(tick_positions)
        ax1.set_xticklabels(['CALORIES', 'PROTEIN', 'CARB', 'FAT'], weight='bold')

        plt.title('NUTRITION COMPOSITION | CALORIES & MACROS', loc='left',
                  fontsize=14, weight='bold', pad=20)

        # - Grid and Cleanup
        ax1.grid(axis='y', linestyle=':', alpha=0.3)
        ax1.legend(loc='upper left', frameon=True, fontsize='small', title="Date Ranges")
        plt.tight_layout()

        # 5. Print figure
        plt.show(block=False)
        plt.pause(0.1)
        plt.gcf().canvas.draw_idle()
        plt.gcf().canvas.flush_events()

    # Function: Plot lines
    def plot_lines(self, nutrition):
        # 1. Identify which data to use
        dfs_to_view = self.sub_ranges if self.sub_ranges else [self.df]

        # 2. Setup Figure
        plt.figure(figsize=(12, 6))

        # - Aesthetics (Matching your bar chart style)
        cmap = plt.get_cmap('GnBu')
        colors = [cmap(i) for i in [0.5, 0.7, 0.9]]

        # 3. Plot each dataset
        for i, dataframe in enumerate(dfs_to_view):
            if dataframe.empty:
                continue

            # 3.1. Get dataframe variables
            # - Set data range label and color
            range_label = self._get_date_range_str(dataframe)
            color = colors[i % len(colors)]

            # - Sort and save by date
            plot_df = dataframe.sort_values('Date').copy()

            # - Calculate averages
            avg_val = plot_df[nutrition].mean()

            # 3.2. Plot day data
            # - Plot the line with markers
            plt.plot(plot_df['Date'], plot_df[nutrition],
                     label=range_label, color=color,
                     marker='o', markersize=4, linewidth=2, alpha=0.9)

            # 3.3. Plot Averages
            # - Plot averages
            plt.hlines(y=avg_val, xmin=plot_df['Date'].min(), xmax=plot_df['Date'].max(),
                       color=color, linestyle='--', linewidth=2, alpha=0.5)

            # - Display averages in legend
            plt.plot([], [], color=color, linestyle='--', linewidth=2,
                     label=f'   → Avg: {avg_val:.1f}')

        # 4. Global Styling
        plt.title(f'NUTRITION TREND | {nutrition.upper()}', loc='left',
                  fontsize=14, weight='bold', pad=20)
        plt.ylabel(f"{nutrition.upper()} {'(kcal)' if nutrition == 'Calories' else '(grams)'}",
                   weight='bold')
        plt.xlabel("DATE", weight='bold')

        # - Maintenance Goal Line (The 1700 kcal / 120g Protein "Beacon")
        # You can add logic here to draw a horizontal line for your current goals

        plt.grid(True, linestyle=':', alpha=0.5)
        plt.legend(loc='best', frameon=True, fontsize='small')
        plt.tight_layout()

        # 5. Non-blocking display (Matches your plot_averages style)
        plt.show(block=False)
        plt.pause(0.1)

    # Function: Reset data
    def reset_data(self):
        # 1. Retrieve original dataset
        self.df = self.df_holder.copy()
        self.sub_ranges = []

        # 3. Retrieve and print range
        range_str = self._get_date_range_str(self.df)

        print("-" * 5 + " DATA RESET " + "-" * 5)
        print(f"Dataset restored to original scope: {range_str}")
        print("-" * 30)
