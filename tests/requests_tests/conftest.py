import os

import pytest
from flask_principal import Identity, Need, UserNeed
from flask_security.utils import hash_password
from invenio_access.models import ActionRoles
from invenio_access.permissions import superuser_access
from invenio_accounts.models import Role
from invenio_app.factory import create_api
from invenio_records_resources.services.uow import RecordCommitOp, UnitOfWork
from invenio_requests.customizations import CommentEventType, LogEventType
from invenio_requests.proxies import current_requests
from invenio_requests.records.api import RequestEventFormat
from thesis.proxies import current_service
from thesis.records.api import ThesisRecord

APP_CONFIG = {
    "JSONSCHEMAS_HOST": "localhost",
    "RECORDS_REFRESOLVER_CLS": "invenio_records.resolver.InvenioRefResolver",
    "RECORDS_REFRESOLVER_STORE": "invenio_jsonschemas.proxies.current_refresolver_store",
    "RATELIMIT_AUTHENTICATED_USER": "200 per second",
    "SEARCH_HOSTS": [
        {
            "host": os.environ.get("OPENSEARCH_HOST", "localhost"),
            "port": os.environ.get("OPENSEARCH_PORT", "9200"),
        }
    ],
    # disable redis cache
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "OAREPO_WORKFLOWS_SET_REQUEST_PERMISSIONS": False,
    "SQLALCHEMY_ENGINE_OPTIONS": { # hack to avoid pool_timeout set in invenio_app_rdm
        "pool_pre_ping": False,
        "pool_recycle": 3600
    }
}


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return create_api


@pytest.fixture(scope="module")
def app_config(app_config):
    app_config["REQUESTS_REGISTERED_EVENT_TYPES"] = [LogEventType(), CommentEventType()]
    for k, v in APP_CONFIG.items():
        app_config[k] = v
    return app_config


@pytest.fixture(scope="module")
def identity_simple():
    """Simple identity fixture."""
    i = Identity(1)
    i.provides.add(UserNeed(1))
    i.provides.add(Need(method="system_role", value="any_user"))
    i.provides.add(Need(method="system_role", value="authenticated_user"))
    return i


@pytest.fixture(scope="module")
def identity_simple_2():
    """Simple identity fixture."""
    i = Identity(2)
    i.provides.add(UserNeed(2))
    i.provides.add(Need(method="system_role", value="any_user"))
    i.provides.add(Need(method="system_role", value="authenticated_user"))
    return i


@pytest.fixture(scope="module")
def requests_service(app):
    """Request Factory fixture."""

    return current_requests.requests_service


@pytest.fixture(scope="module")
def request_events_service(app):
    """Request Factory fixture."""
    service = current_requests.request_events_service
    return service


@pytest.fixture()
def create_request(requests_service):
    """Request Factory fixture."""

    def _create_request(identity, input_data, receiver, request_type, **kwargs):
        """Create a request."""
        # Need to use the service to get the id
        item = requests_service.create(
            identity, input_data, request_type=request_type, receiver=receiver, **kwargs
        )
        return item._request

    return _create_request


@pytest.fixture()
def submit_request(create_request, requests_service, **kwargs):
    """Opened Request Factory fixture."""

    def _submit_request(identity, data, **kwargs):
        """Create and submit a request."""
        request = create_request(identity, input_data=data, **kwargs)
        id_ = request.id
        return requests_service.execute_action(identity, id_, "submit", data)._request

    return _submit_request


@pytest.fixture(scope="module")
def users(app):
    """Create example users."""
    # This is a convenient way to get a handle on db that, as opposed to the
    # fixture, won't cause a DB rollback after the test is run in order
    # to help with test performance (creating users is a module -if not higher-
    # concern)
    from invenio_db import db

    with db.session.begin_nested():
        datastore = app.extensions["security"].datastore

        su_role = Role(name="superuser-access")
        db.session.add(su_role)

        su_action_role = ActionRoles.create(action=superuser_access, role=su_role)
        db.session.add(su_action_role)

        user1 = datastore.create_user(
            email="user1@example.org", password=hash_password("password"), active=True
        )
        user2 = datastore.create_user(
            email="user2@example.org", password=hash_password("password"), active=True
        )
        admin = datastore.create_user(
            email="admin@example.org", password=hash_password("password"), active=True
        )
        admin.roles.append(su_role)

    db.session.commit()
    return [user1, user2, admin]


@pytest.fixture(scope="function")
def request_record_input_data():
    """Input data to a Request record."""
    ret = {
        "title": "Doc1 approval",
        "payload": {
            "content": "Can you approve my document doc1 please?",
            "format": RequestEventFormat.HTML.value,
        },
    }
    return ret


@pytest.fixture(scope="function")
def example_topic(app, db, sample_metadata_list):
    # return record
    with UnitOfWork(db.session) as uow:
        record = ThesisRecord.create(sample_metadata_list[0])
        uow.register(RecordCommitOp(record, current_service.indexer, True))
        uow.commit()
        return record


@pytest.fixture
def sample_metadata_list():
    return [
        {
            "metadata": {
                "status": "Look follow unit civil too red.",
                "title": "Successful town right newspaper economy point worker green.",
            }
        },
        {
            "metadata": {
                "status": "Why opportunity available film.",
                "title": "Defense born friend it modern.",
            }
        },
        {
            "metadata": {
                "status": "Start training very order need west upon.",
                "title": "Music two color activity education build dinner.",
            }
        },
        {
            "metadata": {
                "status": "Now involve miss spring.",
                "title": "Allow usually best.",
            }
        },
        {
            "metadata": {
                "status": "Fire job community back.",
                "title": "Tend treat Democrat money yet people.",
            }
        },
        {
            "metadata": {
                "status": "Run need before final drug.",
                "title": "Our agent bag out story set hear successful.",
            }
        },
        {
            "metadata": {
                "status": "Method various war.",
                "title": "Mention subject hope tend street.",
            }
        },
        {
            "metadata": {
                "status": "Forget network shake young official tax special finally.",
                "title": "Newspaper contain action early.",
            }
        },
        {
            "metadata": {
                "status": "Doctor support provide but.",
                "title": "Last house clear run establish miss.",
            }
        },
        {
            "metadata": {
                "status": "Doctor fear participant matter base we task.",
                "title": "Politics suddenly society staff strategy.",
            }
        },
    ]
