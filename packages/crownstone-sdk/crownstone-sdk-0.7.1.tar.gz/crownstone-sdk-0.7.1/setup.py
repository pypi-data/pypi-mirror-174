#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='crownstone-sdk',
    version="0.7.1",
    packages=find_packages(exclude=["examples","testing"]),
    author="Crownstone B.V.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crownstone/crownstone-python-sdk",
    install_requires=list(package.strip() for package in open('requirements.txt')),
    scripts=[
        'tools/cs_dfu_write_application',
        'tools/cs_scan_any_crownstone',
        'tools/cs_scan_for_alternative_state',
        'tools/cs_scan_known_crownstones',
        'tools/cs_switch_crownstone',
        'tools/cs_microapp_enable',
        'tools/cs_microapp_upload',
        'tools/cs_microapp_message',
        'tools/cs_setup_crownstone',
        'tools/cs_factory_reset_crownstone',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.7',
)
