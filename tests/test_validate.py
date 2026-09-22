import csv
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pipeline.validate import DataValidationError, validate


class ValidateTests(unittest.TestCase):
    def test_missing_required_columns_raises_validation_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "bad.csv")
            with open(csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["sepal length (cm)", "sepal width (cm)"])
                writer.writerow([5.1, 3.5])

            with self.assertRaises(DataValidationError):
                validate(csv_path)


if __name__ == "__main__":
    unittest.main()
