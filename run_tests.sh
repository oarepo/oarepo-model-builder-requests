#!/bin/bash
set -e

pytest tests/test_source_generation.py

MODEL="example_model"
cd $(dirname $0)/..
if test -d $DIR; then
	rm -rf $DIR
fi
oarepo-compile-model ./tests/$MODEL.yaml --output-directory ./tests/$MODEL -vvv
python3 -m venv .model_venv
. .model_venv/bin/activate
pip install "./tests/$MODEL[tests]"
pytest tests/example_model/tests/test_requests.py