import copy
from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioRequestsTypesBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_types"
    template = "requests-types"

    def finish(self, **extra_kwargs):
        requests = copy.deepcopy(getattr(self.schema, "requests", {}))
        dels = []
        for request_name, request_data in requests.items():
            if not request_data.generate_type_class:
                dels.append(request_name)
        for dl in dels:
            requests.pop(dl)
        if not requests:
            return
        current_module = self.settings.python.requests_types
        python_path = self.module_to_path(current_module)
        self.process_template(
            python_path,
            self.template,
            current_package_name=current_module,
            requests=requests,
            **extra_kwargs,
        )
