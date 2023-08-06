import os
import time
from typing import Callable

import matplotlib.pyplot as plt
import tensorflow.keras as keras

from .keras_model_descriptions import tower_conv_2d, merge_constractive
from .distance_prediction_model_base import DistanceBasePredictionModel
from ....util.plotting import plot_history_df


# visualize the results
def plt_metrics(history, output_directory):
    """Plots all metrics from 'history'.

    Arguments:
        history: history attribute of History object returned from Model.fit.

    Returns:
        None.
    """
    keys = history.history.keys()
    for key in keys:
        if "val_" not in str(key):
            plt.plot(history.history[key])
            if "val_" + key in keys:
                plt.plot(history.history["val_" + key])
                plt.legend(["train", "validation"], loc="upper left")
            plt.title(f"{key}-over epochs")
            plt.ylabel(key)
            plt.xlabel("epoch")
            plt.tight_layout()
            plt.savefig(os.path.join(output_directory, f"{key}.pdf"))
            plt.clf()


class KerasPredictionModel(DistanceBasePredictionModel):

    def __init__(self,
                 tower_model_description: Callable[[keras.layers.Input], keras.models.Model]
                 = tower_conv_2d,
                 merge_model_description: Callable[[keras.models.Model, keras.layers.Input,
                                                    keras.layers.Input, keras.models.Model],
                                                   keras.models.Model]
                 = merge_constractive,
                 output_dir: str = "keras_pred_model_out",
                 verbose=False,
                 nb_epochs=10,
                 batch_size: Callable[[int], int] = 16):
        super().__init__(output_dir=output_dir, verbose=verbose)
        self.tower_model_description = tower_model_description
        self.merge_model_description = merge_model_description
        self.nb_epochs = 2000 if nb_epochs is None else nb_epochs
        self.verbose = verbose
        assert isinstance(batch_size, Callable) or isinstance(batch_size, int)
        self.batch_size = batch_size
        self.callbacks = []

    def build_model(self, input_shape):
        input_layer = keras.layers.Input(input_shape)
        tower_1 = self.tower_model_description(input_layer)
        tower_2 = self.tower_model_description(input_layer)
        input_1 = keras.layers.Input(input_shape)
        input_2 = keras.layers.Input(input_shape)
        merge = self.merge_model_description(tower_1, input_1, tower_2, input_2)
        model_checkpoint = keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(self.output_directory, 'best_model.hdf5'),
            monitor='loss',
            save_best_only=True,
            save_weights_only=True)
        self.callbacks = [model_checkpoint]
        return merge

    def fit(self, x_train_1, x_train_2, y_train, x_val_1, x_val_2, y_val, input_shape):
        model = self.build_model(input_shape)
        if self.verbose:
            model.summary()

        model.save_weights(os.path.join(self.output_directory, 'model_init.hdf5'))

        if self.batch_size is Callable:
            batch_size = self.batch_size(x_train_1.shape[0])
        else:
            batch_size = self.batch_size

        start_time = time.time()

        hist = model.fit([x_train_1, x_train_2], y_train, batch_size=batch_size, epochs=self.nb_epochs,
                         verbose=self.verbose, validation_data=([x_train_1, x_train_2], y_val),
                         callbacks=self.callbacks)

        duration = time.time() - start_time
        if self.verbose:
            plot_history_df(hist, self.output_directory)
            plt_metrics(hist, self.output_directory)
            print(f"Siamese model fitted in {round(duration, 2)} seconds!")

        model.save_weights(os.path.join(self.output_directory, 'last_model.hdf5'))

        keras.backend.clear_session()

    def predict(self, x_test_1, x_test_2):
        model_path = os.path.join(self.output_directory, 'best_model.hdf5')
        model = self.build_model(x_test_1.shape[1:])
        model.load_weights(model_path)
        y_pred = model.predict([x_test_1, x_test_2])
        return y_pred
