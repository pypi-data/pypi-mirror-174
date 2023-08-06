from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'Python package for forecasting baezeni data'
LONG_DESCRIPTION = 'This package is for private-use only'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="bzfin",
        version=VERSION,
        author="Marwan Musa",
        author_email="marwanmusa@baezeni.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'bz_forecast', 'bzfin', 'forecasting', 'time_series'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)