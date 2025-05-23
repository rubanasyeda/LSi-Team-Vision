import pandas as pd
import matplotlib.pyplot as plt
import plotly
from prophet.plot import plot_plotly, plot_components_plotly
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import utils

df = pd.read_csv('../dataset/calgary-occupancy.csv', usecols=['Date', 'Capacity'])
# print(df.head())
df.info()

df['Date'] = pd.to_datetime(df['Date'], format="%Y/%m/%d")
ts = df

ts.columns = ['ds', 'y']
# print(ts.head())
ts.info()

# temp = pd.read_csv('../dataset/toronto-weather-2021.csv',  usecols=['Date/Time', 'Mean Temp (°C)'])
# temp['Date/Time'] = pd.to_datetime(temp['Date/Time'], format="%Y-%m-%d")
# temp = temp.interpolate(method='linear')
# data_with_regressors = utils.add_regressor(ts, temp, varname='temp')
# print(data_with_regressors.head())
# data_with_regressors.info()
weather_data = pd.read_csv('weather-calgary-full.csv', usecols=['Date/Time', 'Mean Temp (°C)'])
weather_data['Date/Time'] = pd.to_datetime(weather_data['Date/Time'], format="%Y-%m-%d")
weather_data = weather_data.rename(columns={'Date/Time': 'ds', 'Mean Temp (°C)': 'temp'})
weather_data = weather_data.interpolate(method='linear')  # Handle missing values

# Merge with shelter data
# data_with_regressors = pd.merge(ts, weather_data, on='ds', how='left')

# employment_data = pd.read_csv('../dataset/toronto-unemployment-2021-2025.csv', usecols=['Date', 'Unemployment rate 10'])
# employment_data['Date'] = pd.to_datetime(employment_data['Date'], format="%y-%b")
# employment_data = employment_data.rename(columns={'Date': 'ds', 'Unemployment rate 10': 'unemployment'})
# employment_data = employment_data.interpolate(method='linear')  # Handle missing values
#
# # Merge with shelter data
# data_with_regressors = pd.merge(ts, weather_data, employment_data, on='ds', how='left')
data_with_regressors = pd.merge(ts, weather_data, on='ds', how='left')

# Handle NaN values in the 'temp' column
# data_with_regressors['temp'] = data_with_regressors['temp'].fillna(method='ffill')  # Forward fill
# data_with_regressors['temp'] = data_with_regressors['temp'].fillna(method='bfill')  # Backward fill
# Alternatively, you can use a default value like the mean temperature:
data_with_regressors['temp'] = data_with_regressors['temp'].fillna(data_with_regressors['temp'].mean())

# Ensure no NaN values remain
if data_with_regressors['temp'].isnull().any():
    raise ValueError("NaN values remain in the 'temp' column after filling.")


m = Prophet()
# m.add_regressor('temp', prior_scale=0.5, mode='multiplicative')
m.add_regressor('temp', prior_scale=0.5, mode='multiplicative')
# m.add_regressor('unemployment', prior_scale=0.5, mode='multiplicative')
m.fit(data_with_regressors)

future = m.make_future_dataframe(periods=60)
future = pd.merge(future, weather_data, on='ds', how='left')
# future = pd.merge(future, employment_data, on='ds', how='left')

# Ensure no NaN values remain in the regressors
future['temp'] = future['temp'].fillna(weather_data['temp'].mean())
# future['unemployment'] = future['unemployment'].fillna(employment_data['unemployment'].mean())

forecast = m.predict(future)
future.tail()
future.plot()

# forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig1 = m.plot(forecast)

df_cv = cross_validation(m, initial='780 days', period='100 days', horizon='365 days')
print(df_cv.head())

df_p = performance_metrics(df_cv)
print(df_p.head())
# forecast.head()
plot_plotly(m, forecast)

plot_components_plotly(m, forecast)

plt.show()
