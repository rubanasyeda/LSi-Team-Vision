import pandas as pd
import glob
from datetime import datetime

#Path to Toronto Data
toronto_path = ["../dataset/toronto-occupancy*.csv", 
                "../dataset/toronto-weather*.csv", 
                "../dataset/toronto-inflation*.csv", 
                "../dataset/toronto-unemployment*.csv"]



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

def combine_occupancy_data():
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

def load_csv_to_pandas(file_path):
    try:
        # Load CSV file into a pandas data_23Frame
        df = pd.read_csv(file_path, header=0, low_memory=False, encoding='unicode_escape')
        print("Number of rows in the dataFrame:", file_path, len(df))
        return df
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None
    
def loadData(output_data, weather_data, inflation, unemployment, cpi=""):

    #-------Output Data-------#
    #Loading up the links to the output dataset
    for i in range(len(output_data)):
        output_data[i] = load_csv_to_pandas(output_data[i])

    #Dropping irrelevant columns for output datasets
    for i in range(len(output_data)):
        output_data[i] = output_data[i].drop(columns = ['_id', 'ORGANIZATION_ID', 'SHELTER_ID', 'LOCATION_ID', 'LOCATION_CITY', 'LOCATION_PROVINCE', 'PROGRAM_NAME', 'SECTOR', 'PROGRAM_MODEL','OVERNIGHT_SERVICE_TYPE', 'PROGRAM_AREA', 'SERVICE_USER_COUNT', 'CAPACITY_FUNDING_BED', 'UNOCCUPIED_BEDS', 'UNAVAILABLE_BEDS', 'CAPACITY_FUNDING_ROOM', 'UNOCCUPIED_ROOMS', 'UNAVAILABLE_ROOMS'])
        output_data[i]['OCCUPANCY_DATE'] = output_data[i]['OCCUPANCY_DATE'].astype(str).apply(clean_and_standardize_date)
        output_data[i]['OCCUPANCY_DATE'] =  pd.to_datetime(output_data[i]['OCCUPANCY_DATE'])

    #Joining the Output data together
    big_data = output_data[0]
    for i in range(1,len(output_data)):
        big_data = pd.concat([big_data, output_data[i]], ignore_index = True)

    #Determine the max and min date in the dataset to create a date vector to fill out empty values
    max_date = big_data['OCCUPANCY_DATE'].max()
    min_date = big_data['OCCUPANCY_DATE'].min()
    date_range = pd.date_range(start=min_date, end=max_date, freq = 'D')
    date_df = pd.DataFrame({'OCCUPANCY_DATE': date_range})

    #-------Weather Data-------#

    #loading up the links to the weather dataset
    for i in range(len(weather_data)):
        weather_data[i] = load_csv_to_pandas(weather_data[i])

    #Dropping irrelevant columns for weather datasets
    for i in range(len(weather_data)):
        weather_data[i] = weather_data[i].drop(columns = ['ï»¿"Longitude (x)"', 'Latitude (y)', 'Station Name', 'Climate ID', 'Year', 'Month', 'Day', 'Data Quality', 'Max Temp Flag', 'Min Temp Flag', 'Mean Temp Flag', 'Heat Deg Days Flag', 'Cool Deg Days Flag', 'Total Rain (mm)', 'Total Rain Flag', 'Total Snow (cm)', 'Total Snow Flag', 'Total Precip Flag',
        'Snow on Grnd Flag', 'Dir of Max Gust (10s deg)', 'Dir of Max Gust Flag', 'Spd of Max Gust (km/h)', 'Spd of Max Gust Flag'])
        weather_data[i]['Date/Time'] = weather_data[i]['Date/Time'].astype(str)
        weather_data[i]['Date/Time'] = pd.to_datetime(weather_data[i]['Date/Time'])

    #Joining the Weather data together
    big_weather = weather_data[0]
    for i in range(1, len(weather_data)):
        big_weather = pd.concat([big_weather, weather_data[i]], ignore_index = True)

    #Cut down all data with dates that is bigger than the biggest date and smaller than the smallest date with an output
    big_weather = big_weather[big_weather['Date/Time'] <= max_date]
    big_weather = big_weather[big_weather['Date/Time'] >= min_date]

    #Fill out datasets' entries w no data w 0
    big_weather = big_weather.fillna(0)

    #Changing non output dataset's date column to 'OCCUPANCY_DATE'
    big_weather = big_weather.rename(columns = {'Date/Time': 'OCCUPANCY_DATE'})

    # #-------Inflation Data-------#

    # #loading up housing data
    inflation = load_csv_to_pandas(inflation)

    #Dropping irrelevant columns for housing dataset
    inflation = inflation.rename(columns = {inflation.columns[0]: 'OCCUPANCY_DATE'})
    inflation = inflation.rename(columns = {inflation.columns[1]: 'Inflation_Rate_Change'})
    inflation["OCCUPANCY_DATE"] = pd.to_datetime(inflation["OCCUPANCY_DATE"])
    inflation = inflation[inflation["OCCUPANCY_DATE"] >= min_date]
    inflation = inflation[inflation["OCCUPANCY_DATE"] <= max_date].reset_index(drop=True)
    inflation = pd.merge(inflation, date_df, on = 'OCCUPANCY_DATE', how = 'outer')
    inflation = inflation.sort_values(by='OCCUPANCY_DATE').reset_index(drop=True)
    inflation = inflation.ffill()
    #-------Unemployment Data-------#
    
    #Loading the unemployment dataset
    unemployment = load_csv_to_pandas(unemployment)
    
    #Analyize Data
    unemployment = unemployment.drop(columns = ['Labour force 7', 'Employment 8', 'Unemployment 9'])

    unemployment = unemployment.rename(columns = {'ï»¿Date': 'OCCUPANCY_DATE'})

    unemployment = unemployment.rename(columns = {"Population 6": 'Population'})
    unemployment['Population'] = unemployment['Population'].str.replace(',', '', regex=False).astype(float)*1000
    unemployment = unemployment.rename(columns = {"Unemployment Rate 10": 'Unemployment_Rate'})
    unemployment = unemployment.rename(columns = {"Participation Rate 11": 'Employment_Participation_Rate'})
    unemployment = unemployment.rename(columns = {"Employment Rate 12": 'Employment_Rate'})

    unemployment['OCCUPANCY_DATE'] = pd.to_datetime(unemployment['OCCUPANCY_DATE'], format="%y-%b", errors='coerce').dt.strftime("%Y-%m")

    unemployment = unemployment[unemployment["OCCUPANCY_DATE"] >= pd.to_datetime(min_date).strftime('%Y-%m')]
    unemployment = unemployment[unemployment["OCCUPANCY_DATE"] >= pd.to_datetime(max_date).strftime('%Y-%m')]
    unemployment = pd.merge(date_df, unemployment, on='OCCUPANCY_DATE', how='left')
    
    # #-------Final Data Prep-------#

    # #Merge the datasets together through date
    big_data = pd.merge(big_data, big_weather, on = 'OCCUPANCY_DATE', how = 'inner')
    big_data = pd.merge(big_data, inflation, on = 'OCCUPANCY_DATE', how = 'inner')
    big_data = pd.merge(big_data, unemployment, on = 'OCCUPANCY_DATE', how = 'inner')

    big_data = big_data.sort_values(by='OCCUPANCY_DATE')

    #Placing the bed and room occupancy column last
    room_occupancy = big_data.pop('OCCUPANCY_RATE_ROOMS')
    bed_occupancy = big_data.pop('OCCUPANCY_RATE_BEDS')
    big_data['OCCUPANCY_RATE_BEDS'] = bed_occupancy
    big_data['OCCUPANCY_RATE_ROOMS'] = room_occupancy

    grouped_data = big_data.groupby('PROGRAM_ID')
    shelter_data_frames = {}
    for shelter_id, shelter_group in grouped_data:
        shelter_data_frames[shelter_id] = shelter_group
        shelter_data_frames[shelter_id]['OCCUPANCY_DATE'] = pd.to_datetime(shelter_data_frames[shelter_id]['OCCUPANCY_DATE'])

    big_data.reset_index(inplace=True)
    big_data = big_data.drop(columns = ['index'])

    big_data.to_csv("all_data.csv", index=True)
    return big_data, shelter_data_frames


if __name__ == "__main__":
    shelter = glob.glob(toronto_path[0])
    weather = glob.glob(toronto_path[1])
    inflation = glob.glob(toronto_path[2])
    umemployment = glob.glob(toronto_path[3])
    # print(shelter)
    # print(weather)
    # print(inflation)
    # print(umemployment)

    data, df = loadData(shelter, weather, inflation[0], umemployment[0])

    print(data.columns)
    print(data.head())