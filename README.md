# Water World

Author: Athan Walker [athanwalker@email.arizona.edu](mailto:athanwalker@email.arizona.edu)  
Date: 12/7/2020

## About
Water World is a web-based choropleth that colors roughly 200 countries based on user selected water attributes during a selected year, such as 'water withdrawn per capita' in the year 2015.
All water data used in this project is taken from AQUASTAT, the United Nations Food and Agriculture Organization's open source database.

## Notes
To run:
* Clone this repo
* Within cloned repo execute the command ```npm run serve```

## Included Files
The files which I have take credit for writing are
* csc583ProjectRepo/examples/index.html - Builds and operates on the page. Includes D3 and JS code
* csc583ProjectRepo/examples/myWaterMap.css - Style page for index.html
* csc583ProjectRepo/src/py/* - The python code and csv files in result of executing python code. Purpose was to parse through large data folder and create a csv file per data category. These are then read by index.html
* csc583ProjectRepo/data/* - Contains the raw data of the project
Everything else has been provided by this [d3-geomap repo](https://github.com/yaph/d3-geomap.git)

