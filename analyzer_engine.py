#### 2026/04/02
#### Analyzer Engine
#### - Analysis_PUltimate Split 1
#### - Contains NutritionAnalyzer

import pandas as pd


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
