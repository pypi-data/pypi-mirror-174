import numpy as np

from .anomaly_prediction_model_base import AnomalyBasePredictionModel
from .keras_model_descriptions import BaseDescription, LiebersSequentialAutoencoders
from ....util.plotting import plot_history_df


class KerasPredictionModel(AnomalyBasePredictionModel):

    def __init__(self,
                 model_description: BaseDescription = LiebersSequentialAutoencoders(),
                 verbose: bool = False,
                 output_dir: str = "keras_prediction_model_out",
                 epochs=100):
        super().__init__(output_dir=output_dir, verbose=verbose)
        self.model_description = model_description
        self.epochs = epochs
        self.models = []

    def _get_mse(self, a: np.ndarray, b: np.ndarray):
        """Performs MSE calculation for a single value, returns only one value"""
        # from sklearn.metrics import mean_squared_error
        return np.sqrt(((a - b) ** 2).mean())

    def build_models(self, input_shape, nb_classes):
        result = []
        for i in range(nb_classes):
            result.append(self.model_description.build_model(input_shape))
        return result

    def fit(self, x_train, y_train, x_val, y_val, input_shape, nb_classes):
        assert nb_classes > 0
        models_built = self.build_models(input_shape, nb_classes)
        for i, model in enumerate(models_built):
            # find the elements in the training data that belong to class `i`
            # the `y_train` consists of one hot encoded arrays
            # here we apply np.argmax to get the integer-encoding per array and then compare it with i, resulting
            # in a mask of bools that we can use as an indexer for a local array `x_train` (note the missing 'self.'.).
            training_indexes = y_train == i
            x_train_model_i = x_train[training_indexes]

            print(f'++ Fitting AE {i + 1} of {nb_classes}')

            history = model.fit(
                x_train_model_i,
                x_train_model_i,
                validation_data=(x_val, y_val),
                verbose=self.verbose,
                epochs=self.epochs,
                callbacks=self.model_description.callbacks(),
            )
            if self.verbose:
                plot_history_df(history, self.output_directory)

            preds = model.predict(x_train_model_i)
            mse_list = []

            assert len(preds) == len(x_train_model_i)
            for pred, x in zip(preds, x_train_model_i):
                mse_list.append(self._get_mse(pred, x))

            # store model in internal array
            self.models.append({'model': model,
                                'history': history,
                                'training_max_mse_threshold': max(mse_list)})

    def predict(self, x_test):
        result = []
        for i, model in enumerate(self.models):
            mse_list = []
            preds = model['model'].predict(x_test)
            for pred, x in zip(preds, x_test):
                mse_list.append(self._get_mse(pred, x))
            result.append(np.array(mse_list) / model['training_max_mse_threshold'])
        return np.array(result)
