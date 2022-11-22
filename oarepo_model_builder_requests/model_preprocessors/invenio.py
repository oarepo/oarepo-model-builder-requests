from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.utils.camelcase import camel_case
from oarepo_model_builder.utils.deepmerge import deepmerge


class InvenioModelPreprocessor(ModelPreprocessor):
    TYPE = "invenio_requests"
    def transform(self, schema, settings):
        self.set(
            settings.python,
            "requests-package",
            lambda: f"{settings.package}.requests",
        )

        self.set(
            settings.python,
            "requests-record-resolver-class",
            lambda: f"{settings.python.requests_package}.resolvers.{settings.python.record_prefix}Resolver",
        )

        self.set(
            settings.python,
            "requests-types",
            lambda: f"{settings.python.requests_package}.types",
        )

        self.set(
            settings.python,
            "requests-actions",
            lambda: f"{settings.python.requests_package}.actions",
        )
        # requests
        """
        requests = getattr(schema, "requests", None)
        if requests:
            self.set(
                settings.python,
                "requests-defined",
                lambda: True
            )

            self.set(
                settings.python,
                "requests-package",
                lambda: f"{settings.package}.requests",
            )

            self.set(
                settings.python,
                "requests-record-resolver-class",
                lambda: f"{settings.python.requests_package}.resolvers.{settings.python.record_prefix}Resolver",
            )

            self.set(
                settings.python,
                "requests-names",
                lambda: [request for request in requests]
            )

            self.set(
                settings.python,
                "requests-action-classes",
                lambda: [getattr(request, "custom_class_name", f"{camel_case(request)}RequestAcceptAction") for request
                         in requests]
            )

            self.set(
                settings.python,
                "requests-type-classes",
                lambda: [
                    f"{camel_case(request)}RequestType" for request in requests
                ]
            )
        else:
            self.set(
                settings.python,
                "requests-defined",
                lambda: False
            )
        """


