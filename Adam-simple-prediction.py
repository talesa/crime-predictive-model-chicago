
# coding: utf-8

# In[1]:

get_ipython().magic(u'matplotlib inline')
import pandas as pd
import numpy as np
import statsmodels as sm
import pickle


# In[4]:

crime_chicago = pd.read_pickle('crime_chicago_with_timestamp.pkl')


# In[5]:

crime_chicago.head(1)


# ### Manipulating data

# Binning the data with the size of the bin equal `bin_size`

# In[9]:

bin_size = 400


# In[10]:

crime_chicago['bin_x'] = np.floor(crime_chicago['X Coordinate']/bin_size)
crime_chicago['bin_y'] = np.floor(crime_chicago['Y Coordinate']/bin_size)


# In[12]:

crime_chicago_count = crime_chicago[['bin_x','bin_y']].groupby(['bin_x','bin_y']).size().reset_index().rename(columns={0:'count'})


# In[13]:

crime_chicago_count['count'].describe()

