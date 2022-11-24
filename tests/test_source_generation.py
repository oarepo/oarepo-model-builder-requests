import copy
import json
import os
import re
from io import StringIO
from pathlib import Path
from typing import Dict

import pytest
from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import AbstractFileSystem


# from tests.mock_filesystem import MockFilesystem


class MockFilesystem(AbstractFileSystem):
    def __init__(self):
        self.files: Dict[str, StringIO] = {}

    def open(self, path: str, mode: str = "r"):
        path = Path(path).absolute()
        if mode == "r":
            if not path in self.files:
                raise FileNotFoundError(
                    f"File {path} not found. Known files {[f for f in self.files]}"
                )
            return StringIO(self.files[path].getvalue())
        self.files[path] = StringIO()
        self.files[path].close = lambda: None
        return self.files[path]

    def exists(self, path):
        path = Path(path).absolute()
        return path in self.files

    def mkdir(self, path):
        pass

    def snapshot(self):
        ret = {}
        for fname, io in self.files.items():
            ret[fname] = io.getvalue()
        return ret


def remove_whitespaces(str):
    return re.sub(r"\s", "", str)


def is_in(str1, str2):
    return remove_whitespaces(str1) in remove_whitespaces(str2)


def update_dict(dct, k, *args):
    ret = copy.deepcopy(dct)
    new = {}
    for arg in args:
        new = new | arg
    ret[k] = new
    return ret


APPROVE_REQUEST = {
    "approve": {"action-class-name": "ApproveMeGoddamnAction"}
}
PUBLISH_REQUEST = {
    "publish": {}
}

ACTUALLY_APPROVE_REQUEST = {
    "actually-approve": {
        "action-class": "tests.example_model.tests.requests_classes.ActuallyApproveRecordAction",
        "generate-action-class": False,
    }
}

APPROVE_REQUEST_CUSTOM_ACTION_NAME = {
    "approve": {
        "custom-class-name": "ApproveMeAlreadyJFCAction"
    }
}

MODEL_BASE = {
    "oarepo:use": "invenio",
    "model": {
        "properties": {
            "title": {"type": "fulltext+keyword"},
            "status": {"type": "keyword"},
        }
    }
}

MODEL_ONE_REQUEST = update_dict(MODEL_BASE,
                                "requests",
                                APPROVE_REQUEST
                                )

MODEL_TWO_REQUESTS = update_dict(MODEL_BASE,
                                 "requests",
                                 APPROVE_REQUEST,
                                 PUBLISH_REQUEST,
                                 ACTUALLY_APPROVE_REQUEST,
                                 )


def generate_source(model):
    schema = load_model(
        "test.yaml",
        "test",
        model_content=model,
        isort=False,
        black=False,
    )
    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "")

    actions = builder.filesystem.open(os.path.join("test", "requests", "actions.py")).read()
    resolvers = builder.filesystem.open(os.path.join("test", "requests", "resolvers.py")).read()
    types = builder.filesystem.open(os.path.join("test", "requests", "types.py")).read()
    return actions, resolvers, types


def test_model_no_request():
    schema = load_model(
        "test.yaml",
        "test",
        model_content=MODEL_BASE,
        isort=False,
        black=False,
    )
    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)
    builder.build(schema, "")

    with pytest.raises(FileNotFoundError):
        builder.filesystem.open(os.path.join("test", "requests", "actions.py")).read()
    with pytest.raises(FileNotFoundError):
        builder.filesystem.open(os.path.join("test", "requests", "resolvers.py")).read()
    with pytest.raises(FileNotFoundError):
        builder.filesystem.open(os.path.join("test", "requests", "types.py")).read()


def test_model_one_request():
    actions, resolvers, types = generate_source(MODEL_ONE_REQUEST)
    result = """
    from invenio_requests.customizations import RequestType


from actions import ApproveRequestAcceptAction



class ApproveRequestType(RequestType):

    type_id = "approve"
    name = "Approve"

    available_actions = {
        **RequestType.available_actions,
        "accept": ApproveRequestAcceptAction
    }

    allowed_topic_ref_types = ["referenced_document_record"]
    """
    # assert is_in(result, types)
    print()


def test_model_two_requests():
    actions, resolvers, types = generate_source(MODEL_TWO_REQUESTS)
    pass


def test_model_custom_action():
    pass
