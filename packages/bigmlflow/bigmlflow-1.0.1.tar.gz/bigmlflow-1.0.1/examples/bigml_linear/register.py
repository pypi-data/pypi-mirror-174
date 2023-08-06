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

import warnings
import json

import bigmlflow
import mlflow

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    # Read the model JSON file from the file
    model_file = "bigml_linear/linear_regression.json"
    with open(model_file) as handler:
        model = json.load(handler)

    with mlflow.start_run():
        print(
            "Registering BigML linear regression: %s\nconf: %s (%s)"
            % (
                model["object"]["name"],
                model["object"]["name_options"],
                model["resource"],
            )
        )
        bigmlflow.log_model(model, "model")
        """
        Testing example:
        curl -d '{"columns":["citric acid", "volatile acidity", "chlorides", "free sulfur dioxide","total sulfur dioxide", "pH", "sulphates", "alcohol"], "data":[[1,1,1,1,1,1,1,1]]}' \
             -H 'Content-Type: application/json; format=pandas-split' \
             -X POST localhost:5000/invocations
        """
