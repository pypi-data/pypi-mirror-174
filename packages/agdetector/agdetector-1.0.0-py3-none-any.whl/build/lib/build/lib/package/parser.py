"""
/***************************************************************************
                              Agricultural Field Detector
                             --------------------
        created              : 2022-10-28
        copyright            : (C) 2022 by Jhon Galindo
        email                : jhonalex.ue@gmail.com
 ***************************************************************************/
"""
import argparse

class Parser():
    """Parser provides a method to configure the command-line documentation for the module."""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
                prog='Agricultural Field Detector',
                description='A Python module that calculates the Normalized Difference Vegetation Index (NDVI) for a given image to detect agricultural fields. The output is a GeoTIFF with values of 255 where fields are located and 0 elsewhere.',
                epilog = 'For more information please contact jhonalex.ue@gmail.com')

    def create_parser(self):
        self.parser.add_argument('-i', '--image', metavar='', required=True, help='Path of the input image. File path.')
        self.parser.add_argument('-r', '--red', type=int, metavar='', required=True, help='Band of Red. Integer.')
        self.parser.add_argument('-n', '--nir', type=int, metavar='', required=True, help='Band of Near Infrared (NIR). Integer.')
        self.parser.add_argument('-t', '--threshold', type=float, metavar='', required=False, help='The threshold for determining which NDVI values should be considered as part of a field. Decimal.')
        self.parser.add_argument('-c', '--crs', metavar='', help='Coordinate reference system for the output image. Text, EPSG:####.')
        self.parser.add_argument('-e', '--export', metavar='', help='Path to export image. File path.')
        
        return self.parser.parse_args()


