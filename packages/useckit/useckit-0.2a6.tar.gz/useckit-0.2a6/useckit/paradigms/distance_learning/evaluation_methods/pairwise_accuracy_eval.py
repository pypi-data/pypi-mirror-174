from typing import Callable, Tuple

import numpy as np

from .distance_evaluation_method_base import DistanceBaseEvaluationMethod
from ..prediction_models.distance_prediction_model_base import DistanceBasePredictionModel
from ....util.data import Dataset
from ....util.plotting import plot_roc_curve
from ....util.utils import default_make_pairs


class PairwiseAccuracy(DistanceBaseEvaluationMethod):

    def __init__(self, output_folder_name: str = "evaluation_pairwise"):
        super().__init__(output_folder_name)

    def evaluate(self, dataset: Dataset, prediction_model: DistanceBasePredictionModel,
                 pair_function: Callable[[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]] = default_make_pairs):
        pairs_test, labels_test = pair_function(dataset.testset_data, dataset.testset_labels)

        # split test pairs
        x_test_1 = pairs_test[:, 0]  # x_test_1.shape = (20000, 28, 28)
        x_test_2 = pairs_test[:, 1]

        predictions = prediction_model.predict(x_test_1, x_test_2)
        plot_roc_curve(labels_test, predictions, self.output_folder_name)
