This script is the result of an issue I faced while working on one of my study projects!
I realised that relying only on official building data or only on OSM data meant not considering all of the buildings.
Official data is great, but not complete compared to satellite images; OSM can be messy.

As a solution, I combined them!
This tool automates the process of blending these two sources, prioritising the official data
and using OSM features only to fill in the missing buildings.
The result is a single and more complete building layer.

Important notes:
- the script excludes features that intersect with each other. It was done based on visual analysis of the results and can be adjusted if needed; 
- ensure bounding box coordinates are in EPSG:32632; the input data is being reprojected accordingly.
