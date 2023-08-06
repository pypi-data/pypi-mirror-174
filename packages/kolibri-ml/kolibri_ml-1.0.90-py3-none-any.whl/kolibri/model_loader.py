from typing import Optional

import pandas as pd
import os
from kolibri.config import TaskType
from kolibri.core.component import ComponentBuilder
from kolibri import __version__ as ver
from kolibri.core.modules import validate_requirements
from kolibri.metadata import Metadata
from kolibri.core.pipeline import Pipeline
from .errors import *
from pathlib import Path
from kolibri.tokenizers import *
from kolibri.features import *
from kolibri.task import *
from kolibri.autolearn.model_zoo.zoo_regressor import ZooRegressor
from  kolibri.task.tabular.regression.sklearn_regression_estimator import RegSklearnEstimator
from kdmt.lib import check_dependencies
logger = get_logger(__name__)

MINIMUM_COMPATIBLE_VERSION = "0.0.1"


class ModelLoader(object):
    """Use a trained pipeline of components to parse text documents."""

    # Defines all attributes (& default values)
    # that will be returned by `parse`
    @staticmethod
    def default_output_attributes():
        return {"label": {"name": None, "confidence": 0.0}, "entities": []}

    @staticmethod
    def ensure_model_compatibility(metadata, version_to_check=None):
        from packaging import version

        if version_to_check is None:
            version_to_check = MINIMUM_COMPATIBLE_VERSION

        model_version = metadata.get("kolibri_version", "0.0.0")
        if version.parse(model_version) < version.parse(version_to_check):
            raise UnsupportedModelError(
                "The model_type version is to old to be "
                "loaded by this nlp instance. "
                "Either retrain the model_type, or run with"
                "an older version. "
                "Model version: {} Instance version: {}"
                "".format(model_version, ver.__version__))

    @staticmethod
    def load(model_dir, component_builder=None, skip_validation=False):
        """Create an interpreter based on a persisted model_type.

        Args:
            model_dir (str): The path of the model_type to load
            component_builder (ComponentBuilder): The
                :class:`ComponentBuilder` to use.

        Returns:
            ModelLoader: An interpreter that uses the loaded model_type.
        """

        from shutil import unpack_archive
        model_dir_to_load = model_dir if model_dir[:-4] == '.tgz' else model_dir + ".tgz"
        if os.path.exists(model_dir_to_load):
            import tarfile
            tar = tarfile.open(model_dir_to_load)
            tar.extractall(path=Path(model_dir).parent)
            tar.close()

        model_metadata = Metadata.load(model_dir)

        ModelLoader.ensure_model_compatibility(model_metadata)
        return ModelLoader.create(model_metadata,
                                  component_builder,
                                  skip_validation)

    @staticmethod
    def create(model_metadata, component_builder=None, skip_validation=False):
        """Load stored model_type and components defined by the provided metadata."""

        context = {}

        if component_builder is None:
            # If no builder is passed, every interpreter creation will result
            # in a new builder. hence, no components are reused.
            component_builder = ComponentBuilder()

        steps = []

        # Before instantiating the component classes,
        # lets check if all required packages are available
        if not skip_validation:
            validate_requirements(model_metadata.component_classes)

        for component_name in model_metadata.metadata['pipeline']:
            component = component_builder.load_component(
                component_name, model_metadata.model_dir
                , **context)
            try:
                steps.append((component.name, component))
            except MissingArgumentError as e:
                raise Exception("Failed to initialize component '{}'. "
                                "{}".format(component.name, e))

        return ModelLoader(Pipeline(steps), context, model_metadata)

    def __init__(self, pipeline: Pipeline, context, model_metadata=None):
        """

        :type pipeline: Pipeline
        """
        self.pipeline = pipeline
        self.context = context if context is not None else {}
        self.model_metadata = model_metadata

    def predict(self, data):
        """Predict the input text, classify it and return pipeline result.

        The pipeline result usually contains intent and entities."""

        if data is None:
            # Not all components are able to handle empty strings. So we need
            # to prevent that... This default return will not contain all
            # output attributes of all components, but in the end, no one
            # should pass an empty string in the first place.
            output = self.default_output_attributes()
            output["text"] = ""
            return output

        output = self.pipeline.predict(data)

        if isinstance(data, pd.DataFrame):
            data_out = data.copy()
            if self.pipeline.estimator.task_type == TaskType.ANOMALY_DETECTION:
                data_out["Anomaly"] = [list(c.keys())[0] for c in output]
                data_out["score"] = [list(c.values())[0] for c in output]
            else:
                data_out["Prediction"] = output

            return data_out
        return output

    def predict_proba(self, data):
        return  self.pipeline.predict_proba(data)

    @property
    def classes(self):
        return self.pipeline.estimator.indexer.idx2token

    def fit(self, X, y, X_val=None, y_val=None):
        """Trains the underlying pipeline using the provided training texts."""

        self.pipeline.fit(X, y, X_val, y_val)

        return ModelLoader(self.pipeline, {})

    def get_component(self, component):
        for c in self.pipeline.components:
            if c.my_name == component:
                return c

        return None


    def create_api(self, api_name, host="127.0.0.1", port=8000):

        """
        This function takes an input ``estimator`` and creates a POST API for
        inference. It only creates the API and doesn't run it automatically.
        To run the API, you must run the Python file using ``!python``.


        Example
        -------


        estimator: scikit-learn compatible object
            Trained model object


        api_name: str
            Name of the model.


        host: str, default = '127.0.0.1'
            API host address.


        port: int, default = 8000
            port for API.


        Returns:
            None
        """
        check_dependencies("fastapi", severity="error")
        check_dependencies("uvicorn",  severity="error")
        check_dependencies("pydantic",  severity="error")

        target = f"{self.pipeline.estimator.get_parameter('target')}_prediction"

        query = f"""# -*- coding: utf-8 -*-

import pandas as pd
from kolibri. import load_model, predict_model
from fastapi import FastAPI
import uvicorn
from pydantic import create_model

# Create the app
app = FastAPI()

# Load trained Pipeline
model = load_model("{api_name}")

# Create input/output pydantic models
input_model = create_model("{api_name}_input", **{self.X.iloc[0].to_dict()})
output_model = create_model("{api_name}_output", {target}={repr(self.y[0])})


# Define predict function
@app.post("/predict", response_model=output_model)
def predict(data: input_model):
    data = pd.DataFrame([data.dict()])
    predictions = predict_model(model, data=data)
    return {{"{target}": predictions["prediction_label"].iloc[0]}}


if __name__ == "__main__":
    uvicorn.run(app, host="{host}", port={port})
"""

        file_name = str(api_name) + ".py"

        f = open(file_name, "w")
        f.write(query)
        f.close()

        print(
            "API successfully created. This function only creates a POST API, "
            "it doesn't run it automatically. To run your API, please run this "
            f"command --> !python {api_name}.py"
        )