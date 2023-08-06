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

class IndexesMethods:
    """IndexesMethods provides methods for calculations related to Indexes for digital image processing."""

    def __init__(self):
        # Division by zero.
        np.seterr(divide='ignore', invalid='ignore')

    def ndvi(self, nir, red):
        """Get the Red and Near-Infrared bands to calculate and return the NDVI index as an array.
        ----------
        nir : numpy.array
        red: numpy.array

        Returns
        -------
        ndvi: numpy.array"""

        ndvi = (nir.astype(float) - red.astype(float)) / (nir + red)
        logging.info('NDVI index calculated.')

        return ndvi