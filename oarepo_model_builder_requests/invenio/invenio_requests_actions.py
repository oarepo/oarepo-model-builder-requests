from pathlib import Path

from oarepo_model_builder.datatypes.datatypes import MergedAttrDict
from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.python_name import module_to_path


class InvenioRequestsActionsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_actions"
    section = "requests"
    template = "requests-actions"
    skip_if_not_generating = False

    def finish(self, **extra_kwargs):
        if not self.generate:
            return

        section = getattr(
            self.current_model,
            f"section_mb_{self.TYPE.replace('-', '_')}",
        )

        merged = MergedAttrDict(section.config, self.current_model.definition)

        for request in merged["requests"].values():
            for action in request["actions"].values():
                module = action["module"]
                python_path = Path(module_to_path(module) + ".py")

                self.process_template(
                    python_path,
                    self.template,
                    current_module=module,
                    vars=merged,
                    **extra_kwargs,
                )
    def _get_output_module(self):
        module = self.current_model.definition["requests-modules"]["actions-module"]
        return module
