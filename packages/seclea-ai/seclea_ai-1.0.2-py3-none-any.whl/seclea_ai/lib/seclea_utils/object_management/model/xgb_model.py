from typing import Any, Dict

import xgboost as xgb

from ..object_manager import ModelManager


class XGBoostModelManager(ModelManager):
    framework = "xgboost"

    def save_object(self, obj: xgb.Booster):
        # save to temp file then use manager to store.
        self.metadata.update({self._model_name_key: obj.__class__.__name__})
        obj.save_model(self.object_file_path)

    def load_object(self) -> Any:
        """
        Loads a stored XGBoost model. Note this will always return a Booster (LearningAPI model) even if the original
        model was an SKLearn model. This will impact the methods available on the returned model.
        :param reference:
        :return: XGBoost.Booster model.
        """
        # TODO need to be careful about customer usage - ie. do they use the best iteration for their model or not....
        model_name = self.metadata.get(self._model_name_key)
        model = getattr(xgb, model_name, None)
        if model is None:
            raise TypeError(f"Cannot load xgboost model: {model_name} - not found")
        model = model()
        model.load_model(self.object_file_path)
        return model

    def hash_object(self, obj) -> int:
        return hash(str(obj))

    @staticmethod
    def get_params(model) -> Dict:
        """
        Extracts the parameters of the model.
        :param model: The model
        """

        return model.save_config()
