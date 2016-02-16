
# coding: utf-8

# Library imports

# In[37]:

import pandas as pd
import numpy as np


# Importing data

# In[2]:

crime_chicago = pd.read_csv('Crimes_-_2001_to_present.csv')


# `head(x)` displays first `x` rows of data

# In[16]:

crime_chicago.head(1)


# ### Data exploration

# There are X and Y Coordinate field which seems to be exactly what we need, we can just define bins by some range of that value (I don't quite know what quantity it represents yet).

# In[31]:

max_x = crime_chicago['X Coordinate'].max()
max_x


# In[30]:

max_y = crime_chicago['Y Coordinate'].max()
max_y


# `[0,0]` X,Y Cooridnates translate into Location

# In[29]:

min_loc = crime_chicago[(crime_chicago['X Coordinate'] == 0) | (crime_chicago['Y Coordinate'] == 0)]['Location'].head(1)
min_loc


# `[max_x,max_y]` X,Y Cooridnates translate into Location

# In[32]:

max_loc = crime_chicago[(crime_chicago['X Coordinate'] == max_x) | (crime_chicago['Y Coordinate'] == max_y)]['Location'].head(1)
max_loc


# Minimum and maximum dates for the data

# In[46]:

crime_chicago['Date'].min()


# In[47]:

crime_chicago['Date'].max()


# ### Data manipulation

# Now, binning the data with the size of the bin equal `bin_size`

# In[33]:

bin_size = 100


# In[41]:

crime_chicago['bin_x'] = np.floor(crime_chicago['X Coordinate']/bin_size)
crime_chicago['bin_y'] = np.floor(crime_chicago['Y Coordinate']/bin_size)


# Number of bins

# In[60]:

np.round(max_x/bin_size*max_y/bin_size)


# Counting crime incidents

# In[51]:

crime_chicago_count = crime_chicago[['bin_x','bin_y']].groupby(['bin_x','bin_y']).size().reset_index().rename(columns={0:'count'})


# In[57]:

crime_chicago_count['count'].describe()


# In[67]:

max_crimes = crime_chicago_count['count'].max()
crime_chicago_count[crime_chicago_count['count'] == max_crimes]


# In[68]:

crime_chicago_count['count'].max()

