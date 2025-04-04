import pandas as pd
import glob
from datetime import datetime

def clean_and_standardize_date(date_str):
    try:
        # Case 1: Format like 22-01-01 (YY-MM-DD)
        if len(date_str) == 8 and '-' in date_str:
            return datetime.strptime(date_str, "%y-%m-%d").date()
        
        # Case 2: ISO format with time or standard YYYY-MM-DD
        return pd.to_datetime(date_str).date()
    
    except Exception:
        return pd.NaT 

file_paths = glob.glob("../dataset/*aily*shelter*ove*.csv")  # e.g., shelter_data_2020.csv, ..., 2024.csv

dfs = []

# Extract relevant features
for file in file_paths:
    df = pd.read_csv(file)

    # Keep only relevant columns and rename them
    df_subset = df[[
        # "_id",
        "OCCUPANCY_DATE",
        "ORGANIZATION_NAME",
        "SHELTER_GROUP",
        "LOCATION_ADDRESS",
        "LOCATION_CITY",
        "LOCATION_PROVINCE",
        "LOCATION_POSTAL_CODE",
        "LOCATION_NAME",
        "PROGRAM_NAME",
        "SECTOR",
        "SERVICE_USER_COUNT",
        "CAPACITY_ACTUAL_BED"
    ]].copy()

    # Rename columns for ML dataset features
    df_subset.rename(columns={
        "_id": "RECORD_ID",
        "OCCUPANCY_DATE": "DATE",
        "ORGANIZATION_NAME": "ORGANIZATION",
        "SHELTER_GROUP": "SHELTER",
        "LOCATION_ADDRESS": "ADDRESS",
        "LOCATION_CITY": "CITY",
        "LOCATION_PROVINCE": "PROVINCE",
        "LOCATION_POSTAL_CODE": "POSTAL_CODE",
        "LOCATION_NAME": "FACILITY",
        "PROGRAM_NAME": "PROGRAM",
        "SECTOR": "POPULATION_GROUP",
        "SERVICE_USER_COUNT": "CURRENT_OCCUPANCY",
        "CAPACITY_ACTUAL_BED": "MAX_CAPACITY"
    }, inplace=True)

    df_subset["DATE"] = df_subset["DATE"].astype(str).apply(clean_and_standardize_date)
    dfs.append(df_subset)

# Combine all yearly data
final_df = pd.concat(dfs, ignore_index=True)

# Clean data
final_df = final_df.dropna(subset=["DATE", "CURRENT_OCCUPANCY", "MAX_CAPACITY"])
final_df = final_df[final_df["CURRENT_OCCUPANCY"] >= 0]
final_df = final_df[final_df["MAX_CAPACITY"] > 0]

# Ensure correct types
final_df["DATE"] = final_df["DATE"].astype(str)
final_df["CURRENT_OCCUPANCY"] = final_df["CURRENT_OCCUPANCY"].astype(int)
final_df["MAX_CAPACITY"] = final_df["MAX_CAPACITY"].astype(int)

# Move CURRENT_OCCUPANCY to the end
columns = [col for col in final_df.columns if col != "CURRENT_OCCUPANCY"] + ["CURRENT_OCCUPANCY"]
final_df = final_df[columns]

# Sort by date
final_df = final_df.sort_values("DATE").reset_index(drop=True)

final_df.to_csv("compiled_shelter_dataset.csv", index=True)

print("Dataset compiled and saved as 'compiled_shelter_dataset.csv'")
