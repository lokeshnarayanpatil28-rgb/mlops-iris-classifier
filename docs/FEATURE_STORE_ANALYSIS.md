# Feature Store Analysis

## Overview

Feast was implemented as the feature store for the Iris machine learning workflow.

The project contains two registered Feature Views:

- `iris_measurements`
- `iris_engineered_features`

The project also contains the Feature Service:

- `iris_feature_service`

The Feast workflow supports both online feature serving and historical feature retrieval.

---

## 1. Elimination of Training-Serving Skew

One important benefit of using Feast is reducing training-serving skew.

The same registered feature definitions are used for both online and offline feature retrieval.

In Step 6, the application retrieved features using:

```python
store.get_online_features(...)