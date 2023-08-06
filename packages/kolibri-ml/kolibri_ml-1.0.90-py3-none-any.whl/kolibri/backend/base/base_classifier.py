import gc

import numpy as np
import pandas as pd

from kolibri.backend.base.base_estimator import BaseEstimator
from kolibri.visualizations.classification_plots import ClassificationPlots

try:
    from kolibri.explainers.shap_explainer import PlotSHAP
except:
    pass

from kolibri.config import TaskType
from kolibri.config import ParamType
from sklearn.calibration import CalibratedClassifierCV
from kolibri.logger import get_logger
from kolibri import default_configs as settings
import time
import datetime
from sklearn.model_selection import StratifiedKFold
from kdmt.df import color_df
from kolibri.evaluation.metrics import classification
from kolibri.indexers.label_indexer import LabelIndexer
logger = get_logger(__name__)
from kolibri.output import DefaultDisplay

KOLIBRI_MODEL_FILE_NAME = "classifier_kolibri.pkl"



class BaseClassifier(BaseEstimator):
    """
    This is an abstract class.
    All estimators inherit from BaseEstimator.
    The notion of Estimator represents any mathematical model_type that estimate a response function. In machine learning it can represent either
    a supervised or unsupervised classification algorithm.

    Estimators have the following paramters that can be modified using the configuration object.

    Fixed Hyperparameters
    ---------------------
    base-estimator: a defined kolibri or sklearn.BaseEstimator (default=LogisticRegression)
        This is used by kolibri.bakend.meta estimators as a base estimator for each member of the ensemble is an instance of the base estimator

    explain : boolean (default=False)
        used to output an explanation file in the output folder.

    sampler: str (default=None), A sampler such as SMOTE can be used to balance the data in case the dataset is heavily unbalanced.
    see kolibri.samplers for various options that can be used.

    "priors-thresolding":boolean (default=False), a strategy to handle unbalanced dataset, by class prior probability.

    evaluate-performance: boolean (default=False), use this config to generate performance data before training the model_type.

    optimize-estimator: boolean (default=False), use this config to optimise the parameters of the estimtors. the optimisation stategy optimised the tunable parameters.

    Tunable Hyperparameters
    ---------------------

    These hyper parameters are used in optimization strategies to optimize the performances.
    one obvious parameter to optimise is the base model_type used to train the data.

    """

    short_name = "Unknown"

    component_type = "estimator"

    provides = ["classification", "target_ranking"]

    requires = ["text_features"]

    defaults = {
            "fixed": {
                "target": None,
                "sampler": None,
                "priors-thresolding": False,
                'calibrate-model':False,
                'calibration-method': "isotonic",
            },
            "tunable": {
                "model-param": {
                    "description": "This is just an example of a tuneable variable",
                    "value": "logreg",
                    "type": ParamType.CATEGORICAL,
                }

            }
        }

    def __init__(self, params, model=None, indexer=None):
        super().__init__(params=params, model=model)
        if indexer is not None:
            self.indexer = indexer
        else:
            self.indexer = LabelIndexer(multi_label=False)
        self.sampler=None

        self.X_sampled = None
        self.y_sampled = None

        if self.get_parameter('sampler'):
            from kolibri.samplers import get_sampler
            self.sampler = get_sampler(self.get_parameter('sampler'))

        self.class_priors = None
        self.all_plots = {
            "pipeline": "Pipeline Plot",
            "roc": "ROC",
            "confusion_matrix": "Confusion Matrix",
            "threshold": "Threshold",
            "pr": "Precision Recall",
            "error": "Prediction Error",
            "class_report": "Class Report",
            "class_distribution": "Class Distribution",
            "score_distribution": "Score distribution",
            "errors": "Classification Errors",
            "tree": "Decision tree based visualization",
            "tsne": "TSNE Visualization",
            "umap": "UMAP based visualization",
            "calibration": "Probability Calibration Plot"
        }

    def fit(self, data_X = None, data_y = None, X_val=None, y_val=None):
        self._is_multi_class=len(set(data_y))>2

        runtime_start = time.time()
        full_name = type(self.model).__name__

#        self.display.move_progress()

        """
        MONITOR UPDATE STARTS
        """

        model_fit_time, model_results, avg_results, predictions = self._create_and_evaluate_model(data_X, data_y)

        if predictions != []:
            if len(predictions.shape)>1 and predictions.shape[1] > 1:
                predictions = np.column_stack((self.indexer.inverse_transform(np.argmax(predictions, axis=1)) ,predictions))
            elif len(predictions.shape)==1 or predictions.shape[1] == 1:
                if self.indexer is not None:
                    predictions = self.indexer.inverse_transform(predictions)
        # dashboard logging
        indices = "Mean"

#        self.display.move_progress()

        logger.info("Uploading results into container")


        if model_results is not None:
            # yellow the mean
            model_results_ = color_df(model_results, "yellow", indices, axis=1)
            model_results_ = model_results_.format(precision=self.get_parameter("round"))
            self.display.display(model_results_)

        # end runtime
        runtime_end = time.time()
        runtime = np.array(runtime_end - runtime_start).round(self.get_parameter("round"))




        logger.info(str(self.model))
        logger.info(
            "create_model() successfully completed......................................"
        )
        gc.collect()
#        self.display.close()
#        self.display=None

        self.y_true=data_y
        self.X=data_X
        predictions=np.array(predictions)
        if predictions!=[] and len(predictions.shape)==1:
            self.y_pred=predictions
        else:
            self.y_pred= [] if predictions==[] else predictions[:,1:,].astype(np.float16)

        self.plotter = ClassificationPlots(y_true=self.y_true, y_pred=self.y_pred, labels_dict=self.indexer.idx2token, X=self.X, y=self.y_true, classifier=self.model)

        return model_results, runtime, model_fit_time, predictions

    def _get_models(self):
        from kolibri.backend.models import sklearn_classification_models
        return sklearn_classification_models

    def _get_model(self, model):
        from kolibri.backend.models import get_model
        return get_model(model, task_type = TaskType.CLASSIFICATION)


    def _get_metrics(self):
        return classification.get_all_metrics()

    def calibrate(
        self,
            X, y,
        method: str = "sigmoid",
        fit_kwargs = None,
    ):

        """
        This function calibrates the probability of a given estimator using isotonic
        or logistic regression. The output of this function is a score grid with CV
        scores by fold. Metrics evaluated during CV can be accessed using the
        ``get_metrics`` function. Custom metrics can be added or removed using
        ``add_metric`` and ``remove_metric`` function. The ouput of the original estimator
        and the calibrated estimator (created using this function) might not differ much.
        In order to see the calibration differences, use 'calibration' plot in ``plot_model``
        to see the difference before and after.


        Example
        -------


        estimator: scikit-learn compatible object
            Trained model object


        method: str, default = 'sigmoid'
            The method to use for calibration. Can be 'sigmoid' which corresponds to
            Platt's method or 'isotonic' which is a non-parametric approach.


        calibrate_fold: integer or scikit-learn compatible CV generator, default = 5
            Controls internal cross-validation. Can be an integer or a scikit-learn
            CV generator. If set to an integer, will use (Stratifed)KFold CV with
            that many folds. See scikit-learn documentation on Stacking for
            more details.


        fold: int or scikit-learn compatible CV generator, default = None
            Controls cross-validation. If None, the CV generator in the ``fold_strategy``
            parameter of the ``setup`` function is used. When an integer is passed,
            it is interpreted as the 'n_splits' parameter of the CV generator in the
            ``setup`` function.


        round: int, default = 4
            Number of decimal places the metrics in the score grid will be rounded to.


        fit_kwargs: dict, default = {} (empty dict)
            Dictionary of arguments passed to the fit method of the model.


        groups: str or array-like, with shape (n_samples,), default = None
            Optional group labels when GroupKFold is used for the cross validation.
            It takes an array with shape (n_samples, ) where n_samples is the number
            of rows in training dataset. When string is passed, it is interpreted as
            the column name in the dataset containing group labels.


        verbose: bool, default = True
            Score grid is not printed when verbose is set to False.


        return_train_score: bool, default = False
            If False, returns the CV Validation scores only.
            If True, returns the CV training scores along with the CV validation scores.
            This is useful when the user wants to do bias-variance tradeoff. A high CV
            training score with a low corresponding CV validation score indicates overfitting.


        Returns:
            Trained Model


        Warnings
        --------
        - Avoid isotonic calibration with too few calibration samples (< 1000) since it
        tends to overfit.

        """

        function_params_str = ", ".join([f"{k}={v}" for k, v in locals().items()])

        logger.info("Initializing calibrate_model()")
        logger.info(f"calibrate_model({function_params_str})")

        logger.info("Checking exceptions")

        # run_time
        runtime_start = time.time()

        if not fit_kwargs:
            fit_kwargs = {}

        # checking round parameter
        if type(round) is not int:
            raise TypeError("Round parameter only accepts integer value.")

        """

        ERROR HANDLING ENDS HERE

        """

        fold = StratifiedKFold(self.get_parameter("n-folds"))


        logger.info("Preloading libraries")

        # pre-load libraries

        logger.info("Preparing display monitor")

        progress_args = {"max": 2 + 4}
        timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
        monitor_rows = [
            ["Initiated", ". . . . . . . . . . . . . . . . . .", timestampStr],
            [
                "Status",
                ". . . . . . . . . . . . . . . . . .",
                "Loading Dependencies",
            ],
            [
                "Estimator",
                ". . . . . . . . . . . . . . . . . .",
                "Compiling Library",
            ],
        ]
        display = DefaultDisplay(
            verbose=True,
            html_param=True,
            progress_args=progress_args,
            monitor_rows=monitor_rows,
        )

        np.random.seed(self.get_parameter("seed"))

        probability_threshold = None


        logger.info("Getting model name")

        full_name = str(self.model)

        logger.info(f"Base model : {full_name}")

        display.update_monitor(2, full_name)

        """
        MONITOR UPDATE STARTS
        """

        display.update_monitor(1, "Selecting Estimator")

        """
        MONITOR UPDATE ENDS
        """

        # calibrating estimator

        logger.info("Importing untrained CalibratedClassifierCV")

        calibrated_model=CalibratedClassifierCV(self.model, cv=fold, method=method)

        display.move_progress()

        logger.info(
            "SubProcess create_model() called =================================="
        )
        self._create_and_evaluate_model()
        self.model= calibrated_model.fit(X, y)


    def compute_priors(self, y):
        unique, counts = np.unique(y, return_counts=True)
        self.class_priors = dict(zip(unique, counts))

        total = sum(self.class_priors.values(), 0.0)
        self.class_priors = {k: v / total for k, v in self.class_priors.items()}

    def _predict_proba(self, X):
        """Given a bow vector of an input text, predict the class label.

        Return probabilities for all y_values.

        :param X: bow of input text
        :return: vector of probabilities containing one entry for each label"""
        raw_predictions=None
        try:
            if self.get_parameter('task-type') == TaskType.BINARY_CLASSIFICATION:
                raw_predictions=self.model.predict_proba(X)[:, 1]
            elif self.get_parameter('task-type') == TaskType.CLASSIFICATION:
                raw_predictions=self.model.predict_proba(X)
        except:
            raise Exception('Predict_proba raised an error in Estimator')


        if self.get_parameter("priors-thresolding"):
            if not raw_predictions is None:
                try:
                    priors = np.array([v for v in self.class_priors.values()])
                    raw_predictions = (raw_predictions.T - priors[:, None]) / priors[:, None]
                    raw_predictions = np.argmax(raw_predictions.T, axis=1)
                except Exception as e:
                    print(e)

        # sort the probabilities retrieving the indices of
        # the elements in sorted order
        sorted_indices = np.fliplr(np.argsort(raw_predictions, axis=1))

        return raw_predictions, sorted_indices, [p[sorted_indices[i]] for i, p in enumerate(raw_predictions)]

    def predict_proba(self, X):
        return self.model.predict_proba(X)
    def predict(self, X):
        """Given a bow vector of an input text, predict most probable label.

        Return only the most likely label.

        :param X: bow of input text
        :return: tuple of first, the most probable label and second,
                 its probability."""
        probabilities=[]
        try:
            raw_predictions, class_ids, probabilities=self._predict_proba(X)
        except:
            class_ids=self.model.predict(X)

        classes = [self.indexer.inverse_transform(np.ravel(class_id)) for class_id in class_ids]

        return self.process([list(zip(classe, probability)) for classe, probability in zip(classes, probabilities)])

    def process(self, results):

        if results is not None:
            ranking= [result[:settings.TARGET_RANKING_LENGTH] for result in results]

            target = [{"name": result[0][0], "confidence": result[0][1]} for result in results]

            target_ranking = [[{"name":r[0], "confidence":r[1]} for r in rank] for rank in ranking]
        else:
            target = {"name": None, "confidence": 0.0}
            target_ranking = []


        response={
            "label": target,
            "ranking": target_ranking
        }
        return response
    def explain(self, **kwargs):


        # soft dependencies check

        dashboard_kwargs =  {"shap_interaction":False, "nsamples":500, "whatif":False}
        run_kwargs = {"port":3050}

        from explainerdashboard import ExplainerDashboard, RegressionExplainer

        # Replaceing chars which dash doesnt accept for column name `.` , `{`, `}`
        X = pd.DataFrame(self.X)

        X.columns = self.feature_names
        explainer = RegressionExplainer(
            self.model, X, pd.Series(self.y_true), **kwargs
        )
        db= ExplainerDashboard(
            explainer, **dashboard_kwargs
        )
        db.run(**run_kwargs)

if __name__=="__main__":
    import joblib
    cl=BaseClassifier({"model": 'LogisticRegression'})
    joblib.dump(cl, './test.pkl')