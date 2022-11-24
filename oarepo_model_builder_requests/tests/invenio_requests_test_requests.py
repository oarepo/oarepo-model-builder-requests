from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioRequestsTestRequestsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_tests"
    template = "requests-tests"
    MODULE = "tests.test_requests"

    def finish(self, **extra_kwargs):
        requests = getattr(self.schema, "requests", None)
        if not requests:
            return
        python_path = self.module_to_path(self.MODULE)
        self.process_template(
            python_path,
            self.template,
            requests=requests,
            **extra_kwargs,
        )
