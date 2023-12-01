from pathlib import Path

from oarepo_model_builder.utils.python_name import module_to_path

from .invenio_requests_builder_base import InvenioRequestsBuilder


class InvenioRequestsParentMarshmallowBuilder(InvenioRequestsBuilder):
    TYPE = "invenio_requests_parent_marshmallow"
    section = "parent-record-marshmallow"
    template = "requests-parent-marshmallow"

    def get_marshmallow_module(self):
        return self.current_model.definition["marshmallow"]["module"]

    def finish(self, **extra_kwargs):
        if (
            "draft-parent-record" not in self.current_model.definition
            or not self.current_model.definition["draft-parent-record"]["generate"]
        ):
            return
        vars = self.get_vars_or_none_if_no_requests()
        if not vars:
            return
        module = self.get_marshmallow_module()
        python_path = Path(module_to_path(module) + ".py")
        for request_name, request in vars["requests"].items():
            self.process_template(
                python_path,
                self.template,
                current_module=module,
                vars=vars,
                request_name=request_name.replace("-", "_"),
                request=request,
                **extra_kwargs,
            )
