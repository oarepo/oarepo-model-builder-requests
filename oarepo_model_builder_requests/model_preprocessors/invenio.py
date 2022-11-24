from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.utils.camelcase import camel_case


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

        requests = getattr(schema.schema, "requests", {})
        for request_name, request_data in requests.items():
            # todo what if action-class-name and action-class are conflicting
            request_data.setdefault(
                "action-class-name", f"{camel_case(request_name)}RequestAcceptAction"
            )
            request_data.setdefault(
                "action-class",
                f"{settings.python.requests_actions}.{request_data.action_class_name}",
            )
            request_data.setdefault("generate-action-class", True)
            request_data.setdefault(
                "action-class-bases", ["invenio_requests.customizations.AcceptAction"]
            )  # accept action

            request_data.setdefault(
                "type-class-name", f"{camel_case(request_name)}RequestType"
            )
            request_data.setdefault(
                "type-class",
                f"{settings.python.requests_types}.{request_data.type_class_name}",
            )
            request_data.setdefault("generate-type-class", True)
            request_data.setdefault(
                "type-class-bases", ["invenio_requests.customizations.RequestType"]
            )  # accept action

        print()
