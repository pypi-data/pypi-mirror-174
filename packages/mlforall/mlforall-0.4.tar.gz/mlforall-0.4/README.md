# MLForAll: Easy ML projects from scratch
[![PyPI Latest Release](https://img.shields.io/pypi/v/mlforall.svg)](https://pypi.org/project/mlforall/)
[![Package Status](https://img.shields.io/pypi/status/mlforall.svg)](https://pypi.org/project/mlforall/)
[![License](https://img.shields.io/pypi/l/mlforall.svg)](https://github.com/mlforall-dev/mlforall/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Description
**mlforall** is an open-source library aimed to developers that are beginners in the data analysis area but want to build powerful machine learning projects from the very beginning. The package offers a reliable, easy to use and well documented set of functions that drive the user through the most common steps of any machine learning projects, from data reading to model testing.

## Main features
These are some of the functionalities that mlforall offers:
1. File extension asbtraction when reading data (only supported for `.csv`, `.txt`, `.xls`, `.xlsx`, `.parquet` and `.npy`)
2. Automatic handling of non-numeric features and missing values.
3. A pool with almost all the data-scaling methods available and the most common ML models.
4. Automatic model evaluation and reporting.

## Usage options
The **mlforall** package can be used by command line interface or with Interactive Python Notebooks (`.ipynb`). An example of the first usage method is the following:

```sh
# MLForAll usage through command line
python -m mlforall --kwargs
```
With this option, the library will execute the full ML pipeline, from data reading to model testing. The available keyword arguments are:
- --data_path: **Mandatory**. *str*.
  - The absolute or relative route to the data for which the ML pipelin wants to be built.
- --target_var: **Mandatory**. *str* or *int*.
  - The name or the position of the target column in the original data.
- --test_size: **Optional**. *float*
  - Proportion of the data that wants to be kept as test. The defualt is 0.2.
- --cv: **Optional**. *int*
  - The number of k-folds that will be performed when evaluating the model. The deault is 5.
- --path_to_save_metrics: **Optional**. *str*
  - The absolute or relative path to save the final metrics of the model. It must be a file with the `.csv` extension. If not provided, the metrics will be printed in the console but not saved.


As mentioned, usage from `.ipynb` files is also possible. As of version 0.1, the way to use this module from `.ipynb` files is by importing the submodules and using their methods separatedly. To import the different modules the following code snippet can be used:

```sh
# MLForAll usage through .ipynb files
from mlforall import DataReader
from mlforall import DataScaler
from mlforall import DataModeler


data_reader = DataReader.ReadData(*args, **kwargs)
data_scaler = DataScaler.ScaleData(*args, **kwargs)
data_modeler = DataModeler.ModelData(*args, **kwargs)
```

```sh
# or
import mlforall as ml

data_reader = ml.DataReader.ReadData(*args, **kwargs)
data_scaler = ml.DataScaler.ScaleData(*args, **kwargs)
data_modeler = ml.DataModeler.ModelData(*args, **kwargs)
```


## Dependencies
- [Numpy. It offers comprehensive mathematical functions, random number generators, linear algebra routines, Fourier transforms, and more](https://numpy.org)
- [Pandas. A fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
built on top of the Python programming language](https://pandas.pydata.org)
- [Openpyxl. A python library to read/write excel files](https://openpyxl.readthedocs.io/en/stable/) 
- [Scikit-learn. accesible, reusable, simple and efficient tools for predictive data analysis](https://scikit-learn.org/stable/)

## Where to get it
The source code is currently hosted on GitHub at:
[https://github.com/UnaiTorrecilla/MLForAll](https://github.com/UnaiTorrecilla/MLForAll)

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/mlforall)


```sh
# PyPI
pip install mlforall
```
