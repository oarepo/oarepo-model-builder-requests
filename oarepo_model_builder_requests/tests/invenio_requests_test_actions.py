from oarepo_model_builder_requests.invenio.invenio_requests_builder import InvenioRequestsPythonBuilder


class InvenioRequestsTestActionsBuilder(InvenioRequestsPythonBuilder):
    TYPE = "invenio_requests_actions"
    template = "requests-test-actions"
    MODULE = "tests.requests_actions"

