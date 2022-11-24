from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioRequestsTestTypesBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_types"
    template = "requests-test-types"
    MODULE = "tests.requests_types"

    def finish(self, **extra_kwargs):
        requests = getattr(self.schema, "requests", None)
        if not requests:
            return
        python_path = self.module_to_path(self.MODULE)
        self.process_template(
            python_path,
            self.template,
            **extra_kwargs,
        )
