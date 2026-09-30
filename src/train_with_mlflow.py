"""Train multiple Iris classifier models and log them with MLflow."""

import os
from pathlib import Path

import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "iris_features.csv"


def configure_mlflow() -> None:
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)
    else:
        mlruns_dir = PROJECT_ROOT / "mlruns"
        mlruns_dir.mkdir(exist_ok=True)
        mlflow.set_tracking_uri(mlruns_dir.as_uri())
    mlflow.set_experiment("iris-classification-baseline")


def main() -> None:
    configure_mlflow()

    df = pd.read_csv(DATA_PATH)
    print("Dataset shape:", df.shape)
    print("Columns:")
    print(df.columns.tolist())

    feature_cols = [
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)",
        "sepal_area",
        "petal_area",
        "sepal_to_petal_length_ratio",
    ]
    target_col = "species"

    X = df[feature_cols].copy().fillna(df[feature_cols].median())
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df[target_col])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    models = {
        "logistic_regression": LogisticRegression(max_iter=200, C=1.0),
        "random_forest_shallow": RandomForestClassifier(
            n_estimators=50, max_depth=3, random_state=42
        ),
        "random_forest_deep": RandomForestClassifier(
            n_estimators=200, max_depth=None, random_state=42
        ),
    }

    results = []
    for model_name, model in models.items():
        print(f"\n{'=' * 60}\nTraining: {model_name}\n{'=' * 60}")

        with mlflow.start_run(run_name=model_name):
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average="macro", zero_division=0)
            recall = recall_score(y_test, y_pred, average="macro", zero_division=0)
            f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)

            mlflow.log_param("model_type", model_name)
            if model_name == "logistic_regression":
                mlflow.log_param("max_iter", model.max_iter)
                mlflow.log_param("C", model.C)
            else:
                mlflow.log_param("n_estimators", model.n_estimators)
                mlflow.log_param("max_depth", model.max_depth)

            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision_macro", precision)
            mlflow.log_metric("recall_macro", recall)
            mlflow.log_metric("f1_macro", f1)

            cm = confusion_matrix(y_test, y_pred)
            display = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_encoder.classes_)
            fig, ax = plt.subplots()
            display.plot(ax=ax)
            ax.set_title(f"Confusion Matrix - {model_name}")
            fig.tight_layout()
            cm_filename = PROJECT_ROOT / f"confusion_matrix_{model_name}.png"
            fig.savefig(cm_filename)
            plt.close(fig)

            mlflow.log_artifact(str(cm_filename), artifact_path="plots")
            mlflow.sklearn.log_model(model, artifact_path="model")

            results.append(
                {
                    "run_id": mlflow.active_run().info.run_id,
                    "model": model_name,
                    "accuracy": accuracy,
                    "precision_macro": precision,
                    "recall_macro": recall,
                    "f1_macro": f1,
                }
            )

            print("Accuracy :", accuracy)
            print("Precision:", precision)
            print("Recall   :", recall)
            print("F1 Score :", f1)

    results_df = pd.DataFrame(results)
    print(f"\n{'=' * 60}\nMODEL COMPARISON\n{'=' * 60}")
    print(results_df.to_string(index=False))

    best_model = results_df.loc[results_df["f1_macro"].idxmax()]
    print("\nBest model based on F1 score:")
    print(best_model)


if __name__ == "__main__":
    main()
