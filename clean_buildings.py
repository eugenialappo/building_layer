import geopandas as gpd
import pandas as pd
from shapely.geometry import box

#data location, aoi and crs definitions
official_file = "data/hausumringe.shp"
osm_file = "data/gis_osm_buildings_a_free_1.shp"
output_file = "data/clean_buildings.shp"
aoi_bounds = (693272.2765,5334639.8594,694092.5774,5335238.0172)
target_crs = "EPSG:32632"

def unite_layers(official_path, osm_path, aoi_bounds, target_crs):
    gdf_official = gpd.read_file(official_path)
    gdf_osm = gpd.read_file(osm_path)
    #reprojection
    gdf_official = gdf_official.to_crs(target_crs)
    gdf_osm = gdf_osm.to_crs(target_crs)
    #data clipping for further processing
    aoi_geom = gpd.GeoSeries([box(*aoi_bounds)], crs="EPSG:32632").to_crs(target_crs).iloc[0]
    gdf_official = gdf_official.clip(aoi_geom)
    gdf_osm = gdf_osm.clip(aoi_geom)
    gdf_official['source'] = 'Official'
    gdf_osm['source'] = 'OSM'
    #find all non-overlapping data in the osm file
    gdf_osm_reset = gdf_osm.reset_index(drop=False).rename(columns={'index': 'osm_original_index'})
    overlap_join = gpd.sjoin(
        gdf_osm_reset,
        gdf_official,
        how="left",
        predicate="intersects"
    )
    missing_osm = overlap_join[overlap_join['index_right'].isna()]
    osm_indices_non_over = missing_osm['osm_original_index'].unique()
    gdf_osm_non_over = gdf_osm.loc[osm_indices_non_over]
    #structuring and cleaning the data
    official_cols = ['source', 'geometry']
    osm_cols = ['source', 'geometry']
    gdf_official_clean = gdf_official[[col for col in official_cols if col in gdf_official.columns]]
    gdf_osm_clean = gdf_osm_non_over[[col for col in osm_cols if col in gdf_osm_non_over.columns]]
    #uniting the data and saving the file
    unified_data = pd.concat([gdf_official_clean, gdf_osm_clean], ignore_index=True)
    unified_data = gpd.GeoDataFrame(unified_data, crs=target_crs)
    unified_data.to_file(output_file)
    print(f"File with buildings saved to: {output_file}")

if __name__ == "__main__":
    unite_layers(official_file, osm_file, aoi_bounds, target_crs)
