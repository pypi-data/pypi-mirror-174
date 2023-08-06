#!/usr/bin/env python
#
# Copyright 2022 BigML, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import pytest
import json
import pkg_resources
import pandas as pd

from pathlib import Path

from mlflow import pyfunc
from bigmlflow.bigml import save_model, load_model

from bigml.supervised import SupervisedModel
from bigml.fields import Fields


MODELS_PATH = os.path.join(
    str(Path(pkg_resources.resource_filename("bigmlflow", ".")).parents[0]),
    "tests/models",
)


def _res_filename(file):
    return os.path.join(MODELS_PATH, file)


def _local_model_check(model, examples, model_path):
    """Generic function to test local model registry, recovery and scoring"""
    local_model = SupervisedModel(model)
    predictions = [local_model.predict(example, full=True) for example in examples]
    save_model(model, path=model_path)
    loaded_model = load_model(model_path)
    loaded_model_predictions = [
        loaded_model.predict(example, full=True) for example in examples
    ]
    for index, prediction in enumerate(predictions):
        assert prediction == loaded_model_predictions[index]

    # Loading pyfunc model
    pyfunc_loaded = pyfunc.load_model(model_path)
    pyfunc_predictions = pyfunc_loaded.predict(pd.DataFrame.from_records(examples))
    for index, prediction in enumerate(predictions):
        assert pyfunc_predictions[index] == prediction


@pytest.fixture
def diabetes_examples():
    filename = _res_filename("logistic_regression.json")
    with open(filename) as handler:
        model_info = json.load(handler)
    fields = Fields(model_info)
    examples = []
    for _ in range(0, 3):
        examples.append(fields.training_data_example())
    return examples


@pytest.fixture
def wines_examples():
    filename = _res_filename("linear_regression.json")
    with open(filename) as handler:
        model_info = json.load(handler)
    fields = Fields(model_info)
    examples = []
    for _ in range(0, 3):
        examples.append(fields.training_data_example())
    return examples


@pytest.fixture
def diabetes_logistic():
    filename = _res_filename("logistic_regression.json")
    with open(filename) as handler:
        return json.load(handler)


@pytest.fixture
def diabetes_ensemble():
    model_list = []
    filename = _res_filename("ensemble.json")
    with open(filename) as handler:
        ensemble = json.load(handler)
        model_list.append(ensemble)
    try:
        for model in ensemble["object"]["models"]:
            filename = model.replace("/", "_")
            with open(_res_filename(filename)) as handler:
                model_list.append(json.load(handler))
        return model_list
    except KeyError:
        raise ValueError("This is not a correct ensemble model")


@pytest.fixture
def wines_linear():
    filename = _res_filename("linear_regression.json")
    with open(filename) as handler:
        return json.load(handler)


@pytest.fixture
def model_path(tmpdir):
    return os.path.join(str(tmpdir), "model")


def test_logistic_save_load(diabetes_logistic, diabetes_examples, model_path):
    _local_model_check(diabetes_logistic, diabetes_examples, model_path)


def test_linear_save_load(wines_linear, wines_examples, model_path):
    _local_model_check(wines_linear, wines_examples, model_path)


def test_ensemble_save_load(diabetes_ensemble, diabetes_examples, model_path):
    _local_model_check(diabetes_ensemble, diabetes_examples, model_path)
