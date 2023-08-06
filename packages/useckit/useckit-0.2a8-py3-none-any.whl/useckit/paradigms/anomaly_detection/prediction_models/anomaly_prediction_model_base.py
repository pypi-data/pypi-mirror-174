from abc import abstractmethod

from ..._paradigm_base import PredictionModelBase


class AnomalyBasePredictionModel(PredictionModelBase):

    def __init__(self, output_dir: str = "model_out", verbose: bool = False):
        super().__init__(output_dir, verbose)

    @abstractmethod
    def fit(self, x_train, y_train, x_val, y_val, input_shape, nb_classes):
        pass

    @abstractmethod
    def predict(self, x_test):
        pass
