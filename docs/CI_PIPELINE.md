\# CI Pipeline Documentation



\## 1. Overview



This project uses GitHub Actions to implement a Continuous Integration (CI) pipeline for the MLOps Iris project. The workflow is defined in `.github/workflows/ci.yml`.



The pipeline runs when code is pushed to the `main` or `develop` branches and when a pull request targets either branch. It checks Python code quality, runs automated tests, generates test and coverage reports, and validates model accuracy.



\## 2. CI Jobs



\### 2.1 Build and Lint



\*\*Job name:\*\* `build-and-lint`



\*\*Purpose:\*\* Verify that Python source code compiles and follows the configured linting standards.



Main steps:

\- Check out the repository.

\- Set up Python 3.11.

\- Install project dependencies and Flake8.

\- Compile Python files in `src` and `tests`.

\- Run Flake8 on the source code.



\*\*Success condition:\*\* Compilation and linting complete without errors.



\### 2.2 Test Suite



\*\*Job name:\*\* `test-suite`



\*\*Dependency:\*\* `needs: build-and-lint`



\*\*Purpose:\*\* Test the data-processing pipeline and related functionality.



Main steps:

\- Check out the repository and set up Python 3.11.

\- Install project dependencies and testing tools.

\- Create the required data directories.

\- Collect the Iris dataset.

\- Preprocess the dataset.

\- Engineer features.

\- Execute the test suite with pytest.

\- Generate test results and code coverage reports.

\- Upload the reports as a GitHub Actions artifact.



The artifact is named `test-and-coverage-reports` and contains `test-results.xml` and `coverage.xml` when those files are generated.



\*\*Success condition:\*\* All tests pass.



\### 2.3 Model Quality Gate



\*\*Job name:\*\* `model-quality-gate`



\*\*Dependency:\*\* `needs: test-suite`



\*\*Purpose:\*\* Verify that the model meets the minimum acceptable accuracy requirement.



Main steps:

\- Check out the repository and set up Python 3.11.

\- Install the required dependencies.

\- Run `tests/test\_model\_quality.py`.



The normal minimum accuracy threshold is `0.90` (90%).



\*\*Success condition:\*\* The model-quality tests pass.



\## 3. Job Dependency Order



The workflow uses this sequence:



1\. `build-and-lint`

2\. `test-suite`

3\. `model-quality-gate`



The `needs` configuration ensures that `test-suite` runs only after `build-and-lint` succeeds, and `model-quality-gate` runs only after `test-suite` succeeds. If an upstream job fails, downstream jobs are skipped by default.



\## 4. Branch Protection Ruleset



The Practical 9 configuration requires a GitHub ruleset named `Protect main - CI checks` targeting the `main` branch.



The ruleset should:

\- Require changes to be submitted through a pull request.

\- Require the configured CI status checks to pass before merging.

\- Require the following checks:

&#x20; - `build-and-lint`

&#x20; - `test-suite`

&#x20; - `model-quality-gate`



Verify these settings in GitHub repository settings.



\## 5. Pull Request Verification



The workflow should also be verified using a feature branch containing a harmless README change. Open a pull request from that branch into `main` and confirm that all three CI jobs pass. Merge the pull request only after the required checks succeed.



Record the pull request and its CI results as evidence.



\## 6. Model-Quality Regression Demonstration



The regression demonstration temporarily changes the accuracy threshold in `tests/test\_model\_quality.py` from:



`MIN\_ACCEPTABLE\_ACCURACY = 0.90`



to:



`MIN\_ACCEPTABLE\_ACCURACY = 0.999`



This change must be made on a separate feature branch, not on `main`.



Expected results:

\- `build-and-lint`: passes.

\- `test-suite`: fails because the model accuracy is below the temporary threshold.

\- `model-quality-gate`: is skipped because it depends on the successful completion of `test-suite`.



Do not merge the regression pull request. After recording the failure as evidence, restore the threshold to `0.90`, verify that the normal tests pass, and remove the temporary regression branch.



\## 7. Conclusion



The GitHub Actions CI pipeline automates compilation, linting, testing, report generation, and model-quality validation. Pull-request checks and branch protection help prevent changes from being merged into `main` when required checks fail.



The successful normal pipeline run and the deliberately introduced regression demonstrate the workflow's operation and its ability to detect a model-quality threshold violation.

