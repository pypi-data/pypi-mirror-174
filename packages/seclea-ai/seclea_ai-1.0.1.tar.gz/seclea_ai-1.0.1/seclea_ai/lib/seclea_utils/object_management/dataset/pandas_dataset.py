from __future__ import annotations

from typing import Any

import pandas as pd

from ..object_manager import DatasetManager


class PandasDatasetManager(DatasetManager):
    def save_object(self, obj: pd.DataFrame):
        """
        @param obj:
        @return:
        """
        obj.to_csv(self.object_file_path, index=True)

    def load_object(self) -> Any:
        return pd.read_csv(self.object_file_path, index_col=self.metadata.get("index", 0))

    def hash_object(self, obj) -> int:
        return sum(int(pd.util.hash_pandas_object(obj[col]).sum()) for col in obj.columns)
