from types import FunctionType
from typing import Any
from typing import List, Tuple

from .dataset_transformation.dataset_transformation import GenericDatasetTransformationManager
from .object_manager import ObjectManager


# TODO: import model managers and types directly from their respective modules?
# i.e. find a way not to list everything
def _load_tf_managers():
    try:
        import tensorflow as tf
        from .model.tensorflow_model import TensorflowModelManager
        from .dataset.tensorflow_dataset import TensorflowDatasetManager
    except ImportError:
        print("tensorflow import not found, tensorflow managers will not be loaded")
        return []
    return [
        (tf.data.Dataset, TensorflowDatasetManager),
        (tf.keras.Sequential, TensorflowModelManager),
    ]


def _load_lgbm_managers():
    try:
        from .model.lightgbm_model import LightGBMModelManager
        import lightgbm as lgb
    except ImportError:
        print("lightgbm import not found, lightgbm managers will not be loaded")
        return []
    return [
        (lgb.Booster, LightGBMModelManager),
        (lgb.LGBMModel, LightGBMModelManager),
        (lgb.LGBMRanker, LightGBMModelManager),
        (lgb.LGBMRegressor, LightGBMModelManager),
        (lgb.LGBMClassifier, LightGBMModelManager),
        (lgb.DaskLGBMRanker, LightGBMModelManager),
        (lgb.DaskLGBMRegressor, LightGBMModelManager),
        (lgb.DaskLGBMClassifier, LightGBMModelManager),
    ]


def _load_sklearn_managers():
    try:
        from sklearn.base import BaseEstimator
        from .model.sklearn_model import SKLearnModelManager
    except ImportError:
        print("sklearn import not found, sklearn managers will not be loaded")
        return []
    return [
        (BaseEstimator, SKLearnModelManager),
    ]


def _load_xgb_managers():
    try:
        import xgboost as xgb
        from .model.xgb_model import XGBoostModelManager
    except ImportError:
        print("xgboost import not found, xgboost managers will not be loaded")
        return []
    return [
        (xgb.XGBClassifier, XGBoostModelManager),
        (xgb.Booster, XGBoostModelManager),
        (xgb.XGBModel, XGBoostModelManager),
        (xgb.XGBRanker, XGBoostModelManager),
        (xgb.XGBRegressor, XGBoostModelManager),
        (xgb.XGBRFRegressor, XGBoostModelManager),
        (xgb.XGBRFClassifier, XGBoostModelManager),
    ]


def _load_pandas_managers():
    from .dataset.pandas_dataset import PandasDatasetManager
    import pandas as pd

    return [
        (pd.DataFrame, PandasDatasetManager),
    ]


def _get_object_manager_class_types():
    # Needs to be imported lazilly as it returns a tracked object type
    from .proxy import tracked_decorator

    _object_manager_class_types: List[Tuple[type, ObjectManager.__class__]] = [
        (tracked_decorator, GenericDatasetTransformationManager),
        *_load_tf_managers(),
        *_load_lgbm_managers(),
        *_load_xgb_managers(),
        *_load_pandas_managers(),
        *_load_sklearn_managers(),
    ]

    _combined_object_managers_mappings = {
        manager.__name__: manager for t, manager in _object_manager_class_types
    }

    return _object_manager_class_types, _combined_object_managers_mappings


def load_object_manager_from_class_name(class_name: str) -> ObjectManager:
    _, mapper = _get_object_manager_class_types()
    if class_name not in mapper:
        raise NotImplementedError(f"No object manager found for class: {class_name}")
    return mapper.get(class_name)()


def load_object_manager_from_obj(obj: Any) -> ObjectManager:
    type_manager_list, _ = _get_object_manager_class_types()
    for t, manager in type_manager_list:
        try:
            if isinstance(obj, FunctionType) and isinstance(t, FunctionType):
                if obj.__name__ == t.__name__:
                    return manager()
            elif not isinstance(obj, FunctionType) and not isinstance(t, FunctionType):
                if isinstance(obj, t):
                    return manager()
        except Exception as e:
            print(
                f"Exception checking type: {t} with manager: {manager} during load proxy object manager: {e}"
            )
    raise NotImplementedError(f"Not object manager for object: {obj.__class__}")
