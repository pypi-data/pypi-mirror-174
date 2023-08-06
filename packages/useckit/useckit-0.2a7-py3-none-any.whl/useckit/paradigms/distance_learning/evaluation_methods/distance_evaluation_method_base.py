from abc import abstractmethod

from ..prediction_models.distance_prediction_model_base import DistanceBasePredictionModel
from ..._paradigm_base import EvaluationMethodBase
from ....util.data import Dataset


class DistanceBaseEvaluationMethod(EvaluationMethodBase):

    @abstractmethod
    def evaluate(self, dataset: Dataset, prediction_model: DistanceBasePredictionModel):
        pass
