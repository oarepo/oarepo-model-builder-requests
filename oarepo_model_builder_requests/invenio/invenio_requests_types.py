from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder_requests.utils.requests_utils import get_action_class_name, process_requests


class InvenioRequestsTypesBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_types"
    template = "requests-types"

    def finish(self, **extra_kwargs):
        requests = getattr(self.schema, "requests", None)
        if not requests:
            return
        current_module = self.settings.python.requests_types
        python_path = self.module_to_path(current_module)
        self.process_template(
            python_path,
            self.template,
            current_package_name=current_module,
            requests=process_requests(requests),
            **extra_kwargs,
        )