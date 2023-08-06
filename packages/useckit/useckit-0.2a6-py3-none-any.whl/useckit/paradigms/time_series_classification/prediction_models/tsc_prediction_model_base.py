from abc import ABC, abstractmethod

from ..._paradigm_base import PredictionModelBase


class TSCBasePredictionModel(PredictionModelBase):

    def __init__(self, output_dir: str = "tsc_model_out", verbose: bool = False):
        super().__init__(output_dir, verbose)

    @abstractmethod
    def fit(self, x_train, y_train, x_val, y_val, y_true, input_shape, nb_classes):
        pass

    @abstractmethod
    def predict(self, x_test, y_true, x_train, y_train, y_test, return_df_metrics=True):
        pass

