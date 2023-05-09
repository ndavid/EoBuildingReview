# INRIA : Aerial Labelling Dataset 

[The INRIA Aerial Image Labeling Dataset](https://project.inria.fr/aerialimagelabeling/>) has been proposed in 2017 by {cite:p}`maggiori2017dataset`.


## Download 

The data could be downloaded from the [INRIA dataset page](https://project.inria.fr/aerialimagelabeling/files/) or directly
from command line :

```{code-block} bash
mkdir -p EOData/INRIA
cd EOData/INRIA
curl -k https://files.inria.fr/aerialimagelabeling/getAerial.sh | bash
rm .7z.00*
```
