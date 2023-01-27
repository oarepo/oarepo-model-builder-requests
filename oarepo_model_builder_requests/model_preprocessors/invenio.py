from oarepo_model_builder.model_preprocessors import ModelPreprocessor
from oarepo_model_builder.utils.camelcase import camel_case


class InvenioModelPreprocessor(ModelPreprocessor):
    TYPE = "invenio_requests"

    def transform(self, schema, settings):
        model = schema.current_model
        self.set(
            model,
            "requests-package",
            lambda: f"{model.package}.requests",
        )

        self.set(
            model,
            "requests-record-resolver-class",
            lambda: f"{model.requests_package}.resolvers.{model.record_prefix}Resolver",
        )

        self.set(
            model,
            "requests-types",
            lambda: f"{model.requests_package}.types",
        )

        self.set(
            model,
            "requests-actions",
            lambda: f"{model.requests_package}.actions",
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
                f"{model.requests_actions}.{request_data.action_class_name}",
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
                f"{model.requests_types}.{request_data.type_class_name}",
            )
            request_data.setdefault("generate-type-class", True)
            request_data.setdefault(
                "type-class-bases", ["invenio_requests.customizations.RequestType"]
            )  # accept action

        print()
