import pandas as pd
import numpy as np

def generate_mock_datasets():
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=10, freq="D")
    funds = ["FUND_A", "FUND_B", "FUND_C", "FUND_D"]

    data = []
    for d in dates:
        for f in funds:
            # Edge case: zero shares/NAV trigger for division scenarios
            is_zero_div_edge = (f == "FUND_C" and d == dates[2])
            shares = 0 if is_zero_div_edge else int(np.random.randint(1000, 50000))
            nav = 0.0 if is_zero_div_edge else float(np.round(np.random.uniform(10.0, 500.0), 2))
            
            data.append({
                "batch_date": d.strftime("%Y-%m-%d"),
                "fund_id_raw": f"EXT_{f}",
                "shares": shares,
                "nav": nav,
                "gross_assets": shares * nav,
                "fees": np.round(shares * nav * 0.001, 2)
            })

    source_df = pd.DataFrame(data)
    
    # Simulate missing fund in final layer for completeness checks
    mart_df = source_df[~((source_df["fund_id_raw"] == "EXT_FUND_D") & (source_df["batch_date"] == dates[-1].strftime("%Y-%m-%d")))].copy()
    
    # ID transformation (strip prefix)
    mart_df["fund_id"] = mart_df["fund_id_raw"].str.replace("EXT_", "", regex=False)
    mart_df["calculated_aum"] = mart_df["gross_assets"] - mart_df["fees"]
    
    # Duplicate row injection
    duplicate_row = mart_df.iloc[[0]].copy()
    mart_df = pd.concat([mart_df, duplicate_row], ignore_index=True)

    return source_df, mart_df

if __name__ == "__main__":
    src, mart = generate_mock_datasets()
    src.to_csv("data/raw_source/source_batch.csv", index=False)
    mart.to_csv("data/intermediate_mart/mart_table.csv", index=False)
    print("Mock datasets generated successfully in data/ directories.")