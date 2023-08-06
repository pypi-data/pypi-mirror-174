import numpy as np
from numpy import ndarray
from sklearn.preprocessing import LabelEncoder, LabelBinarizer


class Dataset:

    def __init__(self,
                 trainset_data: ndarray,
                 trainset_labels: ndarray,
                 validationset_data: ndarray = None,
                 validationset_labels: ndarray = None,
                 testset_data: ndarray = None,
                 testset_labels: ndarray = None,
                 normalisation_check: bool = False):

        self.trainset_data = trainset_data
        self.trainset_labels = trainset_labels
        self.testset_data = testset_data
        self.testset_labels = testset_labels
        self.validationset_data = validationset_data
        self.validationset_labels = validationset_labels

        self._label_encoder = LabelEncoder()
        self._label_encoder.fit(self._gather_labels())
        self._transform_lables()

        self._check_nan()
        if normalisation_check:
            self._normalisation_check()

        self._label_binarizer = LabelBinarizer()
        self._label_binarizer.fit(self._gather_labels())

    def view_one_hot_encoded_labels(self):
        def convert_to_onehot(labels: ndarray):
            return None if labels is None else self._label_binarizer.transform(labels)

        return convert_to_onehot(self.trainset_labels), convert_to_onehot(self.validationset_labels), \
            convert_to_onehot(self.testset_labels)

    def _check_nan(self):
        def _check_nan(array: ndarray):
            if array is not None and np.isnan(array).any():
                raise ValueError('Critical: dataset contains NaN values!')

        _check_nan(self.trainset_data)
        _check_nan(self.trainset_labels)
        _check_nan(self.testset_data)
        _check_nan(self.testset_labels)
        _check_nan(self.validationset_data)
        _check_nan(self.validationset_labels)

    def _normalisation_check(self):
        def _normalisation_check(array: ndarray):
            if array is not None:
                _max, _min = np.amax(array), np.amin(array)
                if _max > 1:
                    raise ValueError(f"Critical: dataset contains maximum value {_max}")
                if _min < -1:
                    raise ValueError(f"Critical: dataset contains minimum value {_min}")

        _normalisation_check(self.trainset_data)
        _normalisation_check(self.testset_data)
        _normalisation_check(self.validationset_data)

    def _gather_labels(self):
        labels = [self.trainset_labels]
        if self.testset_labels is not None:
            labels.append(self.testset_labels)
        if self.validationset_labels is not None:
            labels.append(self.validationset_labels)
        return np.concatenate(labels)

    def _transform_lables(self):
        self.trainset_labels = self._label_encoder.transform(self.trainset_labels)
        if self.testset_labels is not None:
            self.testset_labels = self._label_encoder.transform(self.testset_labels)
        if self.validationset_labels is not None:
            self.validationset_labels = self._label_encoder.transform(self.validationset_labels)

    def reverse_label_transform(self, labels):
        return self._label_encoder.inverse_transform(labels)

    def amount_classes(self):
        return len(self._label_encoder.classes_)

    def train_classes(self):
        return len(np.unique(self.trainset_labels))


def split_data_by_amount(data: ndarray, labels: ndarray, train_split_parts: int = 2, test_split_parts: int = 1,
                         validation_split_parts: int = 1) -> Dataset:
    assert train_split_parts > 0 and test_split_parts >= 0 and validation_split_parts >= 0
    assert len(data) == len(labels)

    total_parts = train_split_parts + test_split_parts + validation_split_parts

    split_begin = 0
    split_end = 0

    split_begin = split_end
    split_end = int(len(data) / (train_split_parts / total_parts))
    trainset_data = data[split_begin:split_end]
    trainset_labels = labels[split_begin:split_end]

    if test_split_parts > 0:
        split_begin = split_end
        split_end = split_begin + int(len(data) / (test_split_parts / total_parts))
        testset_data = data[split_begin:split_end]
        testset_labels = labels[split_begin:split_end]
    else:
        testset_data = None
        testset_labels = None

    if validation_split_parts > 0:
        split_begin = split_end
        split_end = split_begin + int(len(data) / (validation_split_parts / total_parts))
        validationset_data = data[split_begin:split_end]
        validationset_labels = labels[split_begin:split_end]
    else:
        validationset_data = None
        validationset_labels = None

    return Dataset(trainset_data=trainset_data,
                   trainset_labels=trainset_labels,
                   testset_data=testset_data,
                   testset_labels=testset_labels,
                   validationset_data=validationset_data,
                   validationset_labels=validationset_labels)
