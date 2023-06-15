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
  - **Site** : [data.world](https://data.world/) or [Blomington open data portal](https://data.bloomington.in.gov). **Dataset** [Bloomington Municipal Boundary GIS Data](https://data.world/city-of-bloomington/522d7f69-8951-46f6-8cb4-30cad69878ca)[Building Area](https://data.bloomington.in.gov/dataset/Building-Areas/vjpj-6g5i)
  - dataworld API, [direct download via export api](https://data.bloomington.in.gov/api/geospatial/vjpj-6g5i?accessType=DOWNLOAD&method=export&format=Shapefile)
* - Chicago
  - **Site** : [Chicago open data portal](https://data.cityofchicago.org/). **Dataset** [Building Footprints Current](https://data.cityofchicago.org/Buildings/Building-Footprints-current-/hz9b-7nh8)
  - [direct download via export api](https://data.cityofchicago.org/api/geospatial/hz9b-7nh8?method=export&format=Shapefile)
* - Innsbruck
  - **Site** [Open GIS Government Data - Tirol](https://data-tiris.opendata.arcgis.com). **Dataset** [Gebaeude](https://data-tiris.opendata.arcgis.com/datasets/gebaeude-1)
  - esri download API [query url](https://opendata.arcgis.com/api/v3/datasets/9fa2f10f991c46739d51e77dbbd39534_0/downloads/data?format=shp&spatialRefId=31254&where=1%3D1)
* - Kitsap
  - **Site** : [Kitspa county portal open data portal](https://www.kitsapgov.com/dis/Pages/resources.aspx). **Dataset** [Parcel Base Map Layers/
Building Footprints](https://ftp.co.kitsap.wa.us/data/gis/datacd/arcview/layers/atsinfo/building.zip)
  - [direct download url](https://ftp.co.kitsap.wa.us/data/gis/datacd/arcview/layers/atsinfo/building.zip)
* - sfo (san fransisco)
  - **Site** : [Princeton library](https://maps.princeton.edu/catalog). **Dataset** [San Francisco (Building Footprints, 2011)](https://maps.princeton.edu/catalog/mit-dqtbhcmu3fmjkp)
  - [direct download url](https://geodata.mit.edu/mit_download/mit-dqtbhcmu3fmjk)
* - Tyrol-e (Tyrol east)
  - **Site** [Open GIS Government Data - Tirol](https://data-tiris.opendata.arcgis.com). **Dataset** [Gebaeude](https://data-tiris.opendata.arcgis.com/datasets/gebaeude-1)
  - esri download API [query url](https://opendata.arcgis.com/api/v3/datasets/9fa2f10f991c46739d51e77dbbd39534_0/downloads/data?format=shp&spatialRefId=31254&where=1%3D1)
* - Tyrol-w (Tyrol West)
  - **Site** [Open GIS Government Data - Tirol](https://data-tiris.opendata.arcgis.com). **Dataset** [Gebaeude](https://data-tiris.opendata.arcgis.com/datasets/gebaeude-1)
  - esri download API [query url](https://opendata.arcgis.com/api/v3/datasets/9fa2f10f991c46739d51e77dbbd39534_0/downloads/data?format=shp&spatialRefId=31254&where=1%3D1)
* - Vienna
  - **site** [Vienne geoportal](https://data.wien.gv.at) or [Map Viewer](https://www.wien.gv.at/ma41datenviewer/public/start.aspx). **Dataset**  [Baukörpermodell LOD1.4](https://www.wien.gv.at/stadtentwicklung/stadtvermessung/geodaten/bkm/daten.html). 
  - [WFS query service](https://data.wien.gv.at/daten/geo?service=WFS&version=1.0.0&request=GetFeature&typeName=ogdwien:FMZKGEBOGD&outputFormat=shape-zip&SRS=EPSG:31256&BBOX=-2237,335400,6828,344450) WFS Layer : FMZKGEBOGD
```

## Image (Raster) data sources


```{list-table} Inria raster data sources link
:header-rows: 1
:name: raster-sources

* - Towns / Area
  - Data source access
  - dates
  - bounding box
* - Austin
  - **Site** [EarthExplorer portal](https://earthexplorer.usgs.gov/). **Collection** : "high_res_ortho". **Dataset** : 201112_austin_tx_6in_sp_cnir
  - "2011-09-01", "2012-09-01"]
  - Austin, Texas;  ll : [30.216, -97.790], ur : [30.2990, -97.6947] 
* - Bellingham
  - **Site** [EarthExplorer portal](https://earthexplorer.usgs.gov/). **Collection** : "high_res_ortho". **Dataset** :  200905_seattle-tacoma-olympia_wa_0x3000m_utm10_clr
  - "2009-01-01", "2012-01-01"
  - Bellingham, Whatcom county, Washington;  ll : [48.6976,  -122.518], ur : [48.7925,  -122.374]
* - Bloomington
  - **Site** [EarthExplorer portal](https://earthexplorer.usgs.gov/). **Collection** : "high_res_ortho". **Dataset** : 201103_monroe_county_in_1ft_sp_cnir
  - "2010-01-01", "2012-01-01"
  - Bloomington, Monroe county, Indiana;  ll : [39.122,  -86.607], ur : [39.2041,  -86.4673]
* - Chicago
  - **Site** [EarthExplorer portal](https://earthexplorer.usgs.gov/). **Collection** : "high_res_ortho". **Dataset** : 201203_cook_county_il_6in_sp_cnir
  - "2011-01-01", "2013-01-01"
  - Chicago, Cook county, Illinois;  ll : [41.824,  -87.7298], ur : [41.9059,  -87.6200]
* - Innsbruck
  - TODO
  - TODO
  - TODO
* - Kitsap
  - **Site** [EarthExplorer portal](https://earthexplorer.usgs.gov/). **Collection** : "high_res_ortho". **Dataset** : 200905_seattle-tacoma-olympia_wa_0x3000m_utm10_clr
  - "2009-01-01", "2010-01-01"
  - Port Orchard, kitsap county, Washington;  ll : [47.4566,  -122.7082], ur : [47.5788, -122.5880]
* - sfo (san francisco)
  - **Site** [EarthExplorer portal](https://earthexplorer.usgs.gov/). **Collection** : "high_res_ortho". **Dataset** : 201104_san_francisco_ca_0x3000m_utm_clr
  - "2010-01-01", "2012-01-01" 
  - san francisco, san francisco county, California;  ll : [37.7161,  -122.4952], ur : [37.7979, -122.3921]
* - Tyrol-e (Tyrol east)
  - TODO
  - TODO
  - TODO
* - Tyrol-w (Tyrol West)
  - TODO
  - TODO
  - TODO
* - Vienna
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
