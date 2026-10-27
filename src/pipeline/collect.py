# src/pipeline/collect.py
"""
Stage 1: Data Collection.
Simulates ingesting raw data from an external source and writing
it to the raw data zone, with basic collection-time metadata logging.
"""
import argparse  # Parse command-line arguments.

# Configure logging for pipeline status messages.
import logging
from datetime import datetime, timezone

import pandas as pd
from sklearn.datasets import load_iris
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("collect")


def collect_data(output_path: str) -> pd.DataFrame:
    iris = load_iris(as_frame=True)
    # convert dataset into pandas dataframe and rename target to species
    df = iris.frame.rename(columns={"target": "species"})
    # converts 0 â†’ setosa, 1 â†’ versicolor, 2 â†’ virginica
    df["species"] = df["species"].map(dict(enumerate(iris.target_names)))
    # adds a timestamp showing when the data was collected.
    df["collected_at"] = datetime.now(timezone.utc).isoformat()

    df.to_csv(output_path, index=False)  # saves the DataFrame as a CSV file. data/raw/iris_raw.csv
    logger.info("Collected %d rows -> %s", len(df), output_path)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/raw/iris_raw.csv")
    args = parser.parse_args()
    collect_data(args.output)
