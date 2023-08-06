#!/usr/bin/env python

"""Tests for `aws_pcluster_slurm_spawner` package."""

import unittest

from aws_pcluster_slurm_spawner import aws_pcluster_slurm_spawner
import os
from devtools import PrettyFormat, pprint, pformat, debug
from rich.console import Console
from aws_pcluster_helpers.models.config import (
    ENV_PCLUSTER_CONFIG_FILE,
    ENV_INSTANCE_TYPES_DATA_FILE,
    ENV_INSTANCE_TYPE_MAPPINGS_FILE,
)

from aws_pcluster_helpers.models.sinfo import SInfoTable, SinfoRow
from aws_pcluster_slurm_spawner.aws_pcluster_slurm_spawner import PClusterSlurmSpawner

instance_types_data_file = os.path.join(
    os.path.dirname(__file__), "instance-types-data.json"
)
instance_type_mapping_file = os.path.join(
    os.path.dirname(__file__), "instance_name_type_mappings.json"
)
pcluster_config_file = os.path.join(os.path.dirname(__file__), "pcluster_config.yml")
os.environ[ENV_INSTANCE_TYPE_MAPPINGS_FILE] = instance_type_mapping_file
os.environ[ENV_INSTANCE_TYPES_DATA_FILE] = instance_types_data_file
os.environ[ENV_PCLUSTER_CONFIG_FILE] = pcluster_config_file


def test_imports():
    from aws_pcluster_slurm_spawner import (
        PClusterSlurmSpawner,
        pcluster_spawner_template_paths,
    )

    assert os.path.exists(pcluster_spawner_template_paths)


def test_profiles():
    spawner = PClusterSlurmSpawner()
    debug(spawner.profiles_list)
    console = Console()
    console.print(spawner.sinfo.dataframe)
