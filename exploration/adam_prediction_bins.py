
# coding: utf-8

# In[37]:

#get_ipython().magic(u'matplotlib inline')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import folium.colormap as cm
import geopandas as gpd
import folium
from shapely.geometry import Polygon, Point


# #### Everything from adam_simple_prediction

# In[2]:

crime_chicago = pd.read_pickle('../crime_chicago_with_timestamp.pkl')


# In[3]:

crime_chicago.index = pd.DatetimeIndex(crime_chicago.datetime)


# In[4]:

min_date = crime_chicago.index.min()
max_date = crime_chicago.index.max()
nobs = len(crime_chicago.index.unique())


# In[5]:

min_date


# In[6]:

weather_chicago = pd.read_csv('WeatherChicago20012016.csv')

def weather_date_to_datetime(date):
    return pd.datetime(int(date[0:4]), int(date[4:6]), int(date[6:]))

weather_chicago['DATE'] = weather_chicago['DATE'].map(lambda x: weather_date_to_datetime(str(x)))
weather_chicago.index = pd.DatetimeIndex(weather_chicago['DATE'])
tmin_mean = weather_chicago['TMIN'].mean()
tmax_mean = weather_chicago['TMAX'].mean()

weather_chicago.loc[weather_chicago['TMIN'] == -9999, ['TMIN']] = tmin_mean
weather_chicago.loc[weather_chicago['TMAX'] == -9999, ['TMAX']] = tmax_mean
weather_chicago.loc[weather_chicago['PRCP'] == -9999, ['PRCP']] = 0
weather_chicago.loc[weather_chicago['AWND'] == -9999, ['AWND']] = 0


# In[140]:

number_of_bins = 3
no = number_of_bins

lat_min = crime_chicago['Latitude'].min()
lon_min = crime_chicago['Longitude'].min()

lat_span = crime_chicago['Latitude'].max() - crime_chicago['Latitude'].min()
lon_span = crime_chicago['Longitude'].max() - crime_chicago['Longitude'].min()

lat_step = lat_span / no
lon_step = lon_span / no

crime_chicago['bin'] =     no*np.floor((crime_chicago['Longitude']-lon_min)/lon_step) +        np.floor((crime_chicago['Latitude'] -lat_min)/lat_step)


# In[141]:

def getPolygonForBin(bin_no):
    lat, lon = getCornerLatLonForBin(bin_no)
    return Polygon([
            (lat,            lon),
            (lat,            lon + lon_step),
            (lat + lat_step, lon + lon_step),
            (lat + lat_step, lon),
        ])
def getPolygonForBinReverse(bin_no):
    lat, lon = getCornerLatLonForBin(bin_no)
    return Polygon([
            (lon,            lat),
            (lon + lon_step, lat),
            (lon + lon_step, lat + lat_step),
            (lon,            lat + lat_step),
        ])
def getCornerLatLonForBin(bin_no):
    return (
        lat_min + (bin_no % no)         *lat_step,
        lon_min + np.floor(bin_no / no) *lon_step
    )


# # THEFTS ONLY

# In[142]:

# crime_chicago_copy = crime_chicago.copy()


# In[143]:

# crime_chicago = crime_chicago_copy.copy()


# In[144]:

# crime_chicago['Primary Type'].unique()


# In[145]:

# crime_chicago = crime_chicago[crime_chicago['Primary Type'] == 'THEFT']


# #### END OF CHOOSING CRIME TYPE

# In[146]:

crime_chicago_count_ref = crime_chicago[['datetime','bin']].groupby(['datetime','bin']).size().reset_index().rename(columns={0:'count'})


# In[147]:

def get_counts_by_date_for_bin(bin_no):
    crime_chicago_count_ref_temp = crime_chicago_count_ref.copy()
    crime_chicago_count_ref_temp.index = pd.DatetimeIndex(crime_chicago_count_ref['datetime'])
    crime_chicago_count_ref_temp = crime_chicago_count_ref_temp[crime_chicago_count_ref_temp['bin'] == bin_no]
    crime_chicago_count_ref_temp = crime_chicago_count_ref_temp.drop(['bin', 'datetime'], axis=1)
    crime_chicago_count_ref_temp = crime_chicago_count_ref_temp.reindex(pd.date_range(min_date.strftime('%Y-%m-%d'), periods=nobs, freq='D'))
    crime_chicago_count_ref_temp = crime_chicago_count_ref_temp.fillna(0)
    return crime_chicago_count_ref_temp


# ## Prediction

# In[148]:

import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy.stats.stats import pearsonr


# In[149]:

def add_dummies(temp):
    temp['weekday'] = temp.index.weekday
    temp['yearday'] = temp.index.dayofyear

    weekday_dummies = pd.get_dummies(temp['weekday'], prefix='weekday')
    weekday_dummies.index = temp.index

    yearday_dummies = pd.get_dummies(temp['yearday'], prefix='yearday')
    yearday_dummies.index = temp.index

    temp = temp.join(weekday_dummies).join(yearday_dummies)

    return temp


# In[150]:

def append_weather(bin_crime_data):
    bin_crime_data_weather = bin_crime_data.join(weather_chicago[['PRCP', 'TMAX','AWND']])
    indeces = pd.isnull(bin_crime_data_weather).any(1)
    bin_crime_data_weather.drop(bin_crime_data_weather.index[indeces], inplace=True)
    return bin_crime_data_weather


# In[167]:

def fit_sm_predict_row(endog, exog, predict_row):
    global start_params_lol
    print(start_params_lol)

    res_temp = sm.GLM(endog, exog, family=sm.families.Poisson(link=sm.families.links.log)).fit(start_params=start_params_lol)

    #crime_chicago_count_weather_weekdays.iloc[1,:]
    prediction = res_temp.predict(predict_row)

    start_params_lol = res_temp.params

    return prediction


# In[152]:

global start_params_lol
start_params_lol = np.zeros(366+7+2)


# In[153]:

def predict_for_bin(bin_crime_data, next_day_row):
    bin_crime_data = append_weather(bin_crime_data)

    bin_crime_data = add_dummies(bin_crime_data)

    #TODO change
    endog = bin_crime_data.loc[:, ['count']]
    exog = bin_crime_data.loc[:, 'PRCP':]
    exog = exog.drop(['AWND','weekday','yearday'], axis=1)

    prediction = fit_sm_predict_row(endog, exog, next_day_row)

    return prediction[0]


# ### Putting it all together

# In[154]:

def generate_nextday(temp, prcp):
    columns = ['TMAX','PRCP']
    for i in range(7):
        columns.append('weekday_' + str(i))
    for i in range(1, 367):
        columns.append('yearday_' + str(i))
    next_day_row = pd.DataFrame(columns = columns)
    next_day_row.loc[0,:] = np.zeros(len(next_day_row.columns))
    next_day_row.loc[0,'TMAX'] = 1
    next_day_row.loc[0,'PRCP'] = 2

    tomorrow = (datetime.date.today() + datetime.timedelta(days=1))
    next_day_row.loc[0,'weekday_' + str(tomorrow.weekday())] = 1
    day_of_the_year = tomorrow.timetuple().tm_yday
    next_day_row.loc[0,'yearday_' + str(day_of_the_year)] = 1

    return next_day_row


# In[155]:

def generate_predictions_for_all_bins(temp, prcp):
    df = pd.DataFrame()
    df['bin'] = np.arange(no*no)

    df['count'] = df['bin'].map(lambda x:
        predict_for_bin(
            get_counts_by_date_for_bin(x),
            generate_nextday(temp, prcp)
        )
    )

    return df


# In[156]:

import weather
tw = weather.fetch()
tw


# In[168]:

dfr = generate_predictions_for_all_bins(tw['temp'], tw['rain'])


# In[158]:

crime_chicago_count_gpd = None
crime_chicago_count_gpd = gpd.GeoDataFrame(dfr)
crime_chicago_count_gpd.geometry = crime_chicago_count_gpd['bin']     .map(lambda x: getPolygonForBinReverse(x))
max_count = crime_chicago_count_gpd['count'].max()
crime_chicago_count_gpd['relative_count'] = crime_chicago_count_gpd['count']/max_count


# In[159]:

linear = cm.LinearColormap(['green','yellow','red'])
linear


# In[160]:

crime_chicago_count_gpd['style'] = crime_chicago_count_gpd['relative_count']     .map(lambda x: {'fillColor' : linear(x), 'weight' : 0})


# In[161]:

crime_chicago_count_gpd.crs = {'init': 'epsg:4326', 'no_defs': True}


# In[162]:

m = folium.Map([41.80,-87.75], zoom_start=11, tiles='cartodbpositron')

folium.GeoJson(crime_chicago_count_gpd).add_to(m)


# In[163]:

m.add_children(folium.Marker([41.868648, -87.640007], popup="The Maxwell", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.897754, -87.623944], popup="Water Tower Place", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.899274, -87.624524], popup="900 North Michigan Shops", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.929220, -87.787405], popup="Brickyard Mall", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.891145, -87.624482], popup="The Shops at North Bridge", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.939177, -87.649695], popup="Pointe At Clark", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.926000, -87.673170], popup="Riverpoint Center", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.755380, -87.736369], popup="Ford City Mall", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.832392, -87.615014], popup="Lake Meadows Shopping Center", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.908722, -87.748696], popup="Washington Square Mall", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.991941, -87.655026], popup="Captains Walk Shopping Mall", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.932977, -87.648383], popup="Diversey Halsted Shopping Center", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.925253, -87.789883], popup="Bricktown Square", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.910541, -87.635704], popup="Pipers Alley Mall", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.890795, -87.616483], popup="Ogden Slip", icon=folium.Icon(color='gray')))

m.add_children(folium.Marker([41.883819, -87.627683], popup="Tiffany Dome", icon=folium.Icon(color='gray')))
m.add_children(folium.Marker([41.883533, -87.629430], popup="Block 37", icon=folium.Icon(color='gray')))


# In[164]:

m.save('tomorrow.html')


# - different crime types
# - bins
# - timescales
# - only shopping centre we're interested in (by hour?)

# ## 1
# - it's provided df with counted crimes
# - appends weather
# - finds empty records and drops them
# - predicts and plots

# ## 2
# - bins crimes within given two corners

# ## 3
# - chooses a crime type or provides all
