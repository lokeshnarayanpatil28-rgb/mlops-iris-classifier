
import numpy as np
from sklearn.metrics import accuracy_score

from src.train import load_data, train_model


def test_model_accuracy_meets_minimum_threshold():
    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    assert accuracy >=  1.01


def test_model_predictions_are_valid_iris_classes():
    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)

    predictions = model.predict(X_test)

    assert set(np.unique(predictions)).issubset({0, 1, 2})


def test_model_predicts_one_label_per_sample():
    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)

    predictions = model.predict(X_test)

    assert len(predictions) == len(X_test)


def test_model_probabilities_are_valid():
    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)

    probabilities = model.predict_proba(X_test)

    assert probabilities.shape == (len(X_test), 3)
    assert np.allclose(probabilities.sum(axis=1), 1.0)
    assert np.all((probabilities >= 0.0) & (probabilities <= 1.0))
