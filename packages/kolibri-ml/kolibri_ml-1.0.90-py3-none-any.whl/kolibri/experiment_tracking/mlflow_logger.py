import secrets
import os
import tempfile

from kolibri import __version__
try:
    import mlflow
    import mlflow.sklearn
except ImportError:
    mlflow = None


def mlflow_remove_bad_chars(string: str) -> str:
    """Leaves only alphanumeric, spaces _, -, ., / in a string"""
    return "".join(c for c in string if c.isalpha() or c in ("_", "-", ".", " ", "/"))

SETUP_TAG = "Session Initialized"

class MlflowLogger():
    def __init__(self) -> None:
        if mlflow is None:
            raise ImportError(
                "MlflowLogger requires mlflow. Install using `pip install mlflow`"
            )
        super().__init__()
        self.run = None

    def init_experiment(self, exp_name_log, full_name=None):
        # get USI from nlp or tabular
        USI = secrets.token_hex(nbytes=2)

        full_name = full_name or f"{SETUP_TAG} {USI}"
        mlflow.set_experiment(exp_name_log)
        mlflow.start_run(run_name=full_name, nested=True)


    def finish_experiment(self):
        try:
            mlflow.end_run()
        except Exception:
            pass

    def log_params(self, params):
        params = {mlflow_remove_bad_chars(k): v for k, v in params.items()}
        mlflow.log_params(params)

    def log_metrics(self, metrics):
        mlflow.log_metrics(metrics)

    def set_tags(self, source, experiment_custom_tags, runtime, USI=None):
        # get USI from nlp or tabular
        if not USI:
            try:
                USI = secrets.token_hex(nbytes=2)
            except Exception:
                pass

        # Get active run to log as tag
        RunID = mlflow.active_run().info.run_id

        # set tag of compare_models
        mlflow.set_tag("Source", source)

        # set custom tags if applicable
        if isinstance(experiment_custom_tags, dict):
            mlflow.set_tags(experiment_custom_tags)

        URI = secrets.token_hex(nbytes=4)
        mlflow.set_tag("URI", URI)
        mlflow.set_tag("USI", USI)
        mlflow.set_tag("Run Time", runtime)
        mlflow.set_tag("Run ID", RunID)

    def log_artifact(self, file, type="artifact"):
        mlflow.log_artifact(file)

    def log_pandas(self, df, type="artifact"):

        with tempfile.TemporaryDirectory() as tmp_dir:

            file_path=os.path.join(tmp_dir, 'validatation_data_.xlsx')
            if df is not None:
                df.to_excel(file_path)
            self.log_artifact(file_path)

    def log_plot(self, plot, title=None):
        self.log_artifact(plot)

    def log_hpram_grid(self, html_file, title="hpram_grid"):
        self.log_artifact(html_file)

    def log_kolibri_pipeline(self, experiment, prep_pipe, model, path=None):
        # get default conda env
        from mlflow.sklearn import get_default_conda_env

        default_conda_env = get_default_conda_env()
        default_conda_env["name"] = f"{experiment.experiment_name}-env"
        default_conda_env.get("dependencies").pop(-3)
        dependencies = default_conda_env.get("dependencies")[-1]

        dep = f"kolibri-ml=={__version__}"
        dependencies["pip"] = [dep]

        directory=experiment.config["output-folder"]
        for root, dirs, files in os.walk(directory):
            for filename in files:
                filre_path=os.path.join(root, filename)
                dir_relative= os.path.relpath(root, start=directory)
                if dir_relative=='.':
                    dir_relative=None

                mlflow.tracking.fluent.log_artifact(filre_path, dir_relative)

