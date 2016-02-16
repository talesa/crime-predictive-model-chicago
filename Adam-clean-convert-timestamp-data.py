
# coding: utf-8

# Library imports

# In[152]:

get_ipython().magic(u'matplotlib inline')
import pandas as pd
import numpy as np
import pickle


# Importing data

# In[96]:

crime_chicago = pd.read_csv('Crimes_-_2001_to_present.csv')


# `head(x)` displays first `x` rows of data

# In[3]:

crime_chicago.head(1)


# ### Cleaning up the data

# Dropping the data outside of our defined boundaries of Chicago

# In[97]:

max_lat = 42.017888
min_lat = 41.646487
max_lon = -87.525492
min_lon = -87.821101


# In[98]:

crime_chicago.loc[(crime_chicago['Latitude'] > max_lat),['Latitude']] = np.NaN
crime_chicago.loc[(crime_chicago['Longitude'] > max_lon),['Longitude']] = np.NaN
crime_chicago.loc[(crime_chicago['Latitude'] < min_lat),['Latitude']] = np.NaN
crime_chicago.loc[(crime_chicago['Longitude'] < min_lon),['Longitude']] = np.NaN


# In[99]:

crime_chicago = crime_chicago.dropna(axis=0, how='any', subset=['Latitude','Longitude'], inplace=False)


# In[100]:

len(crime_chicago)


# In[101]:

max_x = crime_chicago['X Coordinate'].max()
max_x


# In[102]:

min_x = crime_chicago['X Coordinate'].min()
min_x


# In[103]:

max_y = crime_chicago['Y Coordinate'].max()
max_y


# In[104]:

min_y = crime_chicago['Y Coordinate'].min()
min_y


# Make X Coordinate and Y Coordinate absolute

# In[105]:

crime_chicago.loc[:,['X Coordinate']] = crime_chicago['X Coordinate'] - min_x
crime_chicago.loc[:,['Y Coordinate']] = crime_chicago['Y Coordinate'] - min_y


# Minimum and maximum dates for the data

# In[92]:

crime_chicago['Date'].min()


# In[90]:

crime_chicago['Date'].max()


# ### Manipulating data

# Adding `day` field

# In[137]:

crime_chicago['day'] = crime_chicago['Date'].map(lambda x: x[:10])


# In[140]:

crime_chicago['datetime'] = pd.to_datetime(crime_chicago['day'])


# Save timestamped data into `pickle` file

# In[151]:

crime_chicago.to_pickle('crime_chicago_with_timestamp.pkl')

