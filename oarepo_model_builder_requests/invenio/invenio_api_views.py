from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class RequestsAPIViewsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_api_views"
    section = "api-requests-blueprint"
    template = "api-views"

    def finish(self, **extra_kwargs):
        ext = self.current_model.section_requests_ext_resource.config
        super().finish(ext=ext, **extra_kwargs)
