from typing import Callable, Tuple

import numpy as np

from useckit.util.data import Dataset
from .evaluation_methods.distance_evaluation_method_base import DistanceBaseEvaluationMethod
from .evaluation_methods.pairwise_accuracy_eval import PairwiseAccuracy
from .prediction_models.distance_prediction_model_base import DistanceBasePredictionModel
from .prediction_models.keras_prediction_model import KerasPredictionModel
from .._paradigm_base import ParadigmBase
from ...util.utils import default_make_pairs


class SiameseParadigm(ParadigmBase):

    def __init__(self, name: str = None,
                 output_dir: str = "_useckit_out",
                 prediction_model: DistanceBasePredictionModel = KerasPredictionModel(),
                 evaluation_methods: [DistanceBaseEvaluationMethod] = None,
                 pair_function: Callable[[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]] = default_make_pairs,
                 verbose: int = 0,
                 seed=42):
        super().__init__(prediction_model=prediction_model, name=name, output_dir=output_dir)
        if evaluation_methods is None:
            evaluation_methods = [PairwiseAccuracy()]
        self._set_evaluation_methods(evaluation_methods)
        self.verbose = verbose
        self.seed = seed
        self.pair_function = pair_function

    def evaluate(self, dataset: Dataset):
        assert isinstance(self.prediction_model, DistanceBasePredictionModel)
        # make train pairs
        pairs_train, labels_train = self.pair_function(dataset.trainset_data, dataset.trainset_labels)

        # make validation pairs
        pairs_val, labels_val = self.pair_function(dataset.validationset_data, dataset.validationset_labels)

        # split trainig pairs
        x_train_1 = pairs_train[:, 0]
        x_train_2 = pairs_train[:, 1]

        # split validation pairs
        x_val_1 = pairs_val[:, 0]
        x_val_2 = pairs_val[:, 1]

        self.prediction_model.fit(x_train_1, x_train_2, labels_train, x_val_1, x_val_2, labels_val, x_train_1.shape[1:])

        # evaluate the model
        for eval_method in self.evalution_methods:
            eval_method.evaluate(dataset, self.prediction_model, self.pair_function)
