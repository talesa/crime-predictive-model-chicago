### EdPredPol
#### Chicago crime predictive model

This project has been developed for the [Smart Data Hack 2016](http://smartdatahack.org/) at the University of Edinburgh, 15-19 February 2016.

Team: [Adam Golinski](http://adamgol.me/), [Lorenzo Martinico](https://github.com/lzmartinico), [Branislav Pilnan](https://github.com/brano2) and [Ondrej Bohdal](https://github.com/ondrejbohdal).

##### Setup
We suggest using `virtualenv`. To install all the necessary dependencies run `pip install -r requirements.txt`.

Crime data can be obtained in the form of a CSV file from the [City of Chicago data portal](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2).  
Weather data can be obtained from the [NOAA website](https://www.ncdc.noaa.gov/cdo-web/datasets).

##### Structure of the project
We collaborated on data exploration and investigation using `jupyter notebook` and the semi human readable results with accompanying comments are available as `.ipynb` files in the `exploration` folder.

We've also created a simple Python Flask-backend webapp for web presentation of part of the work done and results obtained. You can run the webapp by running `python webapp.py`.

##### Mathematical model
We've used a [Generalized Linear Model](https://en.wikipedia.org/wiki/Generalized_linear_model) using [`statsmodel.api.GLM`](http://statsmodels.sourceforge.net/devel/glm.html) with Poisson distribution and log link.

##### Contact
Feel free to reach out to any of us concerning this project or anything else, every interest is most welcome :)