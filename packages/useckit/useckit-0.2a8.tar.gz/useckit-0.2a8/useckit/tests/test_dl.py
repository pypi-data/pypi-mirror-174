import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import sys
sys.setrecursionlimit(10000)

import unittest
import numpy as np
from useckit import AutoEvaluator, AutoAuthenticator, AutoSiameseAuthenticator


class TestAutoEvaluator(unittest.TestCase):
    def setUp(self) -> None:
        self.x_train = np.array([np.arange(0, 10), np.arange(10, 20), np.arange(20, 30)])
        self.y_train = np.array([0, 1, 2])
        self.x_val = np.array([np.arange(100, 110), np.arange(110, 120), np.arange(120, 130)])
        self.y_val = np.array([0, 1, 2])

    def test_slices_1d(self):
        print("Launching test: TestAutoEvaluator::test_slices_1d")
        from sklearn.preprocessing import LabelBinarizer
        lb = LabelBinarizer()

        ae = AutoEvaluator(self.x_train, lb.fit_transform(self.y_train), self.x_val,  lb.fit_transform(self.y_val),
                           enable_window_slicing=True, window_size=5, window_stride=2,
                           disable_normalization_check=True,
                           shuffle_window_slices=False,
                           nb_classes=11)

        x_train, y_train, x_val, y_val = ae.x_train, ae.y_train, ae.x_val, ae.y_val

        self.assertTrue(np.array_equal(np.array([[0, 1, 2, 3, 4],
                                                 [2, 3, 4, 5, 6],
                                                 [4, 5, 6, 7, 8],
                                                 [10, 11, 12, 13, 14],
                                                 [12, 13, 14, 15, 16],
                                                 [14, 15, 16, 17, 18],
                                                 [20, 21, 22, 23, 24],
                                                 [22, 23, 24, 25, 26],
                                                 [24, 25, 26, 27, 28]]), x_train))
        self.assertTrue(np.array_equal(np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0],
                                                 [0, 1, 0], [0, 1, 0], [0, 1, 0],
                                                 [0, 0, 1], [0, 0, 1], [0, 0, 1]]), y_train))
        self.assertTrue(np.array_equal(np.array([[100, 101, 102, 103, 104],
                                                 [102, 103, 104, 105, 106],
                                                 [104, 105, 106, 107, 108],
                                                 [110, 111, 112, 113, 114],
                                                 [112, 113, 114, 115, 116],
                                                 [114, 115, 116, 117, 118],
                                                 [120, 121, 122, 123, 124],
                                                 [122, 123, 124, 125, 126],
                                                 [124, 125, 126, 127, 128]]), x_val))
        self.assertTrue(np.array_equal([[1, 0, 0], [1, 0, 0], [1, 0, 0],
                                        [0, 1, 0], [0, 1, 0], [0, 1, 0],
                                        [0, 0, 1], [0, 0, 1], [0, 0, 1]], y_val))

    def test_slices_2d_mixed_labels_dtype(self):
        print("Launching test: TestAutoEvaluator::test_slices_2d_mixed_labels_dtype")
        x_train = np.array([[[0.5359274, 0.08249018, 0.89091933],
                             [0.80882945, 0.37818458, 0.25391928],
                             [0.19008578, 0.92485112, 0.11022713],
                             [0.6817229, 0.81315089, 0.42800994],
                             [0.95876003, 0.17977092, 0.40070289],
                             [0.17325143, 0.19055574, 0.07499457],
                             [0.05130531, 0.20929802, 0.165708],
                             [0.54850358, 0.58604208, 0.05273772],
                             [0.49328352, 0.53578782, 0.0879305],
                             [0.87806748, 0.91105881, 0.08477474],
                             [0.27720445, 0.82571441, 0.99001752],
                             [0.07268544, 0.65421845, 0.31915075]],
                            [[0.60440215, 0.53599585, 0.72649968],
                             [0.31000169, 0.38926371, 0.29748983],
                             [0.02413751, 0.05616292, 0.16106505],
                             [0.59741403, 0.26482075, 0.48964744],
                             [0.83301339, 0.06776695, 0.54959184],
                             [0.12008786, 0.32786579, 0.62242488],
                             [0.15605824, 0.20095281, 0.13251899],
                             [0.2859077, 0.30799345, 0.37865966],
                             [0.63819317, 0.71204672, 0.55181256],
                             [0.42783569, 0.95618881, 0.63290933],
                             [0.73122225, 0.15094184, 0.18600836],
                             [0.67734322, 0.4464666, 0.33163741]],
                            [[0.48523873, 0.43358791, 0.03430445],
                             [0.39980229, 0.82521483, 0.29878615],
                             [0.19601974, 0.7412129, 0.90436953],
                             [0.323226, 0.90592117, 0.12485468],
                             [0.69118191, 0.87767577, 0.0783868],
                             [0.40134663, 0.99027958, 0.8940429],
                             [0.23047435, 0.88926745, 0.70372876],
                             [0.6078326, 0.89042862, 0.01379226],
                             [0.5949179, 0.17918223, 0.89959008],
                             [0.25875066, 0.74966193, 0.4064441],
                             [0.23458808, 0.08966336, 0.41137135],
                             [0.97650467, 0.60956433, 0.14885139]]])

        x_val = np.array([[[0.57199003, 0.47945598, 0.2963983],
                           [0.50141056, 0.36736713, 0.90230282],
                           [0.42631566, 0.48273673, 0.7546237],
                           [0.04928868, 0.5371014, 0.11046236],
                           [0.91772924, 0.77600563, 0.89774997],
                           [0.75160818, 0.5281581, 0.27384034],
                           [0.28996399, 0.40331758, 0.80192027],
                           [0.87241846, 0.5815148, 0.49267017],
                           [0.15885638, 0.18872364, 0.08295864],
                           [0.1942771, 0.01631618, 0.45628907],
                           [0.06979198, 0.10752221, 0.09470745],
                           [0.91266834, 0.14622393, 0.55048043]],
                          [[0.91349863, 0.76052917, 0.95743973],
                           [0.20318639, 0.35065392, 0.63302048],
                           [0.79636682, 0.55457903, 0.92070657],
                           [0.14647446, 0.64568567, 0.29347421],
                           [0.78670376, 0.16937696, 0.42120461],
                           [0.94936849, 0.60737097, 0.19846161],
                           [0.41088732, 0.79759915, 0.29626504],
                           [0.86400447, 0.14359629, 0.54081413],
                           [0.90443423, 0.41934346, 0.87106158],
                           [0.67500353, 0.01217834, 0.03917625],
                           [0.67760574, 0.03819667, 0.92409448],
                           [0.28278991, 0.30947104, 0.31735007]],
                          [[0.83120495, 0.23371263, 0.52146982],
                           [0.85907556, 0.04340647, 0.26778963],
                           [0.83222697, 0.76595243, 0.29488267],
                           [0.56052546, 0.50817019, 0.76740915],
                           [0.96394765, 0.48892028, 0.83622398],
                           [0.67370428, 0.04922883, 0.98737778],
                           [0.93718289, 0.53406913, 0.89182002],
                           [0.23354, 0.60901517, 0.91887049],
                           [0.81507629, 0.03241308, 0.85612069],
                           [0.64852316, 0.59296981, 0.92127855],
                           [0.5351609, 0.65649925, 0.35894605],
                           [0.60738813, 0.54381076, 0.58423798]]])

        from sklearn.preprocessing import LabelBinarizer
        lb = LabelBinarizer()
        y_train = lb.fit_transform(np.array([0, 1, 2]))

        y_val = lb.fit_transform(np.array([0, 1, 2]))

        ae = AutoEvaluator(x_train,
                           y_train,
                           x_val,
                           y_val,
                           enable_window_slicing=True,
                           window_size=5,
                           window_stride=2,
                           shuffle_window_slices=False,
                           nb_classes=3)

        x_train_ret, y_train_ret, x_val_ret, y_val_ret = ae.x_train, ae.y_train, ae.x_val, ae.y_val

        self.assertTrue(np.array_equal(x_train_ret, np.array([[[0.5359274, 0.08249018, 0.89091933],
                                                               [0.80882945, 0.37818458, 0.25391928],
                                                               [0.19008578, 0.92485112, 0.11022713],
                                                               [0.6817229, 0.81315089, 0.42800994],
                                                               [0.95876003, 0.17977092, 0.40070289]],
                                                              [[0.19008578, 0.92485112, 0.11022713],
                                                               [0.6817229, 0.81315089, 0.42800994],
                                                               [0.95876003, 0.17977092, 0.40070289],
                                                               [0.17325143, 0.19055574, 0.07499457],
                                                               [0.05130531, 0.20929802, 0.165708]],
                                                              [[0.95876003, 0.17977092, 0.40070289],
                                                               [0.17325143, 0.19055574, 0.07499457],
                                                               [0.05130531, 0.20929802, 0.165708],
                                                               [0.54850358, 0.58604208, 0.05273772],
                                                               [0.49328352, 0.53578782, 0.0879305]],
                                                              [[0.05130531, 0.20929802, 0.165708],
                                                               [0.54850358, 0.58604208, 0.05273772],
                                                               [0.49328352, 0.53578782, 0.0879305],
                                                               [0.87806748, 0.91105881, 0.08477474],
                                                               [0.27720445, 0.82571441, 0.99001752]],
                                                              [[0.60440215, 0.53599585, 0.72649968],
                                                               [0.31000169, 0.38926371, 0.29748983],
                                                               [0.02413751, 0.05616292, 0.16106505],
                                                               [0.59741403, 0.26482075, 0.48964744],
                                                               [0.83301339, 0.06776695, 0.54959184]],
                                                              [[0.02413751, 0.05616292, 0.16106505],
                                                               [0.59741403, 0.26482075, 0.48964744],
                                                               [0.83301339, 0.06776695, 0.54959184],
                                                               [0.12008786, 0.32786579, 0.62242488],
                                                               [0.15605824, 0.20095281, 0.13251899]],
                                                              [[0.83301339, 0.06776695, 0.54959184],
                                                               [0.12008786, 0.32786579, 0.62242488],
                                                               [0.15605824, 0.20095281, 0.13251899],
                                                               [0.2859077, 0.30799345, 0.37865966],
                                                               [0.63819317, 0.71204672, 0.55181256]],
                                                              [[0.15605824, 0.20095281, 0.13251899],
                                                               [0.2859077, 0.30799345, 0.37865966],
                                                               [0.63819317, 0.71204672, 0.55181256],
                                                               [0.42783569, 0.95618881, 0.63290933],
                                                               [0.73122225, 0.15094184, 0.18600836]],
                                                              [[0.48523873, 0.43358791, 0.03430445],
                                                               [0.39980229, 0.82521483, 0.29878615],
                                                               [0.19601974, 0.7412129, 0.90436953],
                                                               [0.323226, 0.90592117, 0.12485468],
                                                               [0.69118191, 0.87767577, 0.0783868]],
                                                              [[0.19601974, 0.7412129, 0.90436953],
                                                               [0.323226, 0.90592117, 0.12485468],
                                                               [0.69118191, 0.87767577, 0.0783868],
                                                               [0.40134663, 0.99027958, 0.8940429],
                                                               [0.23047435, 0.88926745, 0.70372876]],
                                                              [[0.69118191, 0.87767577, 0.0783868],
                                                               [0.40134663, 0.99027958, 0.8940429],
                                                               [0.23047435, 0.88926745, 0.70372876],
                                                               [0.6078326, 0.89042862, 0.01379226],
                                                               [0.5949179, 0.17918223, 0.89959008]],
                                                              [[0.23047435, 0.88926745, 0.70372876],
                                                               [0.6078326, 0.89042862, 0.01379226],
                                                               [0.5949179, 0.17918223, 0.89959008],
                                                               [0.25875066, 0.74966193, 0.4064441],
                                                               [0.23458808, 0.08966336, 0.41137135]]])))
        self.assertTrue(np.array_equal(y_train_ret, np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0],
                                                              [1, 0, 0], [0, 1, 0], [0, 1, 0],
                                                              [0, 1, 0], [0, 1, 0], [0, 0, 1],
                                                              [0, 0, 1], [0, 0, 1], [0, 0, 1]])))
        self.assertTrue(np.array_equal(x_val_ret, np.array([[[0.57199003, 0.47945598, 0.2963983],
                                                             [0.50141056, 0.36736713, 0.90230282],
                                                             [0.42631566, 0.48273673, 0.7546237],
                                                             [0.04928868, 0.5371014, 0.11046236],
                                                             [0.91772924, 0.77600563, 0.89774997]],
                                                            [[0.42631566, 0.48273673, 0.7546237],
                                                             [0.04928868, 0.5371014, 0.11046236],
                                                             [0.91772924, 0.77600563, 0.89774997],
                                                             [0.75160818, 0.5281581, 0.27384034],
                                                             [0.28996399, 0.40331758, 0.80192027]],
                                                            [[0.91772924, 0.77600563, 0.89774997],
                                                             [0.75160818, 0.5281581, 0.27384034],
                                                             [0.28996399, 0.40331758, 0.80192027],
                                                             [0.87241846, 0.5815148, 0.49267017],
                                                             [0.15885638, 0.18872364, 0.08295864]],
                                                            [[0.28996399, 0.40331758, 0.80192027],
                                                             [0.87241846, 0.5815148, 0.49267017],
                                                             [0.15885638, 0.18872364, 0.08295864],
                                                             [0.1942771, 0.01631618, 0.45628907],
                                                             [0.06979198, 0.10752221, 0.09470745]],
                                                            [[0.91349863, 0.76052917, 0.95743973],
                                                             [0.20318639, 0.35065392, 0.63302048],
                                                             [0.79636682, 0.55457903, 0.92070657],
                                                             [0.14647446, 0.64568567, 0.29347421],
                                                             [0.78670376, 0.16937696, 0.42120461]],
                                                            [[0.79636682, 0.55457903, 0.92070657],
                                                             [0.14647446, 0.64568567, 0.29347421],
                                                             [0.78670376, 0.16937696, 0.42120461],
                                                             [0.94936849, 0.60737097, 0.19846161],
                                                             [0.41088732, 0.79759915, 0.29626504]],
                                                            [[0.78670376, 0.16937696, 0.42120461],
                                                             [0.94936849, 0.60737097, 0.19846161],
                                                             [0.41088732, 0.79759915, 0.29626504],
                                                             [0.86400447, 0.14359629, 0.54081413],
                                                             [0.90443423, 0.41934346, 0.87106158]],
                                                            [[0.41088732, 0.79759915, 0.29626504],
                                                             [0.86400447, 0.14359629, 0.54081413],
                                                             [0.90443423, 0.41934346, 0.87106158],
                                                             [0.67500353, 0.01217834, 0.03917625],
                                                             [0.67760574, 0.03819667, 0.92409448]],
                                                            [[0.83120495, 0.23371263, 0.52146982],
                                                             [0.85907556, 0.04340647, 0.26778963],
                                                             [0.83222697, 0.76595243, 0.29488267],
                                                             [0.56052546, 0.50817019, 0.76740915],
                                                             [0.96394765, 0.48892028, 0.83622398]],
                                                            [[0.83222697, 0.76595243, 0.29488267],
                                                             [0.56052546, 0.50817019, 0.76740915],
                                                             [0.96394765, 0.48892028, 0.83622398],
                                                             [0.67370428, 0.04922883, 0.98737778],
                                                             [0.93718289, 0.53406913, 0.89182002]],
                                                            [[0.96394765, 0.48892028, 0.83622398],
                                                             [0.67370428, 0.04922883, 0.98737778],
                                                             [0.93718289, 0.53406913, 0.89182002],
                                                             [0.23354, 0.60901517, 0.91887049],
                                                             [0.81507629, 0.03241308, 0.85612069]],
                                                            [[0.93718289, 0.53406913, 0.89182002],
                                                             [0.23354, 0.60901517, 0.91887049],
                                                             [0.81507629, 0.03241308, 0.85612069],
                                                             [0.64852316, 0.59296981, 0.92127855],
                                                             [0.5351609, 0.65649925, 0.35894605]]])))
        self.assertTrue(np.array_equal(y_val_ret, np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0],
                                                            [1, 0, 0], [0, 1, 0], [0, 1, 0],
                                                            [0, 1, 0], [0, 1, 0], [0, 0, 1],
                                                            [0, 0, 1], [0, 0, 1], [0, 0, 1]])))

    def test_mixed_labels_dtype(self):
        print("Launching test: TestAutoEvaluator::test_mixed_labels_dtype")
        y_train = np.array([4, 5, 6])
        y_train_ret = AutoEvaluator.create_ohc_labels(y_train)

        self.assertTrue(np.array_equal(y_train_ret, np.array([[1, 0, 0],
                                                              [0, 1, 0],
                                                              [0, 0, 1]])))

        y_val = np.array(['P4', 'P5', 'P6'])
        y_val_ret = AutoEvaluator.create_ohc_labels(y_val)

        self.assertTrue(np.array_equal(y_val_ret, np.array([[1, 0, 0],
                                                            [0, 1, 0],
                                                            [0, 0, 1]])))

    @staticmethod
    def make_some_noise(shape: tuple = (20, 3,)):
        arr = np.array([np.ones(shape) * 0.75 + np.random.normal(0, 0.1, shape),
                        np.zeros(shape) + np.random.normal(0, 0.1, shape),
                        np.ones(shape) * -0.75 + np.random.normal(0, 0.1, shape)] +

                       [np.ones(shape) * 0.75 + np.random.normal(0, 0.1, shape),
                        np.zeros(shape) + np.random.normal(0, 0.1, shape),
                        np.ones(shape) * -0.75 + np.random.normal(0, 0.1, shape)] +

                       [np.ones(shape) * 0.75 + np.random.normal(0, 0.1, shape),
                        np.zeros(shape) + np.random.normal(0, 0.1, shape),
                        np.ones(shape) * -0.75 + np.random.normal(0, 0.1, shape)])
        arr = np.clip(arr, -1, 1)
        return arr

    def test_training(self):
        print("Launching test: TestAutoEvaluator::test_training")
        x_train = self.make_some_noise((1200, 3,))
        x_val = self.make_some_noise((1200, 3,))

        y_train = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]*3)
        y_val = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]*3)

        ae = AutoEvaluator(x_train, y_train, x_val, y_val,
                           enable_window_slicing=True,
                           window_size=100,
                           window_stride=10,
                           nb_classes=3,
                           verbose=1,
                           epochs=5)
        try:
            ae.evaluate()
        except RecursionError as re:
            print('Encountered RecursionError in CI/CD. The cause is unknown.', str(re))
            print('Aborting the test.')
            return

    def test_mcdcnn(self):
        print("Launching test: TestAutoEvaluator::test_mcdcnn")
        x_train = self.make_some_noise((1200, 3,))
        x_val = self.make_some_noise((1200, 3,))

        y_train = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]*3)
        y_val = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]*3)

        ae = AutoEvaluator(x_train, y_train, x_val, y_val,
                           custom_name='test_mcdcnn',
                           enable_window_slicing=True,
                           window_size=100,
                           window_stride=10,
                           nb_classes=3,
                           verbose=1,
                           epochs=5,
                           enable_mcdcnn=True,
                           enable_mcnn=False,
                           enable_tlenet=False,
                           enable_twiesn=False,
                           enable_cnn=False,
                           enable_encoder=False,
                           enable_fcn=False,
                           enable_inception=False,
                           enable_resnet=False,
                           enable_mlp=False)
        ae.evaluate()

    def test_mcnn(self):
        print("Launching test: TestAutoEvaluator::test_mcnn")
        x_train = self.make_some_noise((1200, 3,))
        x_val = self.make_some_noise((1200, 3,))

        y_train = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 3)
        y_val = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 3)

        ae = AutoEvaluator(x_train, y_train, x_val, y_val,
                           custom_name='test_mcnn',
                           enable_window_slicing=True,
                           window_size=100,
                           window_stride=10,
                           nb_classes=3,
                           verbose=1,
                           epochs=5,
                           enable_mcdcnn=False,
                           enable_mcnn=True,
                           enable_tlenet=False,
                           enable_twiesn=False,
                           enable_cnn=False,
                           enable_encoder=False,
                           enable_fcn=False,
                           enable_inception=False,
                           enable_resnet=False,
                           enable_mlp=False)
        ae.evaluate()

    def test_tlenet(self):
        print("Launching test: TestAutoEvaluator::test_tlenet")
        x_train = self.make_some_noise((1200, 3,))
        x_val = self.make_some_noise((1200, 3,))

        y_train = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 3)
        y_val = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 3)

        ae = AutoEvaluator(x_train, y_train, x_val, y_val,
                           custom_name='test_tlenet',
                           enable_window_slicing=True,
                           window_size=100,
                           window_stride=10,
                           nb_classes=3,
                           verbose=1,
                           epochs=5,
                           enable_mcdcnn=False,
                           enable_mcnn=False,
                           enable_tlenet=True,
                           enable_twiesn=False,
                           enable_cnn=False,
                           enable_encoder=False,
                           enable_fcn=False,
                           enable_inception=False,
                           enable_resnet=False,
                           enable_mlp=False)
        ae.evaluate()

    def test_twiesn(self):
        print("Launching test: TestAutoEvaluator::test_twiesn")
        x_train = self.make_some_noise((1200, 3,))
        x_val = self.make_some_noise((1200, 3,))

        y_train = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 3)
        y_val = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 3)

        ae = AutoEvaluator(x_train, y_train, x_val, y_val,
                           custom_name='test_twiesn',
                           enable_window_slicing=True,
                           window_size=100,
                           window_stride=10,
                           nb_classes=3,
                           verbose=1,
                           epochs=5,
                           enable_mcdcnn=False,
                           enable_mcnn=False,
                           enable_tlenet=False,
                           enable_twiesn=True,
                           enable_cnn=False,
                           enable_encoder=False,
                           enable_fcn=False,
                           enable_inception=False,
                           enable_resnet=False,
                           enable_mlp=False)
        ae.evaluate()

    def test_other_4_classifiers(self):
        print("Launching test: TestAutoEvaluator::test_other_4_classifiers")
        x_train = self.make_some_noise((1200, 3,))
        x_val = self.make_some_noise((1200, 3,))

        y_train = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 3)
        y_val = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 3)

        ae = AutoEvaluator(x_train, y_train, x_val, y_val,
                           enable_window_slicing=True,
                           window_size=100,
                           window_stride=10,
                           nb_classes=3,
                           verbose=1,
                           epochs=5,
                           enable_mcdcnn=True,
                           enable_mcnn=True,
                           enable_tlenet=True,
                           enable_twiesn=True,
                           enable_cnn=False,
                           enable_encoder=False,
                           enable_fcn=False,
                           enable_inception=False,
                           enable_resnet=False,
                           enable_mlp=False)
        ae.evaluate()

    def test_exclude_bad_ohc0(self):
        print("Launching test: TestAutoEvaluator::test_exclude_bad_ohc0")
        x_train = self.make_some_noise((1200, 3,))
        x_val = self.make_some_noise((1200, 3,))
        y_train = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 3)
        y_val = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]] * 3)  # last ohc is zeroed
        self.assertRaises(ValueError, AutoEvaluator, x_train, y_train, x_val, y_val, 11)

    def test_exclude_bad_ohc1(self):
        print("Launching test: TestAutoEvaluator::test_exclude_bad_ohc1")
        x_train = self.make_some_noise((1200, 3,))
        x_val = self.make_some_noise((1200, 3,))
        y_train = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 3)
        y_val = np.array([[1, 0, 0], [0, 1, 0], [0, 1, 1]] * 3)  # last ohc is 2
        self.assertRaises(ValueError, AutoEvaluator, x_train, y_train, x_val, y_val, 11)

    def test_exclude_bad_ohc2(self):
        print("Launching test: TestAutoEvaluator::test_exclude_bad_ohc2")
        x_train = self.make_some_noise((1200, 3,))
        x_val = self.make_some_noise((1200, 3,))
        y_train = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]] * 3)  # last ohc is zeroed
        y_val = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]] * 3)
        self.assertRaises(ValueError, AutoEvaluator, x_train, y_train, x_val, y_val, 11)

    def test_exclude_bad_ohc3(self):
        print("Launching test: TestAutoEvaluator::test_exclude_bad_ohc3")
        x_train = self.make_some_noise((1200, 3,))
        x_val = self.make_some_noise((1200, 3,))
        y_train = np.array([[1, 0, 0], [0, 1, 0], [0, 1, 1]] * 3)  # last ohc is two
        y_val = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]] * 3)
        self.assertRaises(ValueError, AutoEvaluator, x_train, y_train, x_val, y_val, 11)


class TestAutoAuthenticator(unittest.TestCase):
    def test_aa(self):
        print("Launching test: TestAutoAuthenticator::test_aa")
        x_train = TestAutoEvaluator.make_some_noise((1200, 3,))
        x_val = TestAutoEvaluator.make_some_noise((1200, 3,))

        y_train = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]*3)
        y_val = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]*3)

        aa = AutoAuthenticator(x_train, y_train, x_val, y_val, 3, set())
        evaluation = aa.evaluate()

        accepted = aa.accept_samples(x_val, 0)

    def test_aa_simple(self):
        print("Launching test: TestAutoAuthenticator::test_aa_simple")
        x_train = TestAutoEvaluator.make_some_noise((1200, 3,))
        x_val = TestAutoEvaluator.make_some_noise((1200, 3,))

        y_train = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]*3)
        y_val = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]*3)

        aa = AutoAuthenticator(x_train, y_train, x_val, y_val, 3, set(), epochs=1)
        evaluation = aa.evaluate()

        accepted = aa.accept_samples(x_val, 0)


if __name__ == '__main__':
    unittest.main()
