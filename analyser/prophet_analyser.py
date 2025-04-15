import pandas as pd
import plotly
from prophet import Prophet

df = pd.read_csv('compiled_shelter_dataset_Toronto.csv')
df.head()


m = Prophet()
m.fit(df)


future = m.make_future_dataframe(periods=365)
future.tail()
