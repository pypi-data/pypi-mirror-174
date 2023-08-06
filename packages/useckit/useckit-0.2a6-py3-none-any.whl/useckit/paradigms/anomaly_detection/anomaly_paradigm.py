from .evaluation_methods.anomaly_evaluation_method_base import AnomalyBaseEvaluationMethod
from .evaluation_methods.identification_with_reject_individual_thresholding import \
    IdentificationRejectIndividualThreshold
from .prediction_models.anomaly_prediction_model_base import AnomalyBasePredictionModel
from .prediction_models.keras_prediction_model import KerasPredictionModel
from .._paradigm_base import ParadigmBase
from ...util.data import Dataset


class AnomalyParadigm(ParadigmBase):

    def __init__(self, name: str = None,
                 output_dir: str = "_useckit_out",
                 prediction_model: AnomalyBasePredictionModel = KerasPredictionModel(),
                 evaluation_methods: [AnomalyBaseEvaluationMethod] = None,
                 verbose: int = 0,
                 seed=42,
                 ):
        super().__init__(prediction_model=prediction_model, name=name, output_dir=output_dir)
        if evaluation_methods is None:
            evaluation_methods = [IdentificationRejectIndividualThreshold()]
        self._set_evaluation_methods(evaluation_methods)

        self.verbose = verbose
        self.seed = seed
        self.prediction_model = prediction_model

    def evaluate(self, dataset: Dataset):

        x_train, y_train = dataset.trainset_data, dataset.trainset_labels
        x_val, y_val = dataset.validationset_data, dataset.validationset_labels
        input_shape = x_train.shape[1:]
        nb_classes = dataset.train_classes()

        self.prediction_model.fit(x_train, y_train, x_val, y_val, input_shape, nb_classes)

        for eval_method in self.evalution_methods:
            eval_method.evaluate(dataset, self.prediction_model)
6