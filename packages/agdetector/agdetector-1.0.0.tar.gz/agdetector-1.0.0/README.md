# Agricultural Field Detector

A Python module that calculates the [Normalized Difference Vegetation Index (NDVI)](https://earthobservatory.nasa.gov/features/MeasuringVegetation/measuring_vegetation_2.php) for a given image to detect agricultural fields. The output is a GeoTIFF with values of 255 where fields are located and 0 elsewhere. 

# Environment setup - Installation

### Linux

1. Download the files to configure the application. 
2. Open your console and install Python 3.10 with the following command: ```sudo apt-get install python3.10```
3. Navigate to the folder where downloaded the files.
4. Run the following command: ```pip3 install agricultural_field_detector-1.1.0-py3-none-any.whl```

### Windows

**Note: It is important that you previously install GDAL on your device.**

1. Download the files to configure the application. 
2. Install Python 3.10.6 or greater (Go to the [Python](https://www.python.org/downloads/) web page and Click in Download Python).
3. Excute the installer.
4. Open Windows PowerShell and navigate to the folder where downloaded the files.
5. Run the following command: ```pip3 install agricultural_field_detector-1.1.0-py3-none-any.whl```

# How to use

## Sample code

To execute this agricultural field detector was created the following custom arguments:

| Argument| Abbreviation | Description                     | Expected value | Mandatory  
|---------|--------------|---------------------------------|---| ---|
| --image | -i           | Path of the input image.        | File path  | :heavy_check_mark: |
| --red   | -r           | Band of Red                     | Integer | :heavy_check_mark: |
| --n     | -n           | Band of Near Infrared (NIR)     | Integer |  :heavy_check_mark: |
|--threshold|-t |Threshold for determining which NDVI values should be considered as part of a field.|  Float |  :x: |
| --crs   | -c           | Coordinate reference system for the output image.    |  Text. EPSG:####. |  :x: |
| --export| -e           | Path to export image            | File path | :x: |

:x: Optional.


Users should define the path of the input image, the number of band Red and the number of the band Near-Infrared (NIR):

```
python3 run.py -i "/PATH/20210827_162545_60_2262_3B_AnalyticMS_8b.tif" -r 6 -n 8
```

In this case, the other arguments are defined by default:

| Argument    |  Default value                 |
|-------------|--------------------------------|
| --threshold | Calculated                     |
| --crs       | Lat/Long (EPSG:4326) projection|
| --export    | Path of the input image, with name format: *YYYYMonthDD_HHMMSS_NDVI_**crs***              |

Additionally, users can define arguments such as the threshold for determining which NDVI values should be considered as part of a field, the projection for the resultant image and the path for the resultant image:

```
python3 run.py -i "<Path>/20210827_162545_60_2262_3B_AnalyticMS_8b.tif" -r 6 -n 8 -t 0.15 -c EPSG:3857 -e "<Path>/ResultantImage.tif"
```

## Output

Users obtain a GeoTIFF on the desired path with the defined projection (see [Sample Code](#sample-code)).

![output](resources/Result.png)

The pixels in this output image where fields are located are 255 and 0 elsewhere. 

## Logs

When users execute the code, they can have access to information about the activities and operations of the Agricultural Field Detector through the file ```app.log```.

![output](resources/Logs.png)

# Author

Jhon Alexander Galindo Ambuila.
[jhonalex.ue@gmail.com](mailto:jhonalex.ue@gmail.com)