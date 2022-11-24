from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.jinja import package_name


class InvenioRequestsViewsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_views"
    template = "requests-views"
    class_config = "create_blueprint_from_app"

    def finish(self, **extra_kwargs):
        requests = getattr(self.schema, "requests", None)
        if not requests:
            return
        python_path = self.class_to_path(self.settings.python[self.class_config])
        self.process_template(
            python_path,
            self.template,
            current_package_name=package_name(self.settings.python[self.class_config]),
            **extra_kwargs,
        )
