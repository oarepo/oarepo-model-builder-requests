#!/bin/bash
set -e

pytest tests/test_source_generation.py
MODEL="example_document"
MODEL_VENV=".model_venv"
#export OPENSEARCH_PORT=9400
#cd $(dirname $0)/..
if test -d $MODEL; then
	rm -rf $MODEL
fi
oarepo-compile-model ./tests/$MODEL.yaml --output-directory ./tests/$MODEL -vvv
python3 -m venv $MODEL_VENV
. $MODEL_VENV/bin/activate
pip install "./tests/$MODEL[tests]"
pytest tests/$MODEL/tests