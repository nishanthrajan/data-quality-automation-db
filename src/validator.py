import pandas as pd

class DataValidator:
    def __init__(self, source_df, mart_df):
        self.source_df = source_df
        self.mart_df = mart_df

    def validate_aum_calculations(self, tolerance=0.01):
        """Validates AUM = Gross Assets - Fees within tolerance."""
        expected_aum = self.mart_df["gross_assets"] - self.mart_df["fees"]
        discrepancies = self.mart_df[abs(self.mart_df["calculated_aum"] - expected_aum) > tolerance]
        return len(discrepancies) == 0, discrepancies

    def check_completeness(self):
        """Detects missing records per date across layers."""
        self.source_df["fund_id"] = self.source_df["fund_id_raw"].str.replace("EXT_", "", regex=False)
        
        # Check completeness per batch_date
        missing_records = []
        for date, group in self.source_df.groupby("batch_date"):
            source_funds = set(group["fund_id"])
            mart_group = self.mart_df[self.mart_df["batch_date"] == date]
            mart_funds = set(mart_group["fund_id"])
            
            missing = source_funds - mart_funds
            if missing:
                missing_records.extend(list(missing))
                
        return list(set(missing_records))

    def validate_deduplication(self):
        """Checks for row duplicates."""
        initial_len = len(self.mart_df)
        deduped_df = self.mart_df.drop_duplicates()
        return initial_len - len(deduped_df)