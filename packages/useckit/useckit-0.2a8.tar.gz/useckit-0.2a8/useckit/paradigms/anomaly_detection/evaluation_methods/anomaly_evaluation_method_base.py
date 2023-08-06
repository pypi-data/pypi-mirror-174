from abc import abstractmethod

from ..prediction_models.anomaly_prediction_model_base import AnomalyBasePredictionModel
from ..._paradigm_base import EvaluationMethodBase
from ....util.data import Dataset


class AnomalyBaseEvaluationMethod(EvaluationMethodBase):

    @abstractmethod
    def evaluate(self, dataset: Dataset, prediction_model: AnomalyBasePredictionModel):
        pass
