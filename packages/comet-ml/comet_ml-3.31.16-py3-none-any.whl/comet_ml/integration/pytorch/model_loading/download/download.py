# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2021 Comet ML INC
#  This file can not be copied and/or distributed without
#  the express permission of Comet ML Inc.
# *******************************************************

import pathlib

import comet_ml.api

from ... import constants
from ..uri import parse


def from_registry(MODEL_URI: str, dirpath: str) -> None:
    model_request = parse.registry(MODEL_URI)
    comet_ml.api.get_instance().download_registry_model(
        workspace=model_request.workspace,
        registry_name=model_request.registry,
        output_path=dirpath,
        version=model_request.version,
    )


def from_experiment_by_key(MODEL_URI: str, dirpath: str) -> None:
    model_request = parse.experiment_by_key(MODEL_URI)
    comet_api = comet_ml.api.get_instance()
    experiment_api = comet_api.get_experiment_by_key(model_request.experiment_key)
    assets = experiment_api.get_model_asset_list(model_name=model_request.model_name)
    pathlib.Path(dirpath, constants.MODEL_DATA_DIRECTORY).mkdir(
        parents=True, exist_ok=True
    )

    for asset in assets:
        comet_api.download_experiment_asset(
            experiment_key=model_request.experiment_key,
            asset_id=asset["assetId"],
            output_path=pathlib.Path(dirpath, asset["fileName"]),
        )


def from_experiment_by_workspace(MODEL_URI: str, dirpath: str) -> None:
    model_request = parse.experiment_by_workspace(MODEL_URI)
    comet_api = comet_ml.api.get_instance()
    experiment_api = comet_api.get(
        workspace=model_request.workspace,
        project_name=model_request.project_name,
        experiment=model_request.experiment_name,
    )
    assets = experiment_api.get_model_asset_list(model_name=model_request.model_name)
    pathlib.Path(dirpath, constants.MODEL_DATA_DIRECTORY).mkdir(
        parents=True, exist_ok=True
    )

    for asset in assets:
        comet_api.download_experiment_asset(
            experiment_key=experiment_api.key,
            asset_id=asset["assetId"],
            output_path=pathlib.Path(dirpath, asset["fileName"]),
        )
