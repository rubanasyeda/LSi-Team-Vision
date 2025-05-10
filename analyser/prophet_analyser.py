import pandas as pd
import matplotlib.pyplot as plt
import plotly
from prophet.plot import plot_plotly, plot_components_plotly
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import utils

df = pd.read_csv('compiled_shelter_dataset_Toronto.csv', usecols=['DATE', 'CURRENT_OCCUPANCY'])
# print(df.head())
df.info()

df['DATE'] = pd.to_datetime(df['DATE'], format="%Y-%m-%d")
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

m = Prophet()
# m.add_regressor('temp', prior_scale=0.5, mode='multiplicative')
m.fit(ts)

future = m.make_future_dataframe(periods=60)
future.tail()
future.plot()

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig1 = m.plot(forecast)

df_cv = cross_validation(m, initial='730 days', period='100 days', horizon='365 days')
print(df_cv.head())

df_p = performance_metrics(df_cv)
print(df_p.head())
# forecast.head()
plot_plotly(m, forecast)

plot_components_plotly(m, forecast)

# plt.show()
