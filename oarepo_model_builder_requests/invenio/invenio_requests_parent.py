from pathlib import Path

from oarepo_model_builder.utils.python_name import module_to_path

from .invenio_requests_builder_base import InvenioRequestsBuilder


class InvenioRequestsParentBuilder(InvenioRequestsBuilder):
    TYPE = "invenio_requests_parent"
    section = "requests"
    template = "requests-parent-field"

    def finish(self, **extra_kwargs):
        if (
            "draft-parent-record" not in self.current_model.definition
            or not self.current_model.definition["draft-parent-record"]["generate"]
        ):
            return
        vars = self.get_vars_or_none_if_no_requests()
        if not vars:
            return
        module = self.current_model.definition["draft-parent-record"]["module"]
        python_path = Path(module_to_path(module) + ".py")
        for request_name in vars["requests"]:
            self.process_template(
                python_path,
                self.template,
                current_module=module,
                vars=vars,
                request_name=request_name.replace("-", "_"),
                **extra_kwargs,
            )
