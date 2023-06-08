# Aerial Image Labeling review

[The INRIA Aerial Image Labeling Dataset](https://project.inria.fr/aerialimagelabeling/>) has been proposed in 2017 by {cite:p}`maggiori2017dataset`.
The dataset has been made by collecting diverses open-data sources of aerial imagery and building footpring and it's dedicted to building detection task as a **semantic segmentation** problem. 

## Existing data and issues 

This dataset is use in many research articles on building delineation as a benchmark to compare with other methodologies but some issues has been noted when using this dataset :

* **Unavailable test data** :  The test data used by the original benchmark site has not been released at the benchmark end. Consequently many articles didn't used the original test partition to reports their results. They instead used a new train/val/test partition made with the original train/val data. So, depending on the papers the real used dataset aren't the same, which lead to not being able to trustfully compared the différents published results and methodlogies. 
Moreover, the new test partition use data on the same geographical areas and images acquisition missions than the training and validation dataset and so has lost the ability to measure the generalization power of a building delineation methodology (to new data and geographicla areas) and is subject to strong spatial correlation.
* **Non-vector (binary) building mask** : The building data are on a binay image (mask) format and so are not well adapted for the more recents methodologies which use instance segmentation or aim to directly producing vecto data (building footprint as a polygon and not a pixel mask). 
* **Unknown data quality** : The data has been automatically annotated (by using existing building footprint) and not manually annoted from aerial image and the corresponding annotation quality is not exactly known. Existing labelling issues has already been noted by researchers.   

## Download original dataset 

The original dataset could be downloaded from the [INRIA dataset page](https://project.inria.fr/aerialimagelabeling/files/) or directly
from command line :

```{code-block} bash
mkdir -p EOData/INRIA
cd EOData/INRIA
curl -k https://files.inria.fr/aerialimagelabeling/getAerial.sh | bash
rm .7z.00*
```



