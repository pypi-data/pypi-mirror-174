import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, r2_score, mean_absolute_error, mean_squared_error


class ModelData:
    

    def __init__(self, train_data: pd.DataFrame, target_data: pd.DataFrame, test_size: float=0.2):
        '''
        Parameters
        ----------
        train_data: pandas.DataFrame
            Training data. All the exogenous variables.
        target_data: pandas.DataFrame
            Target data. The endogenous variable.
        test_size: float    
            Size of the test data. Default is 0.2.
        '''

        self.train_data = train_data
        self.target_data = target_data
        self.test_size = test_size

        self.xtr, self.xte, self.ytr, self.yte = train_test_split(self.train_data.values, self.target_data.values, 
        test_size=self.test_size, stratify=None if self._is_target_variable_numeric() else self.target_data)


    def _is_target_variable_numeric(self) -> bool:
        return is_numeric_dtype(self.target_data)


    @staticmethod
    def _create_regression_models_pool() -> dict:

        return {
            'rf': RandomForestRegressor()
        }
    

    @staticmethod
    def _create_classification_models_pool() -> dict:
        
        return  {
            'logistic': LogisticRegression(),
            'rf': RandomForestClassifier()
        }


    def create_models_pool(self) -> dict:
        '''
        Function to create a pool of models. It will create a pool of regression models if the target variable is numeric
        and a pool of classification models if the target variable is categorical.

        Returns
        -------
        models_pool: dict
            Dictionary with the models.
        '''
        if self._is_target_variable_numeric():
            return self._create_regression_models_pool()
        else:
            return self._create_classification_models_pool()
            

    def train_algorithm_and_return_predictions(self, model, xtr_scaled: np.ndarray=None, xte_scaled: np.ndarray=None) -> np.ndarray:
        '''
        Function to fit a model and return the predictions.
        Parameters
        ----------
        model: sklearn model
            Model to fit.
        xtr_scaled: numpy.ndarray
            Scaled training data. If None, the unscaled training data will be used.
        xte_scaled: numpy.ndarray
            Scaled test data. If None, the unscaled test data will be used.

        Returns
        -------
        predictions: numpy.ndarray
            Predictions of the model.
        '''
        if xtr_scaled is None:
            xtr_scaled = self.xtr
        if xte_scaled is None:
            xte_scaled = self.xte

        model.fit(xtr_scaled, self.ytr)
        return model.predict(xte_scaled)
    

    def _evaluate_regression_model(self, model, predictions: np.ndarray, cv: int) -> dict:
        '''
        Function to evaluate the performance of a regression model.
        Parameters
        ---------- 
        model: sklearn model
            Model to evaluate.
        predictions: numpy.ndarray
            Predictions of the model.
        
        Returns
        -------
        A dictionary that includes all of the following metrics.
        train_score: float
            Score of the model on the training data.
        test_r2_score: float
            R2 score of the model on the test data.
        test_mse_score: float
            Mean squared error of the model on the test data.
        test_mae_score: float
            Mean absolute error of the model on the test data.
        '''
        cross_score = cross_val_score(model, self.xtr, self.ytr, cv=cv, scoring='r2')
        train_score = np.mean(cross_score)
        test_r2_score = r2_score(self.yte, predictions)
        test_mse_score = mean_squared_error(self.yte, predictions)
        test_mae_score = mean_absolute_error(self.yte, predictions)

        return {'train_r2': train_score, 'test_r2': test_r2_score, 
                'test_mse': test_mse_score, 'test_mae': test_mae_score}
    

    def _evaluate_classification_model(self, model, predictions: np.ndarray, cv: int) -> dict:
        '''
        Function to evaluate the performance of a classification model.
        Parameters
        ----------
        model: sklearn model
            Model to evaluate.
        predictions: numpy.ndarray
            Predictions of the model.
        
        Returns
        -------
        A dict that includes all of the following metrics.
        train_score: float
            Score of the model on the training data.
        test_accuracy_score: float
            Accuracy score of the model on the test data.
        test_roc_auc_score: float
            ROC AUC score of the model on the test data.
    
        '''

        cross_score = cross_val_score(model, self.xtr, self.ytr, cv=cv, scoring='roc_auc')
        train_score = np.mean(cross_score)
        test_accuracy_score = accuracy_score(self.yte, predictions)
        test_roc_auc_score = roc_auc_score(self.yte, predictions)

        return {'train_auc': train_score, 'test_acc': test_accuracy_score, 'test_auc': test_roc_auc_score}


    def evaluate_model(self, model, predictions: np.ndarray, cv: int) -> dict:
        '''
        Function to evaluate the performance of a model. It will return different metrics depending on the type of the
        target variable. If the target variable is numeric, it will return the R2 score, the mean squared error and the
        mean absolute error. If the target variable is categorical, it will return the accuracy score and the ROC AUC
        score.
        '''
        if self._is_target_variable_numeric():
            return self._evaluate_regression_model(model=model, predictions=predictions, cv=cv)
        else:
            return self._evaluate_classification_model(model=model, predictions=predictions, cv=cv)
