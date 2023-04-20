#!/bin/bash
set -e

MODEL="example_document"
MODEL_VENV=".model_venv"
# export OPENSEARCH_PORT=9400
if test -d $MODEL; then
	rm -rf $MODEL
fi
oarepo-compile-model ./tests/$MODEL.yaml --output-directory ./tests/$MODEL -vvv
python3 -m venv $MODEL_VENV
. $MODEL_VENV/bin/activate
pip install -U setuptools pip wheel
pip install 'oarepo>=11.0.26,<12.0.0'
pip uninstall -y invenio_oauth2server
pip install "./tests/test_custom_classes"
pip install "./tests/$MODEL[tests]"
cp ./tests/test_custom_action.py ./tests/example_document/tests/requests/test_custom_action.py
pytest tests/$MODEL/tests