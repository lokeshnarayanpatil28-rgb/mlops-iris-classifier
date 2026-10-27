
import pandas as pd
from src.pipeline.preprocess import preprocess


def create_input_csv(tmp_path, data):
    input_file = tmp_path / "input.csv"
    pd.DataFrame(data).to_csv(input_file, index=False)
    return input_file


def test_preprocess_removes_duplicates_and_collected_at(tmp_path):
    data = {
        "sepal length (cm)": [5.1, 5.1, 6.2],
        "sepal width (cm)": [3.5, 3.5, 3.4],
        "petal length (cm)": [1.4, 1.4, 5.4],
        "petal width (cm)": [0.2, 0.2, 2.3],
        "species": ["setosa", "setosa", "virginica"],
        "collected_at": ["2025-01-01", "2025-01-01", "2025-01-02"],
    }
    input_file = create_input_csv(tmp_path, data)
    output_file = tmp_path / "output.csv"

    result = preprocess(str(input_file), str(output_file))

    assert len(result) == 2
    assert "collected_at" not in result.columns
    assert output_file.exists()


def test_preprocess_fills_missing_numeric_values_with_median(tmp_path):
    data = {
        "sepal length (cm)": [4.0, None, 8.0],
        "sepal width (cm)": [2.0, 3.0, 4.0],
        "petal length (cm)": [1.0, 2.0, 3.0],
        "petal width (cm)": [0.1, 0.2, 0.3],
        "species": ["setosa", "versicolor", "virginica"],
    }
    input_file = create_input_csv(tmp_path, data)
    output_file = tmp_path / "output.csv"

    result = preprocess(str(input_file), str(output_file))

    assert result["sepal length (cm)"].isna().sum() == 0
    assert result.loc[1, "sepal length (cm)"] == 6.0


def test_preprocess_drops_rows_with_missing_species(tmp_path):
    data = {
        "sepal length (cm)": [5.1, 6.2],
        "sepal width (cm)": [3.5, 3.4],
        "petal length (cm)": [1.4, 5.4],
        "petal width (cm)": [0.2, 2.3],
        "species": ["setosa", None],
    }
    input_file = create_input_csv(tmp_path, data)
    output_file = tmp_path / "output.csv"

    result = preprocess(str(input_file), str(output_file))

    assert len(result) == 1
    assert result["species"].notna().all()


def test_preprocess_writes_processed_csv(tmp_path):
    data = {
        "sepal length (cm)": [5.1],
        "sepal width (cm)": [3.5],
        "petal length (cm)": [1.4],
        "petal width (cm)": [0.2],
        "species": ["setosa"],
    }
    input_file = create_input_csv(tmp_path, data)
    output_file = tmp_path / "output.csv"

    preprocess(str(input_file), str(output_file))
    saved_data = pd.read_csv(output_file)

    assert len(saved_data) == 1
    assert saved_data.loc[0, "species"] == "setosa"
