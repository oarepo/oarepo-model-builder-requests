#!/bin/bash
set -e

pytest tests/test_source_generation.py
MODEL="example_document"
VENV=".model_venv"
#cd $(dirname $0)/..
if test -d $MODEL; then
	rm -rf $MODEL
fi
oarepo-compile-model ./tests/$MODEL.yaml --output-directory ./tests/$MODEL -vvv
python3 -m venv $VENV
. $VENV/bin/activate
pip install "./tests/$MODEL[tests]"
pytest tests/$MODEL/tests/test_requests.py