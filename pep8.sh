#!/bin/bash
VENV=${VENV:-.env}
$VENV/bin/pylint --version
$VENV/bin/pylint --rcfile=pylint.rc setup.py criticalpath
