# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 TU Wien.
#
# Invenio-Theme-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio-Theme-TUW hacks and overrides to be applied on application startup.

This module provides a blueprint whose sole purpose is to execute some code exactly
once during application startup (via ``bp.record_once()``).
These functions will be executed after the Invenio modules' extensions have been
initialized, and thus we can rely on them being already available.
"""

from flask import Blueprint
from flask.config import Config

blueprint = Blueprint("invenio_theme_tuw_hacks", __name__)


class TUWConfig(Config):
    """Override for the Flask config that evaluates the SITE_{API,UI}_URL proxies."""

    def __getitem__(self, key):
        value = super().__getitem__(key)

        # give special treatment to the URL configuration items:
        # enforce their evaluation as strings
        if key in ("SITE_UI_URL", "SITE_API_URL"):
            value = str(value)

        return value


@blueprint.record_once
def patch_app_config(state):
    # replace the app's config with our own override that evaluates
    # the LocalProxy objects set for SITE_{API,UI}_URL by casting them
    # into strings (which is their expected type)
    state.app.config = TUWConfig(state.app.config.root_path, state.app.config)
