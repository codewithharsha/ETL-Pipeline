import requests
import pandas as pd
import numpy as np
from shapely.wkt import loads
import geopandas as gpd
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv("Border_Crossing_Entry_Data.csv")

# data.head()

print(data.shape)

for col in data.columns:
    if data[col].dtype == 'object':
        data[col] = data[col].fillna('Unknown')
    else:
        data[col] = data[col].fillna(0)
print("Successfully Handled Null Values")

data = data.drop_duplicates()
print("Successfully Dropped Duplicates!!")
print("Shape after deleting duplicates:",data.shape)

# Explicitly convert to string (if not already)
cols_to_convert = ['Port Name', 'State', 'Border', 'Measure']
for col in cols_to_convert:
    data[col] = data[col].astype(str)
print("Successfully Handled Column types")

# Convert WKT Point string to shapely Point
data['geometry'] = data['Point'].apply(loads)
# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry='geometry')
print("Successfully Handled point column!!")

data['New Date'] = pd.to_datetime(data['Date'],errors='coerce')
print("Successfully Handled date column!!")


scaler = MinMaxScaler()
data[['Value_norm']] = scaler.fit_transform(data[['Value']])
print("Successfully scaled value column!!")


# Extract year, month, and day of week
data['Year'] = data['New Date'].dt.year
data['Month'] = data['New Date'].dt.month
data['Month_Name'] = data['New Date'].dt.month_name()

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

data['Season'] = data['Month'].apply(get_season)

print("Successfully added season column!!")

data['Traffic_Level'] = pd.cut(
    data['Value'],
    bins=[-1, 1000, 10000, float('inf')],
    labels=['Low', 'Medium', 'High']
)

print("Successfully added traffic level column!!")
print("No.f rows after processing the data:",len(data))
data.to_csv('processed_border_crossing_data.csv', index=False)