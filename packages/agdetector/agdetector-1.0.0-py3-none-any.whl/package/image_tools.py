"""
/***************************************************************************
                              Agricultural Field Detector
                             --------------------
        created              : 2022-10-28
        copyright            : (C) 2022 by Jhon Galindo
        email                : jhonalex.ue@gmail.com
 ***************************************************************************/
"""
import datetime
import logging
from os.path import exists
import rasterio as rio

class ImageTools:
    """ImageTools provides methods for operations related
    to opening, saving and loading bands from the input image 
    defined by the user."""

    def open_image(self, image):
        """Get the input image and grab the attributes associated it.
        ----------
        image : rasterio.dataset

        Returns
        -------
        dict: image, crs, width, height, bounds, meta, transform"""

        logging.info('Opening the image provided.')

        if exists(image):
            src_image = {}
            src = rio.open(image)

            src_image['image'] = src
            src_image['crs'] = src.crs
            src_image['width'] = src.width
            src_image['height'] = src.height
            src_image['bounds'] = src.bounds
            src_image['meta'] = src.meta.copy()
            src_image['transform'] = src.transform
        else:
            logging.error("The image path does not exist.")
            exit()

        logging.info('The image was opened.')
        return src_image

    def save_image(self, result, meta_image, meta_update, path_export):
        """Get the parameters to save the resultant image and its metadata on the defined path.
        ----------
        result : numpy.array
        meta_image : dict
        meta_image : dict
        meta_image : string
        """

        logging.info('Saving the resultant image.')
        now = datetime.datetime.now()

        if not path_export:
            path_export = '{}_{}_{}.tif'.format(now.strftime("%Y%b%d_%H%M%S"), 'NDVI', meta_update['crs'].split(':')[1])

        kwargs = meta_image
        kwargs.update(meta_update)
        
        try:
            with rio.open(path_export, 'w', **kwargs) as dst:
                dst.write_band(1, result.astype(rio.int16))
            logging.info('The image was saved successfully.')
        except:
            logging.exception("The image could not be saved.")


    def load_band(self, image, band):
        """Get the input image and the defined band number to read and return as an array.
        ----------
        image : rasterio.dataset
        band: int

        Returns
        -------
        band_loaded: numpy.array"""
        
        logging.info('Reading the band number: {}.'.format(band))
        if image.count >= band and band > 0:
            band_loaded = image.read(band)
        else:
            logging.error("The image does not have the band number: {}.".format(band))
            exit()

        return band_loaded