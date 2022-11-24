import copy

from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioRequestsActionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_actions"
    template = "requests-actions"

    def finish(self, **extra_kwargs):
        requests = copy.deepcopy(getattr(self.schema, "requests", {}))
        dels = []
        for request_name, request_data in requests.items():
            if not request_data.generate_action_class:
                dels.append(request_name)
        for dl in dels:
            requests.pop(dl)
        if not requests:
            return
        current_module = self.settings.python.requests_actions
        python_path = self.module_to_path(current_module)
        self.process_template(
            python_path,
            self.template,
            current_package_name=current_module,
            requests=requests,
            **extra_kwargs,
        )
