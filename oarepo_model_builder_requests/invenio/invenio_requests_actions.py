from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder

from oarepo_model_builder_requests.utils.requests_utils import process_requests


class InvenioRequestsActionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_actions"
    template = "requests-actions"
    """
    def build(self, schema):
        self.begin(schema.schema, schema.settings)

        for proc in self.property_preprocessors:
            proc.begin(schema, schema.settings)

        try:
            processing_order = self.schema.schema.processing_order
        except AttributeError:
            processing_order = None

        self.build_children(ordering=processing_order)

        for proc in self.property_preprocessors:
            proc.finish()

        self.finish()
    """
    def finish(self, **extra_kwargs):
        requests = getattr(self.schema, "requests", None)
        if not requests:
            return
        current_module = self.settings.python.requests_actions
        python_path = self.module_to_path(current_module)
        self.process_template(
            python_path,
            self.template,
            current_package_name=current_module,
            requests=process_requests(requests),
            **extra_kwargs,
        )


