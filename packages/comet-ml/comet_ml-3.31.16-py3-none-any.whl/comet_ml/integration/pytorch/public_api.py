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

from . import model_logging, model_metadata
from .model_loading.entrypoint import load_model


def log_model(
    experiment, model, model_name, metadata=None, pickle_module=None, **torch_save_args
):
    state_dict = model_logging.get_state_dict(model)

    if pickle_module is None:
        pickle_module = model_metadata.get_torch_pickle_module()

    model_logging.log_comet_model_metadata(experiment, model_name, pickle_module)
    model_logging.log_state_dict(
        experiment, model_name, state_dict, metadata, pickle_module, **torch_save_args
    )
