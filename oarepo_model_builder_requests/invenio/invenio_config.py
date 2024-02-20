from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_config"
    section = "config"
    template = "config"

    def finish(self, **extra_kwargs):
        super().finish(**extra_kwargs)
