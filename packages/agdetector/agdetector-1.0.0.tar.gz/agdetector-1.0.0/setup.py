"""
/***************************************************************************
                              Agricultural Field Detector
                             --------------------
        created              : 2022-10-28
        copyright            : (C) 2022 by Jhon Galindo
        email                : jhonalex.ue@gmail.com
 ***************************************************************************/
"""
from setuptools import setup, find_namespace_packages
  
long_description = 'agricultural_field_detector.'
  
setup(
        name ='agdetector',
        version ='1.0.0',
        author ='Jhon Galindo',
        author_email ='jhonalex.ue@gmail.com',
        url ='https://jhonalex06.github.io/Jhon_Galindo/',
        description ='agricultural_field_detector',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        packages = find_namespace_packages(),
        entry_points ={
            'console_scripts': [
                'agdetector = package.agricultural_field_detector:main',
            ]
        },
        classifiers =[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        keywords ='agricultural field detector python package jhonalex06',
        install_requires = ["affine==2.3.1","attrs==22.1.0","certifi==2022.9.24", 
                            "click==8.1.3", "click-plugins==1.1.1", "cligj==0.7.2", 
                            "numpy==1.23.4", "pyparsing==3.0.9", "rasterio==1.3.3", "snuggs==1.4.7"],
        zip_safe = False,
        include_package_data = True
)
