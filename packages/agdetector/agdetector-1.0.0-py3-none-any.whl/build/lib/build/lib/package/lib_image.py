"""
/***************************************************************************
                              Agricultural Field Detector
                             --------------------
        created              : 2022-10-28
        copyright            : (C) 2022 by Jhon Galindo
        email                : jhonalex.ue@gmail.com
 ***************************************************************************/
"""
import logging
import numpy as np
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling

class LibImage:
    """LibImage provides methods to apply operations of transformation into the defined image."""

    def update_pixel_value(self, threshold, index):
        """Update the values from the index calculated considering the threshold defined.
        ----------
        threshold : int
        index: numpy.array

        Returns
        -------
        index: numpy.array"""

        if not threshold:
            threshold = abs(np.nanmax(index)) - ((abs(np.nanmax(index)) + abs(np.nanmin(index)))/2)
            logging.warning('Threshold is not defined. The value calculated is: {}'.format(threshold))
        
        logging.info('The threshold defined is: {}'.format(threshold))    

        index[np.isnan(index)] = 0
        index[index >= threshold] = 255
        index[index < threshold] = 0

        logging.info('Pixel values updated')

        return index

    def reprojection(self, dst_crs, image, image_updated):
        """Get the input image, the coordinate reference system (CRS) and the image calculated (index) to reproject it to the desired CRS.
        ----------
        dst_crs: numpy.array
        image: numpy.array
        image_updated: numpy.array

        Returns
        -------
        tuple: 
            destination: numpy.array
            metadata_dict: dict
        """

        if not dst_crs:
            dst_crs = 'EPSG:4326'
            logging.warning('CRS was not defined. Default value: EPSG:4326.')

        transform, width, height = calculate_default_transform(
            image['crs'], dst_crs, image['width'], image['height'], *image['bounds'])
        logging.info('Transform matrix calculated.')

        destination_shape = (height, width)
        destination = np.zeros(destination_shape, rio.float32)

        metadata_dict = {
            'nodata': 1,
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height,
            'dtype':rio.int16,
            'count': 1
        }

        logging.info('Reprojecting the image (index).')
        reproject(
            source=image_updated,
            destination=destination,
            src_transform=image['transform'],
            src_crs=image['crs'],
            dst_transform=transform,
            dst_crs=dst_crs,
            resampling=Resampling.nearest)
        logging.info('Image (index) reprojected.')

        return [destination, metadata_dict]