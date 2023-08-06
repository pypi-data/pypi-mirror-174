import os
import sys
import unittest

import numpy as np

from useckit.paradigms.anomaly_detection.anomaly_paradigm import AnomalyParadigm
from useckit.paradigms.distance_learning.distance_paradigm import SiameseParadigm
from useckit.paradigms.time_series_classification.prediction_models.inception import Classifier_INCEPTION
from useckit.paradigms.time_series_classification.prediction_models.keras_model_descriptions import *
from useckit.paradigms.time_series_classification.prediction_models.keras_prediction_model import KerasPredictionModel
from useckit.paradigms.time_series_classification.prediction_models.mcdcnn import Classifier_MCDCNN
from useckit.paradigms.time_series_classification.prediction_models.mcnn import Classifier_MCNN
from useckit.paradigms.time_series_classification.prediction_models.tlenet import Classifier_TLENET
from useckit.paradigms.time_series_classification.prediction_models.twiesn import Classifier_TWIESN
from useckit.paradigms.time_series_classification.tsc_paradigm import TSCParadigm
from useckit.util.data import Dataset

sys.setrecursionlimit(10000)
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


class TestUseckit(unittest.TestCase):

    @staticmethod
    def make_some_intelligent_noise(labels: int = 4, shape: tuple = (100, 100, 100), noisiness: float = 0.1):
        biases = np.array([i / labels for i in range(labels)]) + (1 / (2 * labels))
        x = []
        y = []
        shape = list(shape)
        shape[0] = int(shape[0] / labels)
        i = 0
        for b in biases:
            x.extend(np.random.normal(b, noisiness, shape))
            y.extend(np.ones((shape[0],)) * i)
            i += 1
        x = np.array(x)
        y = np.array(y)
        x = np.clip(x, -1, 1)
        return x, y

    def test_tsc(self):
        x_train, y_train = self.make_some_intelligent_noise()
        x_val, y_val = self.make_some_intelligent_noise()
        x_test, y_test = self.make_some_intelligent_noise()
        data = Dataset(x_train, y_train, x_val, y_val, x_test, y_test)

        # 1
        keras_mlp = TSCParadigm(
            prediction_model=KerasPredictionModel(verbose=True, nb_epochs=10, model_description=fawaz_mlp),
            verbose=True)
        keras_mlp.evaluate(data)

        # 2
        keras_fcn = TSCParadigm(
            prediction_model=KerasPredictionModel(verbose=True, nb_epochs=10, model_description=fawaz_fcn),
            verbose=True)
        keras_fcn.evaluate(data)

        # 3
        keras_resnet = TSCParadigm(
            prediction_model=KerasPredictionModel(verbose=True, nb_epochs=10, model_description=fawaz_resnet),
            verbose=True)
        keras_resnet.evaluate(data)

        # 4
        keras_encoder = TSCParadigm(
            prediction_model=KerasPredictionModel(verbose=True, nb_epochs=10, model_description=fawaz_encoder),
            verbose=True)
        keras_encoder.evaluate(data)

        # 5
        keras_cnn_valid = TSCParadigm(
            prediction_model=KerasPredictionModel(verbose=True, nb_epochs=10,
                                                  model_description=fawaz_cnn_padding_valid),
            verbose=True)
        keras_cnn_valid.evaluate(data)

        # 6
        keras_cnn_same = TSCParadigm(
            prediction_model=KerasPredictionModel(verbose=True, nb_epochs=10, model_description=fawaz_cnn_padding_same),
            verbose=True)
        keras_cnn_same.evaluate(data)

        # 7
        keras_cnn_same = TSCParadigm(
            prediction_model=KerasPredictionModel(verbose=True, nb_epochs=10, model_description=fawaz_cnn_padding_same),
            verbose=True)
        keras_cnn_same.evaluate(data)

        # 8
        mcnn = TSCParadigm(
            prediction_model=Classifier_MCNN(nb_classes=data.amount_classes(), verbose=True, nb_epochs=10),
            verbose=True)
        mcnn.evaluate(data)

        # 9
        tlenet = TSCParadigm(
            prediction_model=Classifier_TLENET(verbose=True, nb_epochs=10),
            verbose=True)
        tlenet.evaluate(data)

        # 10
        twiesen = TSCParadigm(
            prediction_model=Classifier_TWIESN(),
            verbose=True)
        twiesen.evaluate(data)

        # 11
        inception = TSCParadigm(
            prediction_model=Classifier_INCEPTION(verbose=True, nb_epochs=10),
            verbose=True)
        inception.evaluate(data)

        # 12
        mcdcnn = TSCParadigm(
            prediction_model=Classifier_MCDCNN(verbose=True, nb_epochs=10),
            verbose=True)
        mcdcnn.evaluate(data)

    def test_siamese(self):
        x_train, y_train = self.make_some_intelligent_noise(shape=(100, 100, 100, 3))
        x_val, y_val = self.make_some_intelligent_noise(shape=(100, 100, 100, 3))
        x_test, y_test = self.make_some_intelligent_noise(shape=(100, 100, 100, 3))
        data = Dataset(x_train, y_train, x_val, y_val, x_test, y_test)

        siamese = SiameseParadigm(verbose=True)
        siamese.evaluate(data)

    def test_encoders(self):
        x_train, y_train = self.make_some_intelligent_noise(shape=(10, 10))
        x_val, y_val = self.make_some_intelligent_noise(shape=(10, 10))
        x_test, y_test = self.make_some_intelligent_noise(labels=6, shape=(10, 10))
        data = Dataset(x_train, y_train, x_val, y_val, x_test, y_test)

        encoder = AnomalyParadigm(verbose=True)
        encoder.evaluate(data)


if __name__ == '__main__':
    unittest.main()
