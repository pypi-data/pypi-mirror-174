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
import os

import bigmlflow
import mlflow

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def get_full_ensemble(ensemble_file):
    """Reads the ensemble information from the stored JSON file and
    looks for their component models as separate JSON files in the same
    directory. The structure and naming of files is the result of the
    api.export method in the BigML bindings:
    https://bigml.readthedocs.io/en/latest/local_resources.html?highlight=export#local-ensembles
    """
    models = []
    path = os.path.dirname(ensemble_file)
    with open(ensemble_file) as handler:
        model = json.load(handler)
        models.append(model)
    for model_id in model["object"]["models"]:
        filename = os.path.join(path, model_id.replace("/", "_"))
        with open(filename) as component_handler:
            models.append(json.load(component_handler))
    return models


if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    # Read the ensemble JSON file from the file and all the models
    # it uses
    ensemble_file = "bigml_ensemble/ensemble.json"
    ensemble_info = get_full_ensemble(ensemble_file)
    ensemble = ensemble_info[0]

    with mlflow.start_run():
        print(
            "Registering BigML ensemble: %s\nconf: %s (%s)"
            % (
                ensemble["object"]["name"],
                ensemble["object"]["name_options"],
                ensemble["resource"],
            )
        )
        bigmlflow.log_model(ensemble_info, "model")
