from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.utils.jinja import package_name


class InvenioRequestsResolversBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_requests_resolvers"
    class_config = "requests-record-resolver-class"
    template = "requests-resolvers"

    def finish(self, **extra_kwargs):
        requests = getattr(self.schema, "requests", None)
        if not requests:
            return
        python_path = self.class_to_path(self.current_model[self.class_config])
        self.process_template(
            python_path,
            self.template,
            current_package_name=package_name(self.current_model[self.class_config]),
            **extra_kwargs,
        )
