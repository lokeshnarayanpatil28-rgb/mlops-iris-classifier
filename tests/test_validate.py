
import pandas as pd
import pytest

from src.pipeline.validate import validate, DataValidationError


@pytest.fixture
def valid_data():
    return {
        "sepal length (cm)": [5.1, 6.0, 6.5],
        "sepal width (cm)": [3.5, 2.8, 3.0],
        "petal length (cm)": [1.4, 4.5, 5.5],
        "petal width (cm)": [0.2, 1.3, 2.0],
        "species": ["setosa", "versicolor", "virginica"],
        "sepal_area": [17.85, 16.8, 19.5],
        "petal_area": [0.28, 5.85, 11.0],
        "sepal_to_petal_length_ratio": [3.64, 1.33, 1.18],
        "petal_length_bin": ["short", "medium", "long"],
    }


def write_csv(tmp_path, data):
    path = tmp_path / "features.csv"
    pd.DataFrame(data).to_csv(path, index=False)
    return path


def test_validate_accepts_valid_data(tmp_path, valid_data):
    path = write_csv(tmp_path, valid_data)

    result = validate(str(path))

    assert len(result) == 3
    assert set(result["species"]) == {"setosa", "versicolor", "virginica"}


def test_validate_rejects_missing_required_column(tmp_path, valid_data):
    valid_data.pop("sepal_area")
    path = write_csv(tmp_path, valid_data)

    with pytest.raises(DataValidationError, match="Validation failed"):
        validate(str(path))


def test_validate_rejects_null_values(tmp_path, valid_data):
    valid_data["sepal width (cm)"][0] = None
    path = write_csv(tmp_path, valid_data)

    with pytest.raises(DataValidationError, match="Validation failed"):
        validate(str(path))


def test_validate_rejects_invalid_species(tmp_path, valid_data):
    valid_data["species"][0] = "unknown"
    path = write_csv(tmp_path, valid_data)

    with pytest.raises(DataValidationError, match="Validation failed"):
        validate(str(path))


def test_validate_rejects_out_of_range_measurement(tmp_path, valid_data):
    valid_data["sepal length (cm)"][0] = 10.0
    path = write_csv(tmp_path, valid_data)

    with pytest.raises(DataValidationError, match="Validation failed"):
        validate(str(path))
