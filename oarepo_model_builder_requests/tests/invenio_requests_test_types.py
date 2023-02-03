from oarepo_model_builder_requests.invenio.invenio_requests_builder import InvenioRequestsPythonBuilder
class InvenioRequestsTestTypesBuilder(InvenioRequestsPythonBuilder):
    TYPE = "invenio_requests_types"
    template = "requests-test-types"
    MODULE = "tests.requests_types"

