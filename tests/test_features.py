
import pandas as pd
import pytest

from src.pipeline.features import engineer_features


@pytest.fixture
def input_csv(tmp_path):
    data = {
        "sepal length (cm)": [5.0, 6.0, 7.0],
        "sepal width (cm)": [2.0, 3.0, 4.0],
        "petal length (cm)": [1.0, 3.0, 5.0],
        "petal width (cm)": [0.5, 1.0, 2.0],
        "species": ["setosa", "versicolor", "virginica"],
    }
    path = tmp_path / "input.csv"
    pd.DataFrame(data).to_csv(path, index=False)
    return path


def test_engineer_features_calculates_areas(input_csv, tmp_path):
    output_path = tmp_path / "features.csv"

    result = engineer_features(str(input_csv), str(output_path))

    assert result.loc[0, "sepal_area"] == pytest.approx(10.0)
    assert result.loc[0, "petal_area"] == pytest.approx(0.5)
    assert result.loc[1, "sepal_area"] == pytest.approx(18.0)
    assert result.loc[1, "petal_area"] == pytest.approx(3.0)


def test_engineer_features_calculates_length_ratio(input_csv, tmp_path):
    output_path = tmp_path / "features.csv"

    result = engineer_features(str(input_csv), str(output_path))

    assert result.loc[0, "sepal_to_petal_length_ratio"] == pytest.approx(5.0)
    assert result.loc[1, "sepal_to_petal_length_ratio"] == pytest.approx(2.0)


def test_engineer_features_handles_zero_petal_length(tmp_path):
    data = {
        "sepal length (cm)": [5.0],
        "sepal width (cm)": [2.0],
        "petal length (cm)": [0.0],
        "petal width (cm)": [0.0],
        "species": ["setosa"],
    }
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "features.csv"
    pd.DataFrame(data).to_csv(input_path, index=False)

    result = engineer_features(str(input_path), str(output_path))

    assert pd.isna(result.loc[0, "sepal_to_petal_length_ratio"])


def test_engineer_features_assigns_petal_length_bins(input_csv, tmp_path):
    output_path = tmp_path / "features.csv"

    result = engineer_features(str(input_csv), str(output_path))

    assert str(result.loc[0, "petal_length_bin"]) == "short"
    assert str(result.loc[1, "petal_length_bin"]) == "medium"
    assert str(result.loc[2, "petal_length_bin"]) == "long"


def test_engineer_features_writes_output_csv(input_csv, tmp_path):
    output_path = tmp_path / "features.csv"

    engineer_features(str(input_csv), str(output_path))

    assert output_path.exists()

    saved = pd.read_csv(output_path)
    assert "sepal_area" in saved.columns
    assert "petal_area" in saved.columns
    assert "sepal_to_petal_length_ratio" in saved.columns
    assert "petal_length_bin" in saved.columns
    assert len(saved) == 3
