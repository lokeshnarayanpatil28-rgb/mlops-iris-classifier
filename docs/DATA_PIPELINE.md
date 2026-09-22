# Data Pipeline Documentation

## Overview

This project uses **DVC (Data Version Control)** to define, execute, cache, and reproduce the Iris data-processing pipeline.

The pipeline consists of four stages:

```text
                    dvc.yaml dependency graph

┌──────────────┐
│    Collect   │
│ collect.py   │
└──────┬───────┘
       │
       │ iris_raw.csv
       ▼
┌──────────────┐
│  Preprocess  │
│ preprocess.py│
└──────┬───────┘
       │
       │ iris_preprocessed.csv
       ▼
┌────────────────────┐
│ Feature Engineering│
│    features.py     │
└──────────┬─────────┘
           │
           │ iris_features.csv
           ▼
┌──────────────┐
│   Validate   │
│  validate.py │
└──────┬───────┘
       │
       ▼
 Validation Result
```

The dependency order is:

```text
collect → preprocess → features → validate
```

DVC uses the dependencies and outputs declared in `dvc.yaml` to determine whether a stage needs to be executed again.

---

## Pipeline Stages

| Stage               | Purpose                                           | Input                                  | Output                                 |
| ------------------- | ------------------------------------------------- | -------------------------------------- | -------------------------------------- |
| Collect             | Obtain raw Iris data                              | sklearn Iris dataset                   | `data/raw/iris_raw.csv`                |
| Preprocess          | Clean and prepare the raw data                    | `data/raw/iris_raw.csv`                | `data/processed/iris_preprocessed.csv` |
| Feature Engineering | Create useful derived features                    | `data/processed/iris_preprocessed.csv` | `data/processed/iris_features.csv`     |
| Validate            | Check schema, nulls, data types, and value ranges | `data/processed/iris_features.csv`     | Validation result                      |

---

## 1. Collect

### Purpose

The Collect stage obtains the standard Iris dataset using the `scikit-learn` dataset API and stores it as a raw CSV file.

### Script

```text
src/pipeline/collect.py
```

### Input

```text
sklearn.datasets.load_iris()
```

No local input file is required.

### Output

```text
data/raw/iris_raw.csv
```

### Expected result

The standard Iris dataset contains:

* 150 rows
* 4 original numerical measurements
* 1 target column

The collection stage logs the number of rows written to the raw dataset.

---

## 2. Preprocess

### Purpose

The Preprocess stage cleans the collected dataset and prepares it for feature engineering.

### Script

```text
src/pipeline/preprocess.py
```

### Input

```text
data/raw/iris_raw.csv
```

### Output

```text
data/processed/iris_preprocessed.csv
```

### Processing

The preprocessing stage checks and prepares the raw data before feature engineering.

The pipeline reports the number of duplicate rows removed.

For the expected Iris dataset:

```text
Dropped 0 duplicate rows
```

The resulting dataset should contain 150 rows.

---

## 3. Feature Engineering

### Purpose

The Feature Engineering stage creates additional useful features from the preprocessed Iris measurements.

### Script

```text
src/pipeline/features.py
```

### Input

```text
data/processed/iris_preprocessed.csv
```

### Output

```text
data/processed/iris_features.csv
```

### Processing

The stage derives additional features from the original Iris measurements.

The pipeline is expected to produce:

```text
9 features
```

The generated feature dataset is passed to the validation stage.

---

## 4. Validate

### Purpose

The Validate stage verifies that the generated feature dataset satisfies the expected data-quality rules.

### Script

```text
src/pipeline/validate.py
```

### Input

```text
data/processed/iris_features.csv
```

### Output

```text
Validation result
```

### Validation Rules

The validation stage checks:

1. **Schema**

   * Required columns must exist.
   * Expected feature structure must be present.

2. **Null values**

   * Required feature values must not contain unexpected null values.

3. **Data types**

   * Numerical features must contain valid numerical values.

4. **Value ranges**

   * Feature values must remain within the expected Iris dataset ranges.
   * Invalid extreme values should cause validation to fail.

5. **Row count**

   * The expected dataset contains 150 rows.

### Successful validation

A successful validation produces a message similar to:

```text
Validation PASSED: 150 rows, 9 columns, all checks satisfied
```

### Failed validation

If a value violates an enforced range or another validation rule, the validation script exits with a non-zero status code.

---

# DVC Pipeline Dependency Graph

The pipeline is defined in:

```text
dvc.yaml
```

The dependency graph is:

```text
collect
   │
   ▼
preprocess
   │
   ▼
features
   │
   ▼
validate
```

The corresponding data flow is:

```text
sklearn Iris Dataset
        │
        ▼
data/raw/iris_raw.csv
        │
        ▼
data/processed/iris_preprocessed.csv
        │
        ▼
data/processed/iris_features.csv
        │
        ▼
Validation Result
```

DVC records the state of stage dependencies and outputs in:

```text
dvc.lock
```

This allows the pipeline to be reproduced consistently.

---

# Verification & Execution

## 1. First Pipeline Run

Run:

```bash
dvc repro
```

On the first run, all four stages should execute in dependency order.

Expected output is similar to:

```text
Running stage 'collect':
> python src/pipeline/collect.py --output data/raw/iris_raw.csv
[INFO] Collected 150 rows -> data/raw/iris_raw.csv

Running stage 'preprocess':
> python src/pipeline/preprocess.py --input data/raw/iris_raw.csv --output data/processed/iris_preprocessed.csv
[INFO] Dropped 0 duplicate rows
[INFO] Preprocessed 150 rows -> data/processed/iris_preprocessed.csv

Running stage 'features':
> python src/pipeline/features.py ...
[INFO] Engineered 9 features -> data/processed/iris_features.csv

Running stage 'validate':
> python src/pipeline/validate.py ...
[INFO] Validation PASSED: 150 rows, 9 columns, all checks satisfied
```

The command should terminate with exit code `0`.

After successful execution, use:

```bash
dvc push
```

to send DVC-tracked data and pipeline outputs to the configured remote storage.

---

## 2. Second Pipeline Run

Run:

```bash
dvc repro
```

again without modifying any pipeline dependency or output.

DVC should detect that the stages have not changed and skip their execution.

Expected behavior is similar to:

```text
Stage 'collect' didn't change, skipping
Stage 'preprocess' didn't change, skipping
Stage 'features' didn't change, skipping
Stage 'validate' didn't change, skipping
```

This demonstrates DVC's **dependency-based caching** and prevents unnecessary re-execution.

---

## 3. Display the Pipeline DAG

Run:

```bash
dvc dag
```

The output should confirm the linear dependency order:

```text
collect
   ↓
preprocess
   ↓
features
   ↓
validate
```

This verifies that the stages are connected correctly through their dependencies.

---

## 4. Test Validation Failure

To verify that the validation stage correctly detects bad data, manually modify:

```text
data/processed/iris_features.csv
```

For example, change a `sepal length (cm)` value to an invalid value such as:

```text
50
```

Then run:

```bash
python src/pipeline/validate.py
```

The validation stage should:

1. Detect the out-of-range value.
2. Log a range-check error.
3. Exit with code `1`.

After testing, regenerate the correct pipeline output using:

```bash
dvc repro
```

---

## 5. DVC Lock File

After running:

```bash
dvc repro
```

DVC generates or updates:

```text
dvc.lock
```

The lock file records the exact hashes of stage dependencies and outputs.

This provides reproducibility by allowing the project to identify the precise data and pipeline state used for a successful run.

---

## Pipeline Reproducibility

The complete workflow is:

```text
             ┌───────────────────┐
             │    dvc repro      │
             └─────────┬─────────┘
                       │
                       ▼
                 ┌───────────┐
                 │  Collect  │
                 └─────┬─────┘
                       ▼
                ┌─────────────┐
                │ Preprocess  │
                └──────┬──────┘
                       ▼
               ┌────────────────┐
               │ Feature        │
               │ Engineering    │
               └───────┬────────┘
                       ▼
                ┌─────────────┐
                │  Validate   │
                └──────┬──────┘
                       │
                       ▼
              ┌──────────────────┐
              │ dvc.lock updated │
              └──────────────────┘
                       │
                       ▼
                  dvc push
                       │
                       ▼
               DVC Remote Storage
```

This provides a reproducible, dependency-aware data pipeline where changes to inputs or processing stages trigger only the necessary downstream stages.
