from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioRequestsConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_config"
    template = "requests-config"

    def finish(self, **extra_kwargs):
        requests = getattr(self.schema, "requests", None)
        if not requests:
            return
        current_module = self.settings.python.config_package
        python_path = self.module_to_path(current_module)
        self.process_template(
            python_path,
            self.template,
            current_package_name=current_module,
            requests=requests,
            **extra_kwargs,
        )
