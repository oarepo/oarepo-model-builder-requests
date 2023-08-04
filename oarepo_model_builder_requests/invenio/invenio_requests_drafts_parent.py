from pathlib import Path

from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.python_name import module_to_path


class InvenioRequestsDraftsParentBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_types"
    section = "requests"
    template = "requests-drafts-parent-field"

    def finish(self, **extra_kwargs):
        super(InvenioBaseClassPythonBuilder, self).finish() # calls super().finish() of InvenioBaseClassPythonBuilder
        vars = self.vars
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