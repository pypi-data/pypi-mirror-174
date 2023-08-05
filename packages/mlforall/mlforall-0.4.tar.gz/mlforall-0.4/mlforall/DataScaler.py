from typing import Union
import pandas as pd
import numpy as np
import warnings
from sklearn.impute import SimpleImputer

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler, QuantileTransformer, PowerTransformer, Normalizer



class ScaleData:


    def __init__(self, data: pd.DataFrame, target: Union[str, int]) -> None:
        '''
        Parameters
        ----------
        data: pandas.DataFrame
            Data to scale.
        target: str or int
            Name or index of the target column.
        '''

        self.data = data
        self.target = target
        self._separate_target_and_training_data()


    def _separate_target_and_training_data(self) -> None:
        
        if isinstance(self.target, str):
            self.target = self.data.columns.get_loc(self.target)
        
        self.y = self.data.iloc[:, self.target]
        self.X = self.data.drop(self.data.columns[self.target], axis=1)

        return None
    

    def select_dtypes(self) -> pd.DataFrame:
        
        previous_num_columns = self.X.shape[1]
        self.X = self.X.select_dtypes(include=np.number)

        new_num_columns = self.X.shape[1]
        if new_num_columns != previous_num_columns:
            warnings.warn(f'{previous_num_columns - new_num_columns} columns were removed due to not being numeric.'
                          ' In a future release the categorical variables will also be treated.')

        return None


    def clean_data(self) -> pd.DataFrame:
        imputer = SimpleImputer(strategy='median')

        warnings.warn('The data will be cleaned by replacing the missing values with the median of the column. In future releases more'
                      ' advanced cleaning methods will be implemented.')

        if self.X.shape[0] == 1:
            data_array = self.X.values.reshape(1, -1)
        elif self.X.shape[1] == 1:
            data_array = self.X.values.reshape(-1, 1)
        else:
            data_array = self.X.values

        self.X = pd.DataFrame(imputer.fit_transform(data_array), columns=self.X.columns)

        return None


    @staticmethod
    def create_scaling_methods_pool():
        '''
        This method creates a dictionary with the scaling methods available in the class.
        '''

        return {
            'standard': StandardScaler(),
            'minmax': MinMaxScaler(),
            'robust': RobustScaler(),
            'maxabs': MaxAbsScaler(),
            'quantile': QuantileTransformer(),
            'power': PowerTransformer(),
            'normalizer': Normalizer()
        }

    
    def scale_data(self, scaler: Union[StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler, 
                                    QuantileTransformer, PowerTransformer, Normalizer],
                    xtr: pd.DataFrame, xte: pd.DataFrame) -> pd.DataFrame:
        '''
        This method scales the data using the scaling method selected by the user.
        '''

        scaled_train_data = scaler.fit_transform(xtr)
        scaled_test_data = scaler.transform(xte)
        
        return scaled_train_data, scaled_test_data
