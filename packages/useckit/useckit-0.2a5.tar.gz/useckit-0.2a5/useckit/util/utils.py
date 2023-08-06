import os.path
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

matplotlib.use('agg')
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'Arial'


def _unison_shuffle_np_arrays_3(a: np.ndarray, b: np.ndarray, c: np.ndarray):
    assert len(a) == len(b) == len(c)
    p = np.random.permutation(len(a))
    return a[p], b[p], c[p]


def create_window_slices(data: np.ndarray,
                         labels: np.ndarray,
                         stride: int,
                         slice_size: int,
                         shuffle: bool = True) -> [np.ndarray, np.ndarray]:
    if not data.shape[0] == labels.shape[0]:
        raise TypeError("Error in AutoEvaluator::_create_slices(). Data and Labels differ in size.")

    if not len(data.shape) <= 3:
        raise TypeError("Error in AutoEvaluator::_create_slices(). Dimension not supported.")

    ret_sliced_data, ret_sliced_labels, ret_sample_origin = [], [], []

    for sample_id, (array, label) in enumerate(zip(data, labels)):
        array_slices, label_slices, sample_origin = [], [], []

        lost_samples_cnt, added_cnt = 0, 0

        for step_idx in range(0, array.shape[0], stride):
            arr = array[step_idx:step_idx + slice_size]

            if not arr.any():
                pass  # do not append if slice consists only of zero
            else:
                array_slices.append(arr)
                label_slices.append(label)
                sample_origin.append(sample_id)

        for i in range(len(array_slices)):
            if array_slices[i].shape == array_slices[0].shape:
                ret_sliced_data.append(array_slices[i])
                ret_sliced_labels.append(label_slices[i])
                ret_sample_origin.append(sample_origin[i])
                added_cnt += 1
            else:
                lost_samples_cnt += 1

        if not all(s.shape == array_slices[0].shape for s in array_slices):
            print('Warning: `slices` array created in AutoEvaluator::_create_slices() is ragged. '
                  'Check parameters stride, slice_size and shape of array. Lost',
                  lost_samples_cnt, 'samples and created', added_cnt,
                  'new samples. Check your slicing window settings.', file=sys.stderr)

    ret_sliced_data_np = np.array(ret_sliced_data)
    ret_sliced_labels_np = np.array(ret_sliced_labels)
    sample_origin_np = np.array(ret_sample_origin)

    print('Info: Slicing window data consumes', round(ret_sliced_data_np.nbytes / 1024 / 1024, 2), 'mb.',
          file=sys.stderr)

    # TODO check that supressing null arrays does not result in a skewed data set

    if shuffle:
        return _unison_shuffle_np_arrays_3(ret_sliced_data_np, ret_sliced_labels_np, sample_origin_np)
    else:
        return ret_sliced_data_np, ret_sliced_labels_np, sample_origin_np


def default_make_pairs(x, y):
    """Creates a tuple containing image pairs with corresponding label.

    Arguments:
        x: List containing images, each index in this list corresponds to one image.
        y: List containing labels, each label with datatype of `int`.

    Returns:
        Tuple containing two numpy arrays as (pairs_of_samples, labels),
        where pairs_of_samples' shape is (2len(x), 2,n_features_dims) and
        labels are a binary array of shape (2len(x)).
    """
    x = np.array(x)
    y = np.array(y)
    assert x.shape[0] == y.shape[0]
    y_set = set(y)

    pairs = []
    labels = []

    matching_masks = {}
    non_matching_masks = {}
    for label in y_set:
        match = (y == label)
        matching_masks[label] = match
        non_matching_masks[label] = np.invert(match)

    for i in range(len(x)):
        x1 = x[i]
        label = y[i]

        # generate matching pair
        matches = x[matching_masks[label]]
        i = np.random.randint(0, len(matches))
        x2 = matches[i]
        pairs += [[x1, x2]]
        labels += [0]

        # generate non-matching pair
        matches = x[non_matching_masks[label]]
        i = np.random.randint(0, len(matches))
        x2 = matches[i]
        pairs += [[x1, x2]]
        labels += [1]

    return np.array(pairs), np.array(labels).astype("float32")


def calculate_metrics(y_true, y_pred, duration, y_true_val=None, y_pred_val=None):
    res = pd.DataFrame(data=np.zeros((1, 4), dtype=np.float64), index=[0],
                       columns=['precision', 'accuracy', 'recall', 'duration'])
    res['precision'] = precision_score(y_true, y_pred, average='macro')
    res['accuracy'] = accuracy_score(y_true, y_pred)

    if not y_true_val is None:
        # this is useful when transfer learning is used with cross validation
        res['accuracy_val'] = accuracy_score(y_true_val, y_pred_val)

    res['recall'] = recall_score(y_true, y_pred, average='macro')
    res['duration'] = duration
    return res


def plot_epochs_metric(hist, file_name, metric='loss'):
    plt.figure()
    plt.plot(hist.history[metric])
    plt.plot(hist.history['val_' + metric])
    plt.title('model ' + metric)
    plt.ylabel(metric, fontsize='large')
    plt.xlabel('epoch', fontsize='large')
    plt.legend(['train', 'val'], loc='upper left')
    plt.savefig(file_name, bbox_inches='tight')
    plt.close()


def save_logs(output_directory, hist, y_pred, y_true, duration, lr=True, y_true_val=None, y_pred_val=None):
    hist_df = pd.DataFrame(hist.history)
    hist_df.to_csv(os.path.join(output_directory, 'history.csv'), index=False)

    df_metrics = calculate_metrics(y_true, y_pred, duration, y_true_val, y_pred_val)
    df_metrics.to_csv(os.path.join(output_directory, 'df_metrics.csv'), index=False)

    index_best_model = hist_df['loss'].idxmin()
    row_best_model = hist_df.loc[index_best_model]

    df_best_model = pd.DataFrame(data=np.zeros((1, 6), dtype=np.float64), index=[0],
                                 columns=['best_model_train_loss', 'best_model_val_loss', 'best_model_train_acc',
                                          'best_model_val_acc', 'best_model_learning_rate', 'best_model_nb_epoch'])

    df_best_model['best_model_train_loss'] = row_best_model['loss']
    df_best_model['best_model_val_loss'] = row_best_model['val_loss']
    df_best_model['best_model_train_acc'] = row_best_model['accuracy']
    df_best_model['best_model_val_acc'] = row_best_model['val_accuracy']
    if lr == True:
        df_best_model['best_model_learning_rate'] = row_best_model['lr']
    df_best_model['best_model_nb_epoch'] = index_best_model

    df_best_model.to_csv(os.path.join(output_directory, 'df_best_model.csv'), index=False)

    # for FCN there is no hyperparameters fine tuning - everything is static in code

    # plot losses
    plot_epochs_metric(hist, os.path.join(output_directory, 'epochs_loss.png'))

    return df_metrics


def save_test_duration(file_name, test_duration):
    res = pd.DataFrame(data=np.zeros((1, 1), dtype=np.float64), index=[0],
                       columns=['test_duration'])
    res['test_duration'] = test_duration
    res.to_csv(file_name, index=False)


def create_directory(directory_path):
    if os.path.exists(directory_path):
        return None
    else:
        try:
            os.makedirs(directory_path)
        except:
            # in case another machine created the path meanwhile !:(
            return None
        return directory_path


def save_logs_t_leNet(output_directory, hist, y_pred, y_true, duration):
    hist_df = pd.DataFrame(hist.history)
    hist_df.to_csv(os.path.join(output_directory, 'history.csv'), index=False)

    df_metrics = calculate_metrics(y_true, y_pred, duration)
    df_metrics.to_csv(os.path.join(output_directory, 'df_metrics.csv'), index=False)

    index_best_model = hist_df['loss'].idxmin()
    row_best_model = hist_df.loc[index_best_model]

    df_best_model = pd.DataFrame(data=np.zeros((1, 6), dtype=np.float64), index=[0],
                                 columns=['best_model_train_loss', 'best_model_val_loss', 'best_model_train_acc',
                                          'best_model_val_acc', 'best_model_learning_rate', 'best_model_nb_epoch'])

    df_best_model['best_model_train_loss'] = row_best_model['loss']
    df_best_model['best_model_val_loss'] = row_best_model['val_loss']
    df_best_model['best_model_train_acc'] = row_best_model['accuracy']
    df_best_model['best_model_val_acc'] = row_best_model['val_accuracy']
    df_best_model['best_model_nb_epoch'] = index_best_model

    df_best_model.to_csv(os.path.join(output_directory, 'df_best_model.csv'), index=False)

    # plot losses
    plot_epochs_metric(hist, os.path.join(output_directory, 'epochs_loss.png'))
