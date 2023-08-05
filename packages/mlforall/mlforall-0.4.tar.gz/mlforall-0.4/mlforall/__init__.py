#__init__.py
from mlforall.DataReader import ReadData
from mlforall.DataScaler import ScaleData
from mlforall.DataModeler import ModelData

__all__ = [
    'DataReader',
    'DataScaler',
    'DataModeler'
]

__version__ = '0.4'

__doc__ = '''

## Description
**mlforall** is an open-source library aimed to developers that are beginners in the data analysis area but want to build powerful machine learning projects from the very beginning. The package offers a reliable, easy to use and well documented set of functions that drive the user through the most common steps of any machine learning projects, from data reading to model testing.

## Main features
These are some of the functionalities that mlforall offers:
1. File extension asbtraction when reading data (only supported for `.csv`, `.txt`, `.xlsx`, `.xlsx`, `.parquet` and `.npy`)
2. Automatic handling of non-numeric features and missing values.
3. A pool with almost all the data-scaling methods available and the most common ML models.
4. Automatic model evaluation and reporting.

'''

