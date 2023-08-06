"""Top-level package for AwsPClusterSlurmSpawner."""

__author__ = """ Jillian Rowe"""
__email__ = "jillian@dabbleofdevops.com"

import os

from aws_pcluster_slurm_spawner.aws_pcluster_slurm_spawner import (
    PClusterSlurmSpawner, get_ec2_address
)

pcluster_spawner_template_paths = os.path.join(os.path.dirname(__file__), "templates")

from . import _version

__version__ = _version.get_versions()["version"]
