# Python code to demonstrate working of unittest
import unittest
import sys

sys.path.insert(0, '../IndexCalculator')
import image_tools as it
import lib_image as lb
import index_operations as io
  
class TestImageMethods(unittest.TestCase):
    
    def setUp(self):
        pass
  
    def test_open_image(self):
        dataset = it.ImageTools().open_image('test/image.tif')
        self.assertEqual( dataset['image'].count, 8)
        self.assertEqual( dataset['image'].width, 171)
        self.assertEqual( dataset['image'].height, 202)
  
    def test_load_band(self):  
        dataset = it.ImageTools().open_image('test/image.tif')
        band1 = it.ImageTools().load_band(dataset['image'], 6)
        band2 = it.ImageTools().load_band(dataset['image'], 8)      
        self.assertEqual(band1.shape, band2.shape)
  
    def test_update_pixel_value(self): 
        dataset = it.ImageTools().open_image('test/image.tif')
        band1 = it.ImageTools().load_band(dataset['image'], 6)
        band2 = it.ImageTools().load_band(dataset['image'], 8)
        index = io.IndexesMethods().ndvi(band2, band1)       
        image_updated = lb.LibImage().update_pixel_value(None,index)

        self.assertEqual(image_updated.max(), 255)
        self.assertEqual(image_updated.min(), 0)

    def test_reprojection(self): 
        dataset = it.ImageTools().open_image('test/image.tif')
        band1 = it.ImageTools().load_band(dataset['image'], 6)
        band2 = it.ImageTools().load_band(dataset['image'], 8)
        index = io.IndexesMethods().ndvi(band2, band1)      
        image_updated = lb.LibImage().update_pixel_value(None,index)
        image_reprojected, metadata_reprojected = lb.LibImage().reprojection(None,dataset,image_updated)

        self.assertEqual(metadata_reprojected['crs'], 'EPSG:4326')
  
if __name__ == '__main__':
    unittest.main()