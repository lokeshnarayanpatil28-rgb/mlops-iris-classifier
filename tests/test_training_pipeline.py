
import numpy as np
import pytest
from sklearn.ensemble import RandomForestClassifier

from src.train import load_data, train_model, evaluate_model


def test_load_data_returns_train_test_splits():
    X_train, X_test, y_train, y_test = load_data()

    assert len(X_train) == 120
    assert len(X_test) == 30
    assert len(y_train) == 120
    assert len(y_test) == 30
    assert X_train.shape[1] == 4


def test_train_model_returns_random_forest():
    X_train, X_test, y_train, y_test = load_data()

    model = train_model(X_train, y_train)

    assert isinstance(model, RandomForestClassifier)
    assert model.n_estimators == 100
    assert model.random_state == 42
    assert hasattr(model, "classes_")


def test_train_model_supports_custom_parameters():
    X_train, X_test, y_train, y_test = load_data()

    model = train_model(
        X_train, y_train, n_estimators=25, max_depth=3
    )

    assert model.n_estimators == 25
    assert model.max_depth == 3


def test_evaluate_model_returns_accuracy_and_report():
    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)

    accuracy, report = evaluate_model(model, X_test, y_test)

    assert 0.0 <= accuracy <= 1.0
    assert isinstance(report, str)
    assert "precision" in report
    assert "recall" in report


def test_evaluate_model_predicts_all_test_samples():
    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy, report = evaluate_model(model, X_test, y_test)

    assert len(predictions) == len(y_test)
    assert len(predictions) == 30
    assert np.isfinite(accuracy)
