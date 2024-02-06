from oarepo_model_builder.invenio.invenio_ext_setup_cfg import InvenioExtSetupCfgBuilder
from oarepo_model_builder.invenio.invenio_record_resource_setup_cfg import InvenioRecordResourceSetupCfgBuilder
from oarepo_model_builder.outputs.cfg import CFGOutput
from oarepo_model_builder.utils.python_name import split_package_base_name


class InvenioRecordRequestsResourceSetupCfgBuilder(InvenioRecordResourceSetupCfgBuilder):
    TYPE = "invenio_record_requests_resource_setup_cfg"
    def finish(self):
        super().finish()
        section = getattr(
            self.current_model,
            f"section_mb_{self.TYPE.replace('-', '_')}",
        )
        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        register_function = split_package_base_name(
            section.config["api-blueprint"]["function"]
        )

        output.add_entry_point(
            "invenio_base.api_blueprints",
            section.config["api-blueprint"]["alias"],
            f"{register_function[0]}:{register_function[-1]}",
        )

        register_function = split_package_base_name(
            section.config["api-blueprint"]["function"]
        )

        output.add_entry_point(
            "invenio_base.blueprints",
            section.config["api-blueprint"]["alias"],
            f"{register_function[0]}:{register_function[-1]}",
        )
