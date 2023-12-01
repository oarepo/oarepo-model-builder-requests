from pathlib import Path

from oarepo_model_builder.utils.python_name import module_to_path

from .invenio_requests_builder_base import InvenioRequestsBuilder


class InvenioRequestsTypesBuilder(InvenioRequestsBuilder):
    TYPE = "invenio_requests_types"
    section = "requests"
    template = "requests-types"

    def finish(self, **extra_kwargs):
        vars = self.get_vars_or_none_if_no_requests()
        if not vars:
            return

        for request_name, request in vars["requests"].items():
            if not request["type"]["generate"]:
                continue
            module = request["type"]["module"]
            python_path = Path(module_to_path(module) + ".py")

            self.process_template(
                python_path,
                self.template,
                current_module=module,
                vars=vars,
                request=request,
                request_name=request_name,
                **extra_kwargs,
            )
