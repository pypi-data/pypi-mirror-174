from setuptools import setup, find_packages

VERSION = '0.1' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="bearing_new_1", 
        version=VERSION,
        author="Supriya",
        author_email="<supriyasuhas058@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),

       install_requires=['pandas','numpy','matplotlib','paho-mqtt','numpy','pandas','scipy','scikit-learn','matplotlib'

                        ],


        # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        )