# Flight Data Miner

## Requirements
* Tested using Python 3.4
* Requires MatPlotLib

## Input Data
Takes JSON formated tabular data, with the following fields:
* Latitude and Longitude coordinates
* Altitude
* Speed
* Time

## Processing
* Remove gross inconsistent data
* Calculate lift-off and touch-down coordinates
* When applicable group isolated chuncks of data
