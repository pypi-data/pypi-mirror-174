import copy
from typing import Any, Dict

import lightgbm as lgb

from ..object_manager import ModelManager
from ..utils import from_file, to_file


class LightGBMModelManager(ModelManager):
    framework = "lightgbm"

    def save_object(self, obj: Any):
        self.metadata.update({self._model_name_key: obj.__class__.__name__})
        # TODO: review saving here, it seems strange to do it this way, bad smell...
        obj = getattr(obj, "booster_", obj)
        to_file(obj.model_to_string(), self.object_file_path)

    def load_object(self) -> Any:
        """
        :return: LightGBM.Booster model
        """

        model = getattr(lgb, self.metadata.get(self._model_name_key), None)
        if model is None:
            raise TypeError(f"lgb model not found: {self.metadata.get(self._model_name_key)}")
        return model(model_str=from_file(self.object_file_path))

    def hash_object(self, obj) -> int:
        return hash(str(obj))

    @staticmethod
    def get_params(model) -> Dict:
        """
        Extracts the parameters of the model.
        :param model: The model
        """

        return copy.deepcopy(model.params)
