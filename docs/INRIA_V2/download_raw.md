# Download RAW data sources 

The INRIA dataset has been made from open and public domains data sources. Theses sources could be retrieved and used to reproduce the dataset, to script it creation and to improve it by :

* Enabling the use of original vector data and so doing instance segmentation and not only image segmentation witk a building pixel mask.
* Retrieving the data sources for the test area of the dataset who have not been redistributed during the initial challenge. These redistribution will enable to compare methodologies with the initial attended test data. 

The area are located on two countries : United State of America and Austria. For the former vector data are retrieved from different towns or counties open-data portal. 
For the area in USA the raster data come from the USGS high resolution aerial image and could be downloaded with the [EarthExplorer portal](https://earthexplorer.usgs.gov/) and machine to machine API.


If only the raw data sources link and metadata are needed see the following part on vector and data sources. For detail on how-to donwload data, mnaually or in script, see the link in the two following sections. And for a detailled step by step instructions to download and pre-process the data see {ref}`content:download:area-step-by-step`

## Download vector data sources


```{list-table} Inria vector data sources link
:header-rows: 1
:name: vector-sources

* - Towns / Area
  - Vector data source access
  - direct url
* - Austin
  - **Site** [Austin data portal](https://data.austintexas.gov/). **Dataset** : "Building Footprints Year 2013"
  - [direct download via export api](https://data.austintexas.gov/api/geospatial/3qcc-8uhz?accessType=DOWNLOAD&method=export&format=Shapefile)
* - Bellingham
  - **Site** : [Bellingham GIS Data Center](https://cob.org/services/maps/gis). **Dataset** : Structures > Buildings
  - [direct download url](https://data.cob.org/data/gis/SHP_Files/COB_struc_shps.zip)
* - Bloomington
  - **Site** : [Blomington open data portal](https://data.bloomington.in.gov). **Dataset** [Building Area](https://data.bloomington.in.gov/dataset/Building-Areas/vjpj-6g5i)
  - [direct download via export api](https://data.bloomington.in.gov/api/geospatial/vjpj-6g5i?accessType=DOWNLOAD&method=export&format=Shapefile)
* - Chicago
  - **Site** : [Chicago open data portal](https://data.bloomington.in.gov). **Dataset** [Building Footprints (deprecated January 2013)](https://data.cityofchicago.org/Buildings/Building-Footprints-deprecated-January-2013-/w2v3-isjw)
  - [direct download via export api](https://data.cityofchicago.org/download/w2v3-isjw/application%2Fzip)
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
  - dates
  - bounding box
  - dataset info
* - Austin
  - **Site** [EarthExplorer portal](https://earthexplorer.usgs.gov/). **Dataset** : "high_res_ortho"
  - "2011-09-01", "2012-09-01"]
  - Austin, Texas;  ll : [30.216, -97.790], ur : [30.2990, -97.6947] 
  - id dataset : 201112_austin_tx_6in_sp_cnir;
* - Bellingham
  - **Site** [EarthExplorer portal](https://earthexplorer.usgs.gov/). **Dataset** : "high_res_ortho"
  - "2009-01-01", "2012-01-01"
  - Bellingham, Whatcom county, Washington;  ll : [48.6976,  -122.518], ur : [48.7925,  -122.374]
  - id dataset : 200905_seattle-tacoma-olympia_wa_0x3000m_utm10_clr;
* - Bloomington
  - **Site** [EarthExplorer portal](https://earthexplorer.usgs.gov/). **Dataset** : "high_res_ortho"
  - "2010-01-01", "2012-01-01"
  - Bloomington, Monroe county, Indiana;  ll : [39.122,  -86.607], ur : [39.2041,  -86.4673]
  - id dataset : 201103_monroe_county_in_1ft_sp_cnir;
* - Chicago
  - **Site** [EarthExplorer portal](https://earthexplorer.usgs.gov/). **Dataset** : "high_res_ortho"
  - "2011-01-01", "2013-01-01"
  - Chicago, Cook county, Illinois;  ll : [41.824,  -87.7298], ur : [41.9059,  -87.6200]
  - id dataset : 201203_cook_county_il_6in_sp_cnir;
* - Innsbruck
  - TODO
  - TODO
  - TODO
  - TODO
* - Kitsap
  - TODO
  - TODO
  - TODO
  - TODO
* - sfo (san fransisco)
  - TODO
  - TODO
  - TODO
  - TODO
* - Tyrol-e (Tyrol east)
  - TODO
  - TODO
  - TODO
  - TODO
* - Tyrol-w (Tyrol West)
  - TODO
  - TODO
  - TODO
  - TODO
* - Vienna
  - TODO
  - TODO
  - TODO
  - TODO
```

*ll** is for **l**ower **l**eft coordinates and ur for **u**pper **r**ight coordinates. 

To download data from [EarthExplorer portal](https://earthexplorer.usgs.gov/) see the [detailled instructions](earth_explorer_download)

(content:download:area-step-by-step)=
## Step by step instructions to download data by area


Detailled step by step instructions to download and pre-process the data by area

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
