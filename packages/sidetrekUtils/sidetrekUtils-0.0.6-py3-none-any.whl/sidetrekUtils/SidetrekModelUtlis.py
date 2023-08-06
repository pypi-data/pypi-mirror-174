
# -*- coding: utf-8 -*-

"""Sidetrek mlflow wrapper.
"""

# Simple calculator library


class ModelUtils:

    def __init__(self):

        tracking_uri = "https://mlflow.sidetrek.com"
        import mlflow

        # REST API
        ##################################################################
        self.create_experiment = mlflow.create_experiment
        self.list_experiments = mlflow.list_experiments
        self.search_experiments = mlflow.search_experiments
        self.get_experiment = mlflow.get_experiment
        self.get_experiment_by_name = mlflow.get_experiment_by_name
        self.delete_experiment = mlflow.delete_experiment
        # self.restore_experiment
        # self.update_experiment
        # self.create_run
        self.delete_run = mlflow.delete_run
        # self.restore_run
        self.get_run = mlflow.get_run
        self.log_metric = mlflow.log_metric
        self.log_metrics = mlflow.log_metrics
        self.set_experiment_tag = mlflow.set_experiment_tag
        self.set_experiment_tags = mlflow.set_experiment_tags
        self.set_tag = mlflow.set_tag
        self.set_tags = mlflow.set_tags
        self.delete_tag = mlflow.delete_tag
        self.log_param = mlflow.log_param
        self.log_params = mlflow.log_params
        # self.get_metric_history
        self.search_runs = mlflow.search_runs
        # self.list_artifacts
        # self.update_run
        # self.create_registeredModel
        # self.rename_registeredModel
        # self.update_registeredModel
        # self.delete_registeredModel
        # self.list_registeredModel
        # self.latest_modelVersions
        # self.create_modelVersion
        # self.get_modelVersion
        # self.update_modelVersion
        # self.delete_modelVersion
        # self.search_modelVersion
        # self.get_download_URI_for_modelVersion_artifacts
        # self.transition_modelVersion_stage
        # self.search_registeredModels
        # self.set_registered_model_tag
        # self.set_model_version_tag
        # self.data_structures

        self.ActiveRun = mlflow.ActiveRun
        self.run = mlflow.run
        self.end_run = mlflow.end_run
        self.active_run = mlflow.active_run
        self.list_run_infos = mlflow.list_run_infos
        self.start_run = mlflow.start_run
        self.search_runs = mlflow.search_runs
        self.last_active_run = mlflow.last_active_run

        # self.set_tracking_uri = mlflow.set_tracking_uri
        self.get_tracking_uri = mlflow.get_tracking_uri
        self.set_registry_uri = mlflow.set_registry_uri
        self.get_registry_uri = mlflow.get_registry_uri

        # Mlflow Client
        ##################################################################
        self.SidetrekClient = mlflow.MlflowClient
        self.SidetrekClient.tracking_uri = tracking_uri

        # Python API
        ##################################################################
        self.artifacts = mlflow.artifacts
        # self.azureml = mlflow.azureml
        self.catboost = mlflow.catboost
        self.client = mlflow.client
        # self.deployments = mlflow.deployments
        self.diviner = mlflow.diviner
        # self.entities = mlflow.entities
        self.fastai = mlflow.fastai
        self.gluon = mlflow.gluon
        self.h2o = mlflow.h2o
        self.keras = mlflow.keras
        self.lightgbm = mlflow.lightgbm
        self.mleap = mlflow.mleap
        self.models = mlflow.models
        self.onnx = mlflow.onnx
        self.paddle = mlflow.paddle
        # self.pipelines = mlflow.pipelines
        self.pmdarima = mlflow.pmdarima
        self.projects = mlflow.projects
        self.prophet = mlflow.prophet
        self.pyfunc = mlflow.pyfunc
        self.pyspark = mlflow.pyspark
        self.pytorch = mlflow.pytorch
        # self.sagemaker = mlflow.sagemaker
        self.shap = mlflow.shap
        self.sklearn = mlflow.sklearn
        self.spacy = mlflow.spacy
        self.spark = mlflow.spark
        self.statsmodels = mlflow.statsmodels
        self.tensorflow = mlflow.tensorflow
        # self.types = mlflow.types
        self.xgboost = mlflow.xgboost

    def set_tracking_uri(url):
        tracking_uri = "https://mlflow.sidetrek.com"
        from mlflow import set_tracking_uri
        set_tracking_uri(tracking_uri)
