import os
from abc import ABC, abstractmethod

from useckit.util.data import Dataset


class PredictionModelBase(ABC):
    def __init__(self, output_dir: str = "model_out", verbose: bool = False):
        self.output_directory = output_dir
        self.verbose = verbose

    def merge_paradigm_output_folder(self, paradigm_output_folder: str):
        self.output_directory = os.path.join(paradigm_output_folder, self.output_directory)
        os.makedirs(self.output_directory, exist_ok=True)


class EvaluationMethodBase(ABC):
    def __init__(self, output_folder_name: str = "evaluation"):
        self.output_folder_name = output_folder_name

    def merge_paradigm_output_folder(self, paradigm_output_folder: str):
        self.output_folder_name = os.path.join(paradigm_output_folder, self.output_folder_name)
        os.makedirs(self.output_folder_name, exist_ok=True)


class ParadigmBase(ABC):
    _experiment_number = 1

    def __init__(self, prediction_model: PredictionModelBase, name: str = None, output_dir: str = "_useckit_out"):
        if output_dir is None or output_dir.strip() == "":
            self.output_dir = "_useckit_out"
        else:
            self.output_dir = output_dir
        if name is None or name.strip() == "":
            self.name = f"experiment_{ParadigmBase._experiment_number}"
        else:
            self.name = name
        self.output_dir = os.path.join(self.output_dir, self.name)
        os.makedirs(self.output_dir, exist_ok=True)
        ParadigmBase._experiment_number += 1
        if len(os.listdir(self.output_dir)) != 0:
            raise AttributeError(
                "Please choose a unique name for your experiment or delete/move previous results, " +
                "if you want to refrain from naming them by hand")
        prediction_model.merge_paradigm_output_folder(self.output_dir)
        self.prediction_model = prediction_model

    def _set_evaluation_methods(self, evaluation_methods: [EvaluationMethodBase]):
        for eval_method in evaluation_methods:
            eval_method.merge_paradigm_output_folder(self.output_dir)
        self.evalution_methods = evaluation_methods

    @abstractmethod
    def evaluate(self, dataset: Dataset):
        pass
