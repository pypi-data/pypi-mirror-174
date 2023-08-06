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

import logging
from typing import Any, Optional

from .. import model_metadata
from ..types import ModelStateDict, Module
from . import load
from .uri import parse, scheme

LOGGER = logging.getLogger(__name__)


def load_model(
    MODEL_URI: str,
    map_location: Any = None,
    pickle_module: Optional[Module] = None,
    **torch_load_args
) -> ModelStateDict:
    if pickle_module is None:
        pickle_module = model_metadata.get_torch_pickle_module()

    if parse.request_type(MODEL_URI) == parse.RequestTypes.UNDEFINED:
        raise ValueError("Invalid MODEL_URI")

    if scheme.is_file(MODEL_URI):
        model = load.from_disk(
            MODEL_URI,
            map_location=map_location,
            pickle_module=pickle_module,
            **torch_load_args
        )
    else:
        model = load.from_remote(
            MODEL_URI,
            map_location=map_location,
            pickle_module=pickle_module,
            **torch_load_args
        )

    return model
