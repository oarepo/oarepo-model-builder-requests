from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class RequestsAPPViewsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_app_views"
    section = "app-requests-blueprint"
    template = "app-views"

    def finish(self, **extra_kwargs):
        ext = self.current_model.section_requests_ext_resource.config
        super().finish(ext=ext, **extra_kwargs)