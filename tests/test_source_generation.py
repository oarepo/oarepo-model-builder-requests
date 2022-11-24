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


def equals_sans_whitespaces(str1, str2):
    s1 = remove_whitespaces(str1)
    s2 = remove_whitespaces(str2)
    return s1 == s2


def update_dict(dct, k, *args):
    ret = copy.deepcopy(dct)
    new = {}
    for arg in args:
        new = new | arg
    ret[k] = new
    return ret


SIMPLE = {"simple": {}}

CUSTOM_ACTION_NAME = {
    "custom-action-name": {"action-class-name": "ApproveMeGoddamnAction"}
}

CUSTOM_ACTION_CLASS = {
    "custom-action": {
        "action-class": "tests.requests_actions.ActuallyApproveRecordAction",
        "generate-action-class": False,
    }
}

CUSTOM_ACTION_BASE_CLASS = {
    "custom-action-base": {
        "action-class-bases": ["tests.requests_actions.ActuallyApproveRecordAction"]
    }
}

CUSTOM_TYPE_NAME = {"custom-type-name": {"type-class-name": "MyTypeCustomName"}}

CUSTOM_TYPE_CLASS = {
    "custom-type": {
        "type-class": "tests.requests_types.MyTypeCustomClass",
        "generate-type-class": False,
    }
}

CUSTOM_TYPE_BASE_CLASS = {
    "custom-type-base": {"type-class-bases": ["tests.requests_types.MyTypeCustomClass"]}
}

MODEL_BASE = {
    "oarepo:use": "invenio",
    "model": {
        "properties": {
            "title": {"type": "fulltext+keyword"},
            "status": {"type": "keyword"},
        }
    },
}
"""
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
"""
MODEL_ALL = update_dict(
    MODEL_BASE,
    "requests",
    SIMPLE,
    CUSTOM_ACTION_NAME,
    CUSTOM_ACTION_CLASS,
    CUSTOM_ACTION_BASE_CLASS,
    CUSTOM_TYPE_NAME,
    CUSTOM_TYPE_CLASS,
    CUSTOM_TYPE_BASE_CLASS,
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

    actions = builder.filesystem.open(
        os.path.join("test", "requests", "actions.py")
    ).read()
    resolvers = builder.filesystem.open(
        os.path.join("test", "requests", "resolvers.py")
    ).read()
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

RESULT_ACTIONS = """
    from invenio_records_resources.proxies import current_service_registry
from invenio_records_resources.services.uow import RecordCommitOp
from invenio_requests.customizations import AcceptAction
from invenio_requests.resolvers.registry import ResolverRegistry

from tests.requests_actions import ActuallyApproveRecordAction


class ApproveMeGoddamnAction(AcceptAction):
    def execute(self, identity, uow):
        topic = self.request.topic.resolve()
        ## todo - do something with the record
        # topic["status"] = "accepted"
        ##
        for resolver in ResolverRegistry.get_registered_resolvers():
            if resolver.matches_entity(topic):
                topic_service = current_service_registry.get(resolver._service_id)
                break
        else:
            raise KeyError(f"topic {topic} service not found")
        uow.register(RecordCommitOp(topic, topic_service.indexer))
        super().execute(identity, uow)


class CustomActionBaseRequestAcceptAction(ActuallyApproveRecordAction):
    def execute(self, identity, uow):
        topic = self.request.topic.resolve()
        ## todo - do something with the record
        # topic["status"] = "accepted"
        ##
        for resolver in ResolverRegistry.get_registered_resolvers():
            if resolver.matches_entity(topic):
                topic_service = current_service_registry.get(resolver._service_id)
                break
        else:
            raise KeyError(f"topic {topic} service not found")
        uow.register(RecordCommitOp(topic, topic_service.indexer))
        super().execute(identity, uow)


class SimpleRequestAcceptAction(AcceptAction):
    def execute(self, identity, uow):
        topic = self.request.topic.resolve()
        ## todo - do something with the record
        # topic["status"] = "accepted"
        ##
        for resolver in ResolverRegistry.get_registered_resolvers():
            if resolver.matches_entity(topic):
                topic_service = current_service_registry.get(resolver._service_id)
                break
        else:
            raise KeyError(f"topic {topic} service not found")
        uow.register(RecordCommitOp(topic, topic_service.indexer))
        super().execute(identity, uow)


class CustomTypeNameRequestAcceptAction(AcceptAction):
    def execute(self, identity, uow):
        topic = self.request.topic.resolve()
        ## todo - do something with the record
        # topic["status"] = "accepted"
        ##
        for resolver in ResolverRegistry.get_registered_resolvers():
            if resolver.matches_entity(topic):
                topic_service = current_service_registry.get(resolver._service_id)
                break
        else:
            raise KeyError(f"topic {topic} service not found")
        uow.register(RecordCommitOp(topic, topic_service.indexer))
        super().execute(identity, uow)


class CustomTypeRequestAcceptAction(AcceptAction):
    def execute(self, identity, uow):
        topic = self.request.topic.resolve()
        ## todo - do something with the record
        # topic["status"] = "accepted"
        ##
        for resolver in ResolverRegistry.get_registered_resolvers():
            if resolver.matches_entity(topic):
                topic_service = current_service_registry.get(resolver._service_id)
                break
        else:
            raise KeyError(f"topic {topic} service not found")
        uow.register(RecordCommitOp(topic, topic_service.indexer))
        super().execute(identity, uow)


class CustomTypeBaseRequestAcceptAction(AcceptAction):
    def execute(self, identity, uow):
        topic = self.request.topic.resolve()
        ## todo - do something with the record
        # topic["status"] = "accepted"
        ##
        for resolver in ResolverRegistry.get_registered_resolvers():
            if resolver.matches_entity(topic):
                topic_service = current_service_registry.get(resolver._service_id)
                break
        else:
            raise KeyError(f"topic {topic} service not found")
        uow.register(RecordCommitOp(topic, topic_service.indexer))
        super().execute(identity, uow)
    """
RESULT_RESOLVERS = """
from invenio_records_resources.references import RecordResolver


class ExampleDocumentResolver(RecordResolver):
    # invenio_requests.registry.TypeRegistry
    # requires name of the resolver for the model; needs only to be unique for the model, so use the name of the model
    type_id = "example_document"

    """
RESULT_TYPES = """
    from example_document.requests.actions import (
    ApproveMeGoddamnAction,
    CustomActionBaseRequestAcceptAction,
    CustomTypeBaseRequestAcceptAction,
    CustomTypeNameRequestAcceptAction,
    SimpleRequestAcceptAction,
)
from invenio_requests.customizations import RequestType

from tests.requests_actions import ActuallyApproveRecordAction
from tests.requests_types import MyTypeCustomClass


class CustomActionNameRequestType(RequestType):
    type_id = "custom-action-name"
    name = "Custom-action-name"

    available_actions = {
        **RequestType.available_actions,
        "accept": ApproveMeGoddamnAction,
    }

    allowed_topic_ref_types = ["record"]  # key in topic on Request


class CustomActionRequestType(RequestType):
    type_id = "custom-action"
    name = "Custom-action"

    available_actions = {
        **RequestType.available_actions,
        "accept": ActuallyApproveRecordAction,
    }

    allowed_topic_ref_types = ["record"]  # key in topic on Request


class CustomActionBaseRequestType(RequestType):
    type_id = "custom-action-base"
    name = "Custom-action-base"

    available_actions = {
        **RequestType.available_actions,
        "accept": CustomActionBaseRequestAcceptAction,
    }

    allowed_topic_ref_types = ["record"]  # key in topic on Request


class SimpleRequestType(RequestType):
    type_id = "simple"
    name = "Simple"

    available_actions = {
        **RequestType.available_actions,
        "accept": SimpleRequestAcceptAction,
    }

    allowed_topic_ref_types = ["record"]  # key in topic on Request


class MyTypeCustomName(RequestType):
    type_id = "custom-type-name"
    name = "Custom-type-name"

    available_actions = {
        **RequestType.available_actions,
        "accept": CustomTypeNameRequestAcceptAction,
    }

    allowed_topic_ref_types = ["record"]  # key in topic on Request


class CustomTypeBaseRequestType(MyTypeCustomClass):
    type_id = "custom-type-base"
    name = "Custom-type-base"

    available_actions = {
        **RequestType.available_actions,
        "accept": CustomTypeBaseRequestAcceptAction,
    }

    allowed_topic_ref_types = ["record"]  # key in topic on Request
    """

"""
def test_generation():
    actions, resolvers, types = generate_source(MODEL_ALL)

    assert equals_sans_whitespaces(actions, RESULT_ACTIONS)
    assert equals_sans_whitespaces(resolvers, RESULT_RESOLVERS)
    assert equals_sans_whitespaces(types, RESULT_TYPES)
"""

"""
def test_model_two_requests():
    actions, resolvers, types = generate_source(MODEL_TWO_REQUESTS)
    pass


def test_model_custom_action():
    pass
"""
