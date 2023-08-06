import os
import time
from typing import Callable

import numpy as np
import tensorflow as tf
import tensorflow.keras as keras

from .tsc_prediction_model_base import TSCBasePredictionModel
from useckit.paradigms.time_series_classification.prediction_models.keras_model_descriptions import fawaz_cnn_padding_valid
from ....util.utils import calculate_metrics, save_logs, save_test_duration


class KerasPredictionModel(TSCBasePredictionModel):

    def __init__(self,
                 model_description: Callable[[keras.layers.Input, int], tuple[keras.models.Model, list[Callable]]]
                 = fawaz_cnn_padding_valid,
                 verbose=False,
                 nb_epochs=2000,
                 class_weights=None,
                 batch_size: Callable[[int], int] = 16):
        super().__init__()
        self.model_description = model_description
        self.nb_epochs = 2000 if nb_epochs is None else nb_epochs
        self.class_weights = class_weights
        self.verbose = verbose
        assert isinstance(batch_size, Callable) or isinstance(batch_size, int)
        self.batch_size = batch_size
        self.callbacks = []

    def build_model(self, input_shape, nb_classes):
        input_layer = keras.layers.Input(input_shape)
        model, callbacks = self.model_description(input_layer, nb_classes)
        model_checkpoint = keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(self.output_directory, 'best_model.hdf5'),
            monitor='loss',
            save_best_only=True)
        self.callbacks = [model_checkpoint]
        self.callbacks += callbacks
        return model

    def fit(self, x_train, y_train, x_val, y_val, y_true, input_shape, nb_classes):
        if not tf.test.is_gpu_available:
            print('error')
            exit()

        model = self.build_model(input_shape, nb_classes)
        if self.verbose:
            model.summary()

        model.save_weights(os.path.join(self.output_directory, 'model_init.hdf5'))

        if self.batch_size is Callable:
            batch_size = self.batch_size(x_train.shape[0])
        else:
            batch_size = self.batch_size

        start_time = time.time()

        hist = model.fit(x_train, y_train, batch_size=batch_size, epochs=self.nb_epochs,
                         class_weight=self.class_weights,
                         verbose=self.verbose, validation_data=(x_val, y_val), callbacks=self.callbacks)

        duration = time.time() - start_time

        model.save(os.path.join(self.output_directory, 'last_model.hdf5'))

        model = keras.models.load_model(os.path.join(self.output_directory, 'best_model.hdf5'))

        y_pred = model.predict(x_val)

        # convert the predicted from binary to integer
        y_pred = np.argmax(y_pred, axis=1)

        save_logs(self.output_directory, hist, y_pred, y_true, duration, lr=False)

        keras.backend.clear_session()

    def predict(self, x_test, y_true, x_train, y_train, y_test, return_df_metrics=True):
        start_time = time.time()
        model_path = os.path.join(self.output_directory, 'best_model.hdf5')
        model = keras.models.load_model(model_path)
        y_pred = model.predict(x_test)
        if return_df_metrics:
            y_pred = np.argmax(y_pred, axis=1)
            df_metrics = calculate_metrics(y_true, y_pred, 0.0)
            return df_metrics
        else:
            test_duration = time.time() - start_time
            try:
                save_test_duration(os.path.join(self.output_directory, 'test_duration.csv'), test_duration)
            except PermissionError:
                print(
                    'PermissionError: Could not save test_duration.csv in Classifier_Keras due to lack of permission.')
            return np.argmax(y_pred, axis=1)
