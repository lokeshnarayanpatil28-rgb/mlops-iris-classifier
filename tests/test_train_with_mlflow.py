import importlib.util
import unittest
from pathlib import Path


class TrainWithMlflowTests(unittest.TestCase):
    def test_train_with_mlflow_module_imports(self):
        module_path = Path(__file__).resolve().parents[1] / "src" / "train_with_mlflow.py"
        spec = importlib.util.spec_from_file_location("train_with_mlflow", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertTrue(hasattr(module, "main"))


if __name__ == "__main__":
    unittest.main()
