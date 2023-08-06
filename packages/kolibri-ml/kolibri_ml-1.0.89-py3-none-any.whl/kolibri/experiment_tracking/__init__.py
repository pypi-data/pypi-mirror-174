from kolibri.experiment_tracking.experiment_logger import ExperimentLogger
from kolibri.experiment_tracking.mlflow_logger import MlflowLogger

DefaultLogger=ExperimentLogger([MlflowLogger()])