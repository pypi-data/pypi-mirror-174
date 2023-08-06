from abc import abstractmethod

from ..._paradigm_base import PredictionModelBase


class DistanceBasePredictionModel(PredictionModelBase):

    def __init__(self, output_dir: str = "model_out", verbose: bool = False):
        super().__init__(output_dir=output_dir, verbose=verbose)

    @abstractmethod
    def fit(self, x_train_1, x_train_2, y_train, x_val_1, x_val_2, y_val, input_shape):
        pass

    @abstractmethod
    def predict(self, x_test_1, x_test_2):
        pass
