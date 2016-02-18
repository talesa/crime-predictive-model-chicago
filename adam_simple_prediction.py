
# coding: utf-8

# In[49]:

get_ipython().magic(u'matplotlib inline')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:

crime_chicago = pd.read_pickle('crime_chicago_with_timestamp.pkl')


# In[3]:

crime_chicago.head(1)


# ### Manipulating data

# Binning the data with the size of the bin equal `bin_size`

# In[4]:

number_of_bins = 70
no = number_of_bins

lat_min = crime_chicago['Latitude'].min()
lon_min = crime_chicago['Longitude'].min()

lat_span = crime_chicago['Latitude'].max() - crime_chicago['Latitude'].min()
lon_span = crime_chicago['Longitude'].max() - crime_chicago['Longitude'].min()

lat_step = lat_span / no
lon_step = lon_span / no


# In[5]:

crime_chicago['bin'] =     no*np.floor((crime_chicago['Longitude']-lon_min)/lon_step) +        np.floor((crime_chicago['Latitude'] -lat_min)/lat_step)


# In[6]:

def getPolygonForBin(bin_no):
    lat, lon = getCornerLatLonForBin(bin_no)
    return Polygon([
            (lat,            lon),
            (lat,            lon + lon_step),
            (lat + lat_step, lon + lon_step),
            (lat + lat_step, lon),
        ])


# In[7]:

def getPolygonForBinReverse(bin_no):
    lat, lon = getCornerLatLonForBin(bin_no)
    return Polygon([
            (lon,            lat),
            (lon + lon_step, lat),
            (lon + lon_step, lat + lat_step),
            (lon,            lat + lat_step),
        ])


# #### Grouping

# In[8]:

crime_chicago['datetime'].head(1)


# In[9]:

crime_chicago.index = pd.DatetimeIndex(crime_chicago['datetime'])


# In[10]:

crime_chicago_count = crime_chicago[['bin', 'datetime']].groupby(['bin', 'datetime']).size().reset_index().rename(columns={0:'count'})


# In[11]:

crime_chicago_count['count'].describe()


# In[12]:

crime_chicago_count.index = pd.DatetimeIndex(crime_chicago_count['datetime'])


# In[13]:

crime_chicago_count.head(1)


# ### Importing weather data

# In[14]:

weather_chicago = pd.read_csv('WeatherChicago20012016.csv')


# In[15]:

def weather_date_to_datetime(date):
#     print date[0:4], date[6:], date[4:6]
    return pd.datetime(int(date[0:4]), int(date[4:6]), int(date[6:]))


# In[16]:

weather_chicago['DATE'] = weather_chicago['DATE'].map(lambda x: weather_date_to_datetime(str(x)))


# In[17]:

weather_chicago.index = pd.DatetimeIndex(weather_chicago['DATE'])


# In[18]:

tmin_mean = weather_chicago['TMIN'].mean()
tmax_mean = weather_chicago['TMAX'].mean()

weather_chicago.loc[weather_chicago['TMIN'] == -9999, ['TMIN']] = tmin_mean
weather_chicago.loc[weather_chicago['TMAX'] == -9999, ['TMAX']] = tmax_mean
weather_chicago.loc[weather_chicago['PRCP'] == -9999, ['PRCP']] = 0
weather_chicago.loc[weather_chicago['AWND'] == -9999, ['AWND']] = 0


# In[19]:

weather_chicago.describe()


# In[20]:

weather_chicago.head(2)


# ### Concatenating crimes and weather

# In[21]:

crime_chicago_count_ref = crime_chicago[['datetime']].groupby(['datetime']).size().reset_index().rename(columns={0:'count'})
crime_chicago_count_ref.index = pd.DatetimeIndex(crime_chicago_count_ref['datetime'])
crime_chicago_count_ref.head(1)


# In[22]:

crime_chicago_count_weather = crime_chicago_count_ref.join(weather_chicago[['PRCP', 'TMAX','AWND']])


# In[23]:

crime_chicago_count_weather.head(1)


# #### Finding empty records

# In[24]:

indeces = pd.isnull(crime_chicago_count_weather).any(1)
crime_chicago_count_weather.drop(crime_chicago_count_weather.index[indeces], inplace=True)
len(crime_chicago_count_weather)


# ## Trying to predict 

# In[50]:

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy.stats.stats import pearsonr


# In[26]:

crime_chicago_count_weather.describe()


# In[27]:

crime_chicago_count_weather['ones'] = crime_chicago_count_weather.loc[:,['count']]
crime_chicago_count_weather.loc[:,['ones']] = 1
dta = crime_chicago_count_weather


# In[28]:

res = smf.glm('count~TMAX', data=dta, 
                family=sm.families.Poisson(link=sm.families.links.log)).fit()
res.summary()


# In[53]:

res = smf.glm('count~TMAX', data=dta, 
                family=sm.families.Poisson(link=sm.families.links.log)).fit()
res.summary()


# In[29]:

nobs = res.nobs
yhat = res.mu


# In[30]:

from statsmodels.graphics.api import abline_plot


# In[39]:

y = crime_chicago_count_weather.loc[:,'count']


# In[40]:

len(y)


# In[41]:

len(yhat)


# In[56]:

yhat[:] = crime_chicago_count_weather['count'].mean()


# In[57]:

yhat


# In[51]:

fig, ax = plt.subplots()
ax.scatter(yhat, y)
line_fit = sm.OLS(y, sm.add_constant(yhat, prepend=True)).fit()
abline_plot(model_results=line_fit, ax=ax)

plt.axis([0, 2000, 0, 2000])

ax.set_title('Model Fit Plot')
ax.set_ylabel('Observed values')
ax.set_xlabel('Fitted values');


# In[60]:

fig, ax = plt.subplots()
ax.scatter(yhat, y)
line_fit = sm.OLS(y, sm.add_constant(yhat, prepend=True)).fit()
# abline_plot(model_results=1, ax=ax)

plt.axis([0, 2000, 0, 2000])

ax.set_title('Model Fit Plot')
ax.set_ylabel('Observed values')
ax.set_xlabel('Fitted values');


# In[ ]:



