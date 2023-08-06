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
import package.index_operations as io
import package.image_tools as it
import package.lib_image as li
from package import parser

def main():
       index_method = io.IndexesMethods()
       image_tools = it.ImageTools()
       lib_image = li.LibImage()
       args = parser.Parser().create_parser()

       logging.basicConfig(filename ='app.log',
                     level = logging.INFO,
                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

       image = image_tools.open_image(args.image)
       band_red = image_tools.load_band(image['image'], args.red)
       band_nir = image_tools.load_band(image['image'], args.nir)

       index_calculated = index_method.ndvi(band_nir, band_red)
       image_updated = lib_image.update_pixel_value(args.threshold, index_calculated)

       destination, metadata_dict = lib_image.reprojection(args.crs, image, image_updated)

       image_tools.save_image(destination, image['meta'], metadata_dict, args.export)

if __name__ == "__main__":
	main()