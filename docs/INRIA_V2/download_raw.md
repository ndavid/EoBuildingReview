# Download RAW data sources 

The INRIA dataset has been made from open and public domains data sources. Theses sources could be retrieved and used to reproduce the dataset, to script it creation and to improve it by :

* Enabling the use of original vector data and so doing instance segmentation and not only image segmentation witk a building pixel mask.
* Retrieving the data sources for the test area of the dataset who have not been redistributed during the initial challenge. These redistribution will enable to compare methodologies with the initial attended test data. 

The area are located on two countries : United State of America and Austria. For the former vector data are retrieved from different towns or counties open-data portal. 
For the area in USA the raster data come from the USGS high resolution aerial image and could be dowloader with the [EarthExplorer portal](https://earthexplorer.usgs.gov/) and machine to machine API.

For a detailled step by step instructions to download and pre-process the data see the corresponding page by area :

* [Austin](austin)
* Bellingham
* Bloomington
* Chicago
* Innsbruck
* Kitsap
* sfo (san fransisco)
* Tyrol-e (Tyrol east)
* Tyrol-w (Tyrol West)
* Vienna

If only the raw data sources link and metadata are needed see the following part on vector and data sources. 


## Download vector data sources


```{list-table} Inria vector data sources link
:header-rows: 1
:name: vector-sources

* - Towns / Area
  - Vector data source access
  - direct url
* - Austin
  - **Site** Austin data portal : https://data.austintexas.gov/. **Dataset** : "Building Footprints Year 2013"
  - [direct download via export api](https://data.austintexas.gov/api/geospatial/3qcc-8uhz?accessType=DOWNLOAD&method=export&format=Shapefile)
* - Bellingham
  - TODO
  - TODO
* - Bloomington
  - TODO
  - TODO
* - Chicago
  - TODO
  - TODO
* - Innsbruck
  - TODO
  - TODO
* - Kitsap
  - TODO
  - TODO
* - sfo (san fransisco)
  - TODO
  - TODO
* - Tyrol-e (Tyrol east)
  - TODO
  - TODO
* - Tyrol-w (Tyrol West)
  - TODO
  - TODO
* - Vienna
  - TODO
  - TODO
```

## Image (Raster) data sources


```{list-table} Inria raster data sources link
:header-rows: 1
:name: raster-sources

* - Towns / Area
  - Data source access
  - data filter
* - Austin
  - **Site** [EarthExplorer portal](https://earthexplorer.usgs.gov/). **Dataset** : "Building Footprints Year 2013"
  - dataset : high_res_ortho; dates : ["2011-09-01", "2012-09-01"]; area : austin, texas;  ll : [30.2225,  -97.8013], ur : [30.2990,  -97.6544]
* - Bellingham
  - TODO
  - TODO
* - Bloomington
  - TODO
  - TODO
* - Chicago
  - TODO
  - TODO
* - Innsbruck
  - TODO
  - TODO
* - Kitsap
  - TODO
  - TODO
* - sfo (san fransisco)
  - TODO
  - TODO
* - Tyrol-e (Tyrol east)
  - TODO
  - TODO
* - Tyrol-w (Tyrol West)
  - TODO
  - TODO
* - Vienna
  - TODO
  - TODO
```