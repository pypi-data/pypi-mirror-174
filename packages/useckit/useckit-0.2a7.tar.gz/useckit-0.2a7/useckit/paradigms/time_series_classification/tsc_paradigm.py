import os
import random
import time

import numpy as np
import pandas as pd

from .evaluation_methods.legacy_identification import IdentificationOnly
from .evaluation_methods.tsc_evaluation_method_base import TSCBaseEvaluationMethod
from .prediction_models.keras_prediction_model import KerasPredictionModel
from .prediction_models.tsc_prediction_model_base import TSCBasePredictionModel
from .._paradigm_base import ParadigmBase
from ...util.data import Dataset
from ...util.plotting import plot_history_df
from ...util.utils import create_window_slices


class TSCParadigm(ParadigmBase):

    def __init__(self, name: str = None,
                 output_dir: str = "_useckit_out",
                 prediction_model: TSCBasePredictionModel = KerasPredictionModel(),
                 evaluation_methods: [TSCBaseEvaluationMethod] = None,
                 verbose: bool = False,
                 enable_window_slicing=False,
                 window_stride=None,
                 window_size=None,
                 seed=42,
                 kcrossvalidation_k=None,
                 disable_normalization_check=False,
                 shuffle_window_slices=True,
                 class_weights=None
                 ):
        super().__init__(prediction_model=prediction_model, name=name, output_dir=output_dir)
        if evaluation_methods is None:
            evaluation_methods = [IdentificationOnly()]
        self._set_evaluation_methods(evaluation_methods)
        self.complete_history_df = None
        self.enable_window_slicing = enable_window_slicing
        self.window_stride = window_stride
        self.window_size = window_size
        self.shuffle_window_slices = shuffle_window_slices
        self.disable_normalization_check = disable_normalization_check
        self.verbose = verbose
        self.seed = seed
        self.prediction_model = prediction_model

        if kcrossvalidation_k is not None:
            raise NotImplementedError("kcrossvalidation_k is not implemented yet.")

        if class_weights is not None:
            assert isinstance(class_weights, dict), 'class_weights must be a dict. See: https://bit.ly/3ljOI9c'
        self.class_weights = class_weights

    def evaluate(self, dataset: Dataset):
        # sanitize parameters
        x_train, x_val = dataset.trainset_data, dataset.validationset_data
        y_train, y_val, _ = dataset.view_one_hot_encoded_labels()

        if self.enable_window_slicing:
            if self.window_stride is None:
                raise TypeError('window_stride must not be None if window slicing is used.')

            if self.window_size is None:
                raise TypeError('window_size must not be None if window slicing is used.')

            x_train, y_train, _ = create_window_slices(dataset.trainset_data,
                                                       y_train,
                                                       self.window_stride,
                                                       self.window_size,
                                                       shuffle=self.shuffle_window_slices)
            x_val, y_val, _ = create_window_slices(dataset.validationset_data,
                                                   y_val,
                                                   self.window_stride,
                                                   self.window_size,
                                                   shuffle=self.shuffle_window_slices)

        start_time = time.time()
        model = self.prediction_model

        if self.verbose > 0:
            print('++ Fitting model:', str(type(model)))
        self.set_seed()
        model.fit(x_train,
                  y_train,
                  x_val,
                  y_val,
                  np.argmax(y_val, axis=1),
                  x_train.shape[1:],
                  dataset.amount_classes())
        if self.verbose > 0:
            self._plot_history(os.path.join(self.output_dir, 'history.csv'), type(model).__name__)

        if self.verbose > 0:
            print('++ TSC-Model', str(type(model)), 'finished fit().')
        self.set_seed()

        for eval_method in self.evalution_methods:
            eval_method.evaluate(dataset, model)

        if self.verbose > 0:
            print('++ TSC-Model', str(type(model)), 'finished predictions [do_cm()].')
            print(f"{self.name} took", round(time.time() - start_time, 4) / 3600, 'hours')

    def _plot_history(self, path, modelname):
        try:
            hist_df = pd.read_csv(path, dtype=np.float64)
            hist_df['epoch'] = hist_df.index
            hist_df['modelname'] = modelname

            plot_history_df(hist_df, path, name=modelname, acc='accuracy')
        except FileNotFoundError as e:
            print(e)

    def set_seed(self):
        import tensorflow as tf
        tf.keras.backend.clear_session()
        if self.seed is not None:
            tf.random.set_seed(self.seed)
            tf.random.set_seed(self.seed)
            random.seed(self.seed)
            np.random.seed(self.seed)
            os.environ['PYTHONHASHSEED'] = str(self.seed)
            os.environ['TF_CUDNN_DETERMINISTIC'] = '1'
