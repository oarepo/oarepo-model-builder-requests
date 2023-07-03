from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioRequestsTypesBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_types"
    section = "requests"
    template = "requests-types"
    skip_if_not_generating = False

    def finish(self, **extra_kwargs):
        super().finish(**extra_kwargs)

    def _get_output_module(self):
        module = self.current_model.definition["requests-modules"]["types-module"]
        return module
