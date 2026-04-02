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
        # - Also include holder for data reset
        self.df = dataframe[(dataframe['Date'] >= self.start) & (dataframe['Date'] <= self.end)].copy()
        self.df_holder = self.df.copy()

    # Helper: Get date range string of dataframes
    def _get_date_range_str(self, dataframe):
        start = dataframe['Date'].iloc[0].strftime('%m/%d/%Y')
        end = dataframe['Date'].iloc[-1].strftime('%m/%d/%Y')
        return f"{start} - {end}"

    # Function: Show summary (averages) of data
    def show_summary(self, dfs_to_view):
        print("-" * 5 + " SUMMARY " + "-" * 5)
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
    def show_data(self, dfs_to_view):
        print("-" * 5 + " DATA " + "-" * 5)
        for i, dataframe in enumerate(dfs_to_view):
            # 1. Identify range
            range_str = self._get_date_range_str(dataframe)
            print(f"Dataset {i + 1}: {range_str}")

            # 2. Print dataframes
            print(dataframe)
            print("-" * 20)
        print("-" * 30)

    # Function: Break data
    def break_date(self, r1_end, r2_start):
        # 1. Convert inputs to datetime objects
        r1_end_dt = pd.to_datetime(r1_end, format='%m/%d/%Y')
        r2_start_dt = pd.to_datetime(r2_start, format='%m/%d/%Y')

        # 2. Slice the main dataframe into two segments
        # - Range 1:  Original start to new split point
        self.df_range1 = self.df[self.df['Date'] <= r1_end_dt].copy()
        # -- String Range 1
        range1_str = self._get_date_range_str(self.df_range1)

        # - Range 2: New second start point to original end
        self.df_range2 = self.df[self.df['Date'] >= r2_start_dt].copy()
        # -- String Range 2
        range2_str = self._get_date_range_str(self.df_range2)

        # 3. Verification
        print("-" * 5 + " DATA SPLIT COMPLETE " + "-" * 5)
        print(f"Range 1: {len(self.df_range1)} days | {range1_str}")
        print(f"Range 2: {len(self.df_range2)} days | {range2_str}")
        print("-" * 30)

    # Function: Reset data
    def reset_data(self):
        # 1. Retrieve original dataset
        self.df = self.df_holder.copy()

        # 2. Clean up the broken ranges
        if hasattr(self, 'df_range1'):
            del self.df_range1
            del self.df_range2

        # 3. Retrieve and print range
        range_str = self._get_date_range_str(self.df)

        print("-" * 5 + " DATA RESET " + "-" * 5)
        print(f"Dataset restored to original scope: {range_str}")
        print("-" * 30)
