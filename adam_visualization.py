
# coding: utf-8

# In[1]:

get_ipython().magic(u'matplotlib inline')
import pandas as pd
import geopandas as gpd
import numpy as np
import folium
from shapely.geometry import Polygon, Point 
import folium.colormap as cm


# In[2]:

crime_chicago = pd.read_pickle('crime_chicago_with_timestamp.pkl')


# #### Binning

# In[8]:

number_of_bins = 20
no = number_of_bins

lat_min = crime_chicago['Latitude'].min()
lon_min = crime_chicago['Longitude'].min()

lat_span = crime_chicago['Latitude'].max() - crime_chicago['Latitude'].min()
lon_span = crime_chicago['Longitude'].max() - crime_chicago['Longitude'].min()

lat_step = lat_span / no
lon_step = lon_span / no


# In[9]:

crime_chicago['bin'] =     no*np.floor((crime_chicago['Longitude']-lon_min)/lon_step) +        np.floor((crime_chicago['Latitude'] -lat_min)/lat_step)


# In[10]:

def getCornerLatLonForBin(bin_no):
    return (
        lat_min + (bin_no % no)         *lat_step, 
        lon_min + np.floor(bin_no / no) *lon_step
    )


# In[11]:

def getPolygonForBin(bin_no):
    lat, lon = getCornerLatLonForBin(bin_no)
    return Polygon([
            (lat,            lon),
            (lat,            lon + lon_step),
            (lat + lat_step, lon + lon_step),
            (lat + lat_step, lon),
        ])


# In[12]:

def getPolygonForBinReverse(bin_no):
    lat, lon = getCornerLatLonForBin(bin_no)
    return Polygon([
            (lon,            lat),
            (lon + lon_step, lat),
            (lon + lon_step, lat + lat_step),
            (lon,            lat + lat_step),
        ])


# #### Grouping

# In[13]:

crime_chicago_count = crime_chicago[['bin']].groupby(['bin']).size().reset_index().rename(columns={0:'count'})


# #### Transforming to GeoDataFrame

# In[14]:

crime_chicago_count_gpd = None


# In[15]:

crime_chicago_count_gpd = gpd.GeoDataFrame(crime_chicago_count)


# In[16]:

crime_chicago_count_gpd.geometry = crime_chicago_count_gpd['bin']     .map(lambda x: getPolygonForBinReverse(x))


# In[17]:

max_count = crime_chicago_count_gpd['count'].max()
crime_chicago_count_gpd['relative_count'] = crime_chicago_count_gpd['count']/max_count


# In[37]:

scale = cm.LinearColormap(['green','yellow','red'])
scale


# In[42]:

scale = cm.LinearColormap(['green','yellow','red']).to_step(n=100, method='log')
scale


# In[43]:

crime_chicago_count_gpd['style'] = crime_chicago_count_gpd['relative_count']     .map(lambda x: {'fillColor' : scale(x), 'weight' : 0})


# In[40]:

crime_chicago_count_gpd.crs = {'init': 'epsg:4326', 'no_defs': True}


# In[44]:

m = folium.Map([41.80,-87.75], zoom_start=11, tiles='cartodbpositron')

folium.GeoJson(crime_chicago_count_gpd).add_to(m)

m


# May be useful later

# In[18]:

# m = folium.Map([41.80,-87.75], zoom_start=11, tiles='cartodbpositron')

# folium.GeoJson(
#     crime_chicago_count_gpd,
#     style_function=lambda feature: {
#         'fillColor': linear(crime_chicago_count_gpd[]),
#         'color' : 'black',
#         'weight' : 2,
#         'dashArray' : '5, 5'
#         }).add_to(m)

# m

