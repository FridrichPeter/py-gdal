from osgeo import gdal
import subprocess

# Step 1: gdal_translate to compress and optimize the TIFF
input_file = r"D:\GEO\DOLET\--gdal--\bio\web\result.tif"
first_result = r"D:\GEO\DOLET\--gdal--\bio\web\first_result1.tif"

gdal_translate_options = [
     "gdal_translate", "-b", "1", "-b", "2", "-b", "3",  # Use only the first three bands
    "-of", "GTiff", "-ot", "Byte",
    "-co", "COMPRESS=JPEG", "-co", "JPEG_QUALITY=85",
    "-co", "PHOTOMETRIC=RGB", "-co", "TILED=YES",
    "-co", "BLOCKXSIZE=256", "-co", "BLOCKYSIZE=256",
    "-a_nodata", "0", input_file, first_result  # Using a single value for nodata
]

subprocess.run(gdal_translate_options)

# Step 2: gdaladdo to generate overviews
gdaladdo_options = [
    "gdaladdo", "-r", "AVERAGE",
    "--config", "JPEG_QUALITY_OVERVIEW", "80",
    "--config", "COMPRESS_OVERVIEW", "JPEG",
    "--config", "PHOTOMETRIC_OVERVIEW", "YCBCR",
    "--config", "INTERLEAVE_OVERVIEW", "PIXEL",
    "--config", "GDAL_TIFF_OVR_BLOCKSIZE", "256",
    first_result, "2", "4", "8", "16", "32", "64", "128", "256"
]

subprocess.run(gdaladdo_options)

# Step 3: gdalwarp to reproject and finalize the TIFF
final_result = r"D:\GEO\DOLET\--gdal--\bio\web\final_result_test.tif"

gdalwarp_options = [
    "gdalwarp", "-multi", "-wo", "NUM_THREADS=3",
    "-r", "lanczos", "-dstnodata", "0",
    "-tr", "0.0746455354243517", "0.0746455354243517",
    "-t_srs", "EPSG:32634",
    "-of", "GTiff", "-ot", "Byte",
    "-co", "COMPRESS=LZW", "-co", "PHOTOMETRIC=RGB", "-co", "INTERLEAVE=PIXEL",
    "-co", "TILED=YES", "-co", "BLOCKXSIZE=256", "-co", "BLOCKYSIZE=256",
    first_result, final_result
]


subprocess.run(gdalwarp_options)

print("Raster optimization and reprojection completed.")
