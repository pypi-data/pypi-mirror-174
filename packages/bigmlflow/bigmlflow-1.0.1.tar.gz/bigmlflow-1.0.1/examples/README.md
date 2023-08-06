### BigMLFlow Examples

The examples in this directory illustrate how you can use `MLFlow`
to generate `BigML` models, log evaluation metrics and deploy the different
Supervised Models available in the `BigML` platform.

- `bigml_train/train.py` will create a Decision Tree in BigML and evaluate it.
  The data is extracted from the `Diabetes dataset`, that has been published
  in the `https://static.bigml.com/csv/diabetes.csv` URL.
  The `accuracy, precision and recall` will be logged and printed and the model
  will be registered for further deploy. Please, check the prerequisites
  section to ensure that the environment is correctly set up before running
  the script.
- `bigml_logistic/register.py` will register a BigML model previously
  stored in the `bigml_logistic/logistic_regression.json` file, that can be
  deployed using MLFlow to produce classification predictions.
- `bigml_ensemble/register.py` will register a BigML model previously
  stored in the `bigml_ensemble/ensemble.json` file and its inner models,
  that can be deployed using MLFlow to produce classification predictions.
- `bigml_linear/register.py` will register a linear regression model
  previously stored in the `bigml_linear/linear_regression.json` file,
  that can be deployed using MLFlow to produce regression predictions.

#### Prerequisites

Installing this `bigmlflow` library should install both `mlflow` and `bigml`
bindings, which are the only prerequisites.

NOTE: In order to run the `bigml_train/train.py` script, you need
an active account in [BigML](https://bigml.com) and your credentials
(username and [API key](https://bigml.com/account/apikey))
should be stored as environment variables
[https://bigml.readthedocs.io/en/latest/index.html?highlight=authentication#authentication](https://bigml.readthedocs.io/en/latest/index.html?highlight=authentication#authentication)
to be able to connect and use the service. You can sign in `BigML` at
[https://bigml.com/account/register](https://bigml.com/account/register) and
reproduce these examples using a free account.


#### How to run the examples

Run them as regular Python scripts.

```
python bigml_train/train.py {conf}
python bigml_logistic/register.py
python bigml_linear/register.py
python bigml_ensemble/register.py
```

The `{conf}` optional argument for the
`bigml_train/train.py` script accepts a JSON string describing the
configuration arguments for the model creation. E.g:

```
python bigml_train/train.py "{\"node_threshold\": 3}"
```

will create a 3-node Decision Tree.
