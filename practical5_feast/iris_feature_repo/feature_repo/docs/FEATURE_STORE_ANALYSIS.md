# Feature Store Analysis

## Overview

Feast was implemented as the feature store for the Iris machine learning
workflow. The feature store manages the registration, storage, retrieval,
and reuse of machine learning features for both online serving and offline
model training.

The implemented workflow contains:

- `iris_measurements` - original Iris measurement features
- `iris_engineered_features` - engineered Iris features
- `iris_feature_service` - centralized feature service containing the
  registered features
- SQLite online store for low-latency feature retrieval
- Parquet-based offline source for historical feature retrieval

---

## 1. Elimination of Training-Serving Skew

One major benefit observed from using Feast is the reduction of
training-serving skew.

The same registered feature definitions are used for both offline and
online feature retrieval.

### Online retrieval

In Step 6, the features are retrieved from the Feast online store using:

```python
store.get_online_features(...)