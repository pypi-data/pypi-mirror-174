import mlflow as __mlflow
# -*- coding: utf-8 -*-

"""Sidetrek mlflow wrapper.
"""
# Simple calculator library


class ModelUtils:

    def __init__(self):

        tracking_uri = "https://__mlflow.sidetrek.com"

        # REST API
        ##################################################################
        self.create_experiment = __mlflow.create_experiment
        self.list_experiments = __mlflow.list_experiments
        self.search_experiments = __mlflow.search_experiments
        self.get_experiment = __mlflow.get_experiment
        self.get_experiment_by_name = __mlflow.get_experiment_by_name
        self.delete_experiment = __mlflow.delete_experiment
        # self.restore_experiment
        # self.update_experiment
        # self.create_run
        self.delete_run = __mlflow.delete_run
        # self.restore_run
        self.get_run = __mlflow.get_run
        self.log_metric = __mlflow.log_metric
        self.log_metrics = __mlflow.log_metrics
        self.set_experiment_tag = __mlflow.set_experiment_tag
        self.set_experiment_tags = __mlflow.set_experiment_tags
        self.set_tag = __mlflow.set_tag
        self.set_tags = __mlflow.set_tags
        self.delete_tag = __mlflow.delete_tag
        self.log_param = __mlflow.log_param
        self.log_params = __mlflow.log_params
        # self.get_metric_history
        self.search_runs = __mlflow.search_runs
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

        self.ActiveRun = __mlflow.ActiveRun
        self.run = __mlflow.run
        self.end_run = __mlflow.end_run
        self.active_run = __mlflow.active_run
        self.list_run_infos = __mlflow.list_run_infos
        self.start_run = __mlflow.start_run
        self.search_runs = __mlflow.search_runs
        self.last_active_run = __mlflow.last_active_run

        # self.set_tracking_uri = __mlflow.set_tracking_uri
        self.get_tracking_uri = __mlflow.get_tracking_uri
        self.set_registry_uri = __mlflow.set_registry_uri
        self.get_registry_uri = __mlflow.get_registry_uri

        # __mlflow Client
        ##################################################################
        self.SidetrekClient = __mlflow.__mlflowClient
        self.SidetrekClient.tracking_uri = tracking_uri

        # Python API
        ##################################################################
        self.artifacts = __mlflow.artifacts
        # self.azureml = __mlflow.azureml
        self.catboost = __mlflow.catboost
        self.client = __mlflow.client
        # self.deployments = __mlflow.deployments
        self.diviner = __mlflow.diviner
        # self.entities = __mlflow.entities
        self.fastai = __mlflow.fastai
        self.gluon = __mlflow.gluon
        self.h2o = __mlflow.h2o
        self.keras = __mlflow.keras
        self.lightgbm = __mlflow.lightgbm
        self.mleap = __mlflow.mleap
        self.models = __mlflow.models
        self.onnx = __mlflow.onnx
        self.paddle = __mlflow.paddle
        # self.pipelines = __mlflow.pipelines
        self.pmdarima = __mlflow.pmdarima
        self.projects = __mlflow.projects
        self.prophet = __mlflow.prophet
        self.pyfunc = __mlflow.pyfunc
        self.pyspark = __mlflow.pyspark
        self.pytorch = __mlflow.pytorch
        # self.sagemaker = __mlflow.sagemaker
        self.shap = __mlflow.shap
        self.sklearn = __mlflow.sklearn
        self.spacy = __mlflow.spacy
        self.spark = __mlflow.spark
        self.statsmodels = __mlflow.statsmodels
        self.tensorflow = __mlflow.tensorflow
        # self.types = __mlflow.types
        self.xgboost = __mlflow.xgboost

    def set_tracking_uri(self, url: str):
        tracking_uri = "https://__mlflow.sidetrek.com"
        # from __mlflow import set_tracking_uri
        # set_tracking_uri(tracking_uri)
        ____mlflow.set_registry_uri
        print("Tracking uri can't be changed")


model_utils = ModelUtils()
