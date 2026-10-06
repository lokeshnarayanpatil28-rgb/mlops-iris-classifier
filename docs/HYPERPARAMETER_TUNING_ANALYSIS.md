# Hyperparameter Tuning Analysis

## 1. Baseline Model

Model:
DecisionTreeClassifier

CV F1 Macro:
0.9663

Test Accuracy:
0.9000

Total Fits:
5

## 2. Grid Search

Model:
RandomForestClassifier

Total Combinations:
72

Cross-validation:
5-fold

Total Fits:
360

Best Parameters:
- max_depth = 3
- max_features = sqrt
- min_samples_split = 2
- n_estimators = 50

Best CV F1 Macro:
0.9663

Test Accuracy:
0.9667

## 3. Random Search

Model:
RandomForestClassifier

Number of Iterations:
30

Cross-validation:
5-fold

Total Fits:
150

Best Parameters:
- max_depth = 3
- max_features = sqrt
- min_samples_split = 6
- n_estimators = 100

Best CV F1 Macro:
0.9663

Test Accuracy:
0.9667

## 4. Comparison

The baseline Decision Tree achieved a test accuracy of 0.9000.

Grid Search improved the test accuracy to 0.9667 after evaluating
360 model fits.

Random Search also achieved a test accuracy of 0.9667,
but required only 150 model fits.

Both Grid Search and Random Search achieved the same CV F1 Macro
score of 0.9663.

Therefore, in this experiment, Random Search was more computationally
efficient because it achieved the same test accuracy and CV F1 Macro
as Grid Search using significantly fewer model fits.