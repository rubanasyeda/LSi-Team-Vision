import csv

import pandas as pd
import glob
from datetime import datetime

#Path to Toronto Data
toronto_path = ["../dataset/toronto-occupancy*.csv", 
                "../dataset/toronto-weather*.csv", 
                "../dataset/toronto-inflation*.csv", 
                "../dataset/toronto-unemployment*.csv",
                "../dataset/toronto-cpi*.csv"]

calgary_path = ["../dataset/calgary-occupancy*.csv", 
                "../dataset/calgary-weather*.csv", 
                "../dataset/calgary-inflation*.csv", 
                "../dataset/calgary-unemployment*.csv",
                "../dataset/calgary-cpi*.csv"]

def clean_and_standardize_date(date_str):
    try:
        # Case 1: Format like 22-01-01 (YY-MM-DD)
        if len(date_str) == 8 and '-' in date_str:
            return datetime.strptime(date_str, "%y-%m-%d").date()
        return pd.to_datetime(date_str).date()
    
    except Exception:
        return pd.NaT 

file_paths = glob.glob("../dataset/*aily*shelter*ove*.csv")

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
    
def loadData(path, city):
    print(path[0])
    output_data = glob.glob(path[0])
    weather_data = glob.glob(path[1])
    inflation = glob.glob(path[2])[0]
    unemployment = glob.glob(path[3])[0]
    cpi = glob.glob(path[4])[0]

    #-------Output Data-------#
    #Loading up the links to the output dataset
    if city == "calgary":
        output_data = load_csv_to_pandas(output_data[0])

        output_data = output_data.drop(columns = ['YEAR', 'MONTH', 'Daytime'])
        output_data['Date'] = output_data['Date'].astype(str).apply(clean_and_standardize_date)
        output_data['Date'] =  pd.to_datetime(output_data['Date'])

        output_data = output_data.rename(columns = {'Date': 'OCCUPANCY_DATE'})
        big_data = output_data

    else:
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
    print("Min date: ", min_date)
    print("Max date: ", max_date)

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

    #-------Inflation Data-------#

    #loading up housing data
    inflation = load_csv_to_pandas(inflation)

    #Dropping irrelevant columns for housing dataset
    inflation = inflation.rename(columns = {inflation.columns[0]: 'OCCUPANCY_DATE'})
    inflation = inflation.rename(columns = {inflation.columns[1]: 'Inflation_Rate_Change'})

    date_df['OCCUPANCY_DATE'] = pd.to_datetime(date_df['OCCUPANCY_DATE'])
    date_df['YEAR_MONTH'] = date_df['OCCUPANCY_DATE'].dt.to_period('M')


    if city == "calgary":
        inflation['OCCUPANCY_DATE'] = pd.to_datetime(inflation['OCCUPANCY_DATE'], format="%y-%b", errors='coerce')

        # Prepare unemployment data (monthly values)
        inflation['OCCUPANCY_DATE'] = pd.to_datetime(inflation['OCCUPANCY_DATE'])
        inflation['YEAR_MONTH'] = inflation['OCCUPANCY_DATE'].dt.to_period('M')

        inflation = inflation[
            (inflation['OCCUPANCY_DATE'] >= pd.to_datetime(min_date)) &
            (inflation['OCCUPANCY_DATE'] <= pd.to_datetime(max_date))
        ]

        # Merge on the unified OCCUPANCY_DATE column
        inflation = pd.merge(date_df, inflation.drop(columns='OCCUPANCY_DATE'), on='YEAR_MONTH', how='left')
        inflation = inflation.drop(columns='YEAR_MONTH')

    else:
        inflation["OCCUPANCY_DATE"] = pd.to_datetime(inflation["OCCUPANCY_DATE"])
        inflation = inflation[inflation["OCCUPANCY_DATE"] <= max_date].reset_index(drop=True)
        inflation = pd.merge(inflation, date_df, on = 'OCCUPANCY_DATE', how = 'outer')
        inflation = inflation.sort_values(by='OCCUPANCY_DATE').reset_index(drop=True)
        inflation = inflation.ffill()

    #-------Unemployment Data-------#
    
    #Loading the unemployment dataset
    unemployment = load_csv_to_pandas(unemployment)
    
    #Analyize Data
    unemployment = unemployment.rename(columns = {unemployment.columns[0]:'OCCUPANCY_DATE'})

    if city == "calgary":
         unemployment = unemployment.rename(columns = {unemployment.columns[1]:'Unemployment_Rate'})
    else:
        unemployment = unemployment.drop(columns = ['Labour force 7', 'Employment 8', 'Unemployment 9'])
        unemployment = unemployment.rename(columns = {"Population 6": 'Population'})
        unemployment['Population'] = unemployment['Population'].str.replace(',', '', regex=False).astype(float)*1000
        unemployment = unemployment.rename(columns = {"Unemployment Rate 10": 'Unemployment_Rate'})
        unemployment = unemployment.rename(columns = {"Participation Rate 11": 'Employment_Participation_Rate'})
        unemployment = unemployment.rename(columns = {"Employment Rate 12": 'Employment_Rate'})

    # Convert both date columns to datetime objects representing first day of month
    unemployment['OCCUPANCY_DATE'] = pd.to_datetime(unemployment['OCCUPANCY_DATE'], format="%y-%b", errors='coerce')
    # date_df['OCCUPANCY_DATE'] = pd.to_datetime(date_df['OCCUPANCY_DATE'])
    # date_df['YEAR_MONTH'] = date_df['OCCUPANCY_DATE'].dt.to_period('M')

    # Prepare unemployment data (monthly values)
    unemployment['OCCUPANCY_DATE'] = pd.to_datetime(unemployment['OCCUPANCY_DATE'])
    unemployment['YEAR_MONTH'] = unemployment['OCCUPANCY_DATE'].dt.to_period('M')

    unemployment = unemployment[
        (unemployment['OCCUPANCY_DATE'] >= pd.to_datetime(min_date)) &
        (unemployment['OCCUPANCY_DATE'] <= pd.to_datetime(max_date))
    ]

    # Merge on the unified OCCUPANCY_DATE column
    unemployment = pd.merge(date_df, unemployment.drop(columns='OCCUPANCY_DATE'), on='YEAR_MONTH', how='left')
    unemployment = unemployment.drop(columns='YEAR_MONTH')

    #-------CPI Data-------#
    
    # Load the CPI data
    cpi = load_csv_to_pandas(cpi)

    # Keep only necessary columns
    columns_to_keep = ['ï»¿"REF_DATE"', 'GEO', 'Products and product groups', 'VALUE']
    cpi = cpi[columns_to_keep]

    # Rename for clarity
    cpi = cpi.rename(columns={
        'ï»¿"REF_DATE"': 'OCCUPANCY_DATE',
        'Products and product groups': 'CPI_Type',
        'VALUE': 'CPI_Value'
    })

    # Convert to datetime (first day of month)
    cpi['OCCUPANCY_DATE'] = pd.to_datetime(cpi['OCCUPANCY_DATE'])

    # Convert date_df to proper datetime and generate YEAR_MONTH
    date_df['OCCUPANCY_DATE'] = pd.to_datetime(date_df['OCCUPANCY_DATE'])
    date_df['YEAR_MONTH'] = date_df['OCCUPANCY_DATE'].dt.to_period('M')

    cpi['YEAR_MONTH'] = cpi['OCCUPANCY_DATE'].dt.to_period('M')

    # Filter CPI based on min/max date
    cpi = cpi[
        (cpi['OCCUPANCY_DATE'] >= pd.to_datetime(min_date)) &
        (cpi['OCCUPANCY_DATE'] <= pd.to_datetime(max_date))
    ]

    # Merge and broadcast monthly CPI across daily dates
    cpi = pd.merge(date_df, cpi.drop(columns='OCCUPANCY_DATE'), on='YEAR_MONTH', how='left')
    cpi = cpi.drop(columns='YEAR_MONTH')

    #-------Final Data Prep-------#

    # Merge the datasets together through date
    big_data = pd.merge(big_data, big_weather, on = 'OCCUPANCY_DATE', how = 'left')
    big_data = pd.merge(big_data, inflation, on = 'OCCUPANCY_DATE', how = 'left')
    big_data = pd.merge(big_data, unemployment, on = 'OCCUPANCY_DATE', how = 'left')
    big_data = pd.merge(big_data, cpi, on = 'OCCUPANCY_DATE', how = 'left')

    big_data = big_data.sort_values(by='OCCUPANCY_DATE')

    if city == "calgary":
        room_occupancy = big_data.pop('Overnight')
        room_capacity = big_data.pop('Capacity')
        big_data['OCCUPANCY_RATE_ROOMS'] = room_occupancy/room_capacity

        grouped_data = big_data.groupby('Shelter')
        shelter_data_frames = {}
        for shelter_id, shelter_group in grouped_data:
            shelter_data_frames[shelter_id] = shelter_group
            shelter_data_frames[shelter_id]['OCCUPANCY_DATE'] = pd.to_datetime(shelter_data_frames[shelter_id]['OCCUPANCY_DATE'])
    else:
        #Placing the bed and room occupancy column last
        room_occupancy = big_data['OCCUPANCY_RATE_ROOMS']
        bed_occupancy = big_data['OCCUPANCY_RATE_BEDS']
        big_data['OCCUPANCY_RATE_BEDS'] = bed_occupancy
        big_data['OCCUPANCY_RATE_ROOMS'] = room_occupancy

        grouped_data = big_data.groupby('PROGRAM_ID')
        shelter_data_frames = {}
        for shelter_id, shelter_group in grouped_data:
            shelter_data_frames[shelter_id] = shelter_group
            shelter_data_frames[shelter_id]['OCCUPANCY_DATE'] = pd.to_datetime(shelter_data_frames[shelter_id]['OCCUPANCY_DATE'])

    big_data.reset_index(inplace=True)
    big_data = big_data.drop(columns = ['index'])

    big_data.to_csv("../dataset/"+ city +"_data.csv", index=True)
    return big_data, shelter_data_frames

def merge_weather(city):
    new_csv_data = []
    for year in range(2013, 2025):
        filename = f"../dataset/{city}-weather-{year}.csv"
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new_csv_data.append([
                    row["Date/Time"],  # Date
                    row["Max Temp (°C)"],  # Max Temp
                    row["Min Temp (°C)"],  # Min Temp
                    row["Mean Temp (°C)"],  # Mean Temp
                    row["Total Rain (mm)"],  # Precipitation
                    row["Total Snow (cm)"],  # Snowfall
                    row["Snow on Grnd (cm)"],  # Snow Depth
                ])

    with open('weather-calgary-full.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date/Time", "Max Temp (°C)", "Min Temp (°C)", "Mean Temp (°C)", "Total Rain (mm)", "Total Snow (cm)", "Snow on Grnd (cm)"])
        writer.writerows(new_csv_data)

def merge_occupancy(city):
    new_csv_data = []
    for year in range(2021, 2026):
        filename = f"../dataset/{city}-occupancy-{year}.csv"
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new_csv_data.append([
                    row["OCCUPANCY_DATE"],  # Date
                    row["ORGANIZATION_NAME"],  # Max Temp
                    row["LOCATION_ID"],  # Min Temp
                    row["PROGRAM_ID"],  # Mean Temp
                    row["CAPACITY_ACTUAL_BED"],  # Precipitation
                    row["UNOCCUPIED_BEDS"],  # Snowfall
                    row["UNOCCUPIED_ROOMS"],  # Snow Depth
                ])

    with open('occupancy-toronto-full.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["OCCUPANCY_DATE", "ORGANIZATION_NAME", "LOCATION_ID", "PROGRAM_ID", "CAPACITY_ACTUAL_BED", "UNOCCUPIED_BEDS", "UNOCCUPIED_ROOMS"])
        writer.writerows(new_csv_data)

if __name__ == "__main__":
    city = "calgary"

    city_paths = {
    "calgary": calgary_path,
    "toronto": toronto_path,
}
    path = city_paths[city]
