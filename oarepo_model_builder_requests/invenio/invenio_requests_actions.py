from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioRequestsActionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_actions"
    section = "requests"
    template = "requests-actions"
    skip_if_not_generating = False

    def _get_output_module(self):
        module = self.current_model.definition["requests-modules"]["actions-module"]
        return module
