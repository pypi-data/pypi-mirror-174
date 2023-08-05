#!/usr/bin/env python

import os
import shutil
from os import makedirs

from setuptools import setup

LXD_PROVIDER_VERSION = "1.5.0"

RELEASE_VERSION = "5"

__version__ = f"{LXD_PROVIDER_VERSION}.post{RELEASE_VERSION}"

FILE_NAME = f"terraform-provider-lxd_v{LXD_PROVIDER_VERSION}"

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None

setup(
    name="terraform-lxd-provider-wrapper",
    version=__version__,
    description="Python wrapper for Terraform Lxd Provider",
    author="Iman Azari",
    author_email="azari@mahsan.co",
    url="https://github.com/imanazari70/terraform-lxd-provider-wrapper",
    py_modules=["terraform_lxd_provider_wrapper"],
    data_files=[("lib", [f"lib/{FILE_NAME}"]), ],
    cmdclass={'bdist_wheel': bdist_wheel},
    entry_points={
        "console_scripts": [
            "tf-lxd-provider-download = "
            "terraform_lxd_provider_wrapper:download",
        ]
    },
)

package_directory = os.path.abspath(os.path.dirname(__file__))

home_directory = os.environ['HOME']
plugin_directory = f"{home_directory}/.terraform.d/plugins/" \
                   f"registry.terraform.io/terraform-lxd/lxd/" \
                   f"{LXD_PROVIDER_VERSION}/linux_amd64"
makedirs(plugin_directory, exist_ok=True)
try:
    shutil.copy2(os.path.join(package_directory, 'lib', FILE_NAME),
                 plugin_directory)
except Exception as msg:
    print(msg)
