from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioRequestsExtResourceBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_ext_resource"
    section = "ext"
    template = "requests-ext-resource"

    def finish(self, **extra_kwargs):
        ext = self.current_model.section_requests_ext_resource.config
        super().finish(ext=ext, **extra_kwargs)
