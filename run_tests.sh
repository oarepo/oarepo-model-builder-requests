#!/bin/bash
set -e

MODEL="thesis"
TESTS_VENV=".venv-tests"
CODE_TEST_DIR="tests"
BUILD_TEST_DIR="build-tests"

OAREPO_VERSION=${OAREPO_VERSION:-11}
OAREPO_VERSION_MAX=$((OAREPO_VERSION+1))

BUILDER_VENV=".venv-builder"
if test -d $BUILDER_VENV ; then
	rm -rf $BUILDER_VENV
fi

python3 -m venv $BUILDER_VENV
. $BUILDER_VENV/bin/activate
pip install -U setuptools pip wheel
pip install -e .


if test -d $BUILD_TEST_DIR; then
  rm -rf $BUILD_TEST_DIR
fi

oarepo-compile-model ./$CODE_TEST_DIR/$MODEL.yaml --output-directory ./$BUILD_TEST_DIR/$MODEL -vvv

if test -d $TESTS_VENV; then
	rm -rf $TESTS_VENV
fi

python3 -m venv $TESTS_VENV
. $TESTS_VENV/bin/activate
pip install -U setuptools pip wheel
pip install "oarepo>=$OAREPO_VERSION,<$OAREPO_VERSION_MAX"
pip install "./$BUILD_TEST_DIR/${MODEL}[tests]"
pip install "./$CODE_TEST_DIR/test_custom_classes"
cp -r ./$CODE_TEST_DIR/requests_tests ./$BUILD_TEST_DIR/$MODEL/tests/requests

pytest $BUILD_TEST_DIR/$MODEL/tests