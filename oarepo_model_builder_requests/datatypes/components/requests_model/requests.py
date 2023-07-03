import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.utils.camelcase import camel_case
from oarepo_model_builder.validation.utils import ImportSchema


class RecordResolverClassSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    generate = ma.fields.Bool()
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
    )
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
    )
    extra_code = ma.fields.Str(
        attribute="extra-code",
        data_key="extra-code",
    )
    module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    skip = ma.fields.Boolean()


class RequestActionSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    class_ = ma.fields.String(
        attribute="class",
        data_key="class",
    )
    generate = ma.fields.Bool()
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "Request action base classes"},
    )
    # module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class RequestTypeSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    class_ = ma.fields.String(
        attribute="class",
        data_key="class",
    )
    generate = ma.fields.Bool()
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "RequestType base classes"},
    )
    # module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )

    # actions = ma.fields.Dict(keys=ma.fields.Str(), values=ma.fields.Nested(RequestActionSchema))


class RequestSchema(ma.Schema):
    type = ma.fields.Nested(RequestTypeSchema)
    actions = ma.fields.Dict(
        keys=ma.fields.Str(), values=ma.fields.Nested(RequestActionSchema)
    )


# since for now i'm allowing to generate inidividual types and actions into different modules
class RequestModulesSchema(ma.Schema):
    types_module = ma.fields.String(attribute="types-module", data_key="types-module")
    actions_module = ma.fields.String(
        attribute="actions-module", data_key="actions-module"
    )


class RequestsComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        record_resolver = ma.fields.Nested(
            RecordResolverClassSchema,
            attribute="record-resolver",
            data_key="record-resolver",
        )
        requests_modules = ma.fields.Nested(
            RequestModulesSchema,
            attribute="requests-modules",
            data_key="requests-modules",
        )
        requests = ma.fields.Dict(
            keys=ma.fields.Str(),
            values=ma.fields.Nested(RequestSchema),
            attribute="requests",
            data_key="requests",
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        module = datatype.definition["module"]["qualified"]
        profile_module = context["profile_module"]

        requests_package = f"{module}.{profile_module}.requests"

        record_resolver = set_default(datatype, "record-resolver", {})
        record_resolver.setdefault("generate", True)
        resolver_module = record_resolver.setdefault(
            "module", f"{requests_package}.resolvers"
        )
        record_resolver.setdefault(
            "class",
            f"{resolver_module}.{datatype.definition['module']['prefix']}Resolver",
        )
        record_resolver.setdefault(
            "base-classes",
            ["RecordResolver"],
        )
        record_resolver.setdefault(
            "imports",
            [
                {
                    "import": "invenio_records_resources.references.RecordResolver",
                },
            ],
        )

        requests_modules = set_default(datatype, "requests-modules", {})
        request_type_module = requests_modules.setdefault(
            "types-module", f"{requests_package}.types"
        )
        request_action_module = requests_modules.setdefault(
            "actions-module", f"{requests_package}.actions"
        )

        requests = set_default(datatype, "requests", {})
        for request_name, request_input_data in requests.items():
            request_type = request_input_data.setdefault("type", {})
            request_type.setdefault(
                "class",
                f"{request_type_module}.{camel_case(request_name)}RequestType",
            )
            request_type.setdefault("generate", True)
            request_type.setdefault("base-classes", ["RequestType"])  # accept action
            request_type.setdefault(
                "imports",
                [
                    {
                        "import": "invenio_requests.customizations.RequestType",
                    },
                ],
            )
            # this needs to be updated if other types of actions are considered
            request_actions = request_input_data.setdefault("actions", {"approve": {}})
            for action_name, action_input_data in request_actions.items():
                # action_input_data.setdefault("module", request_action_module)
                action_input_data.setdefault(
                    "class",
                    f"{request_action_module}.{camel_case(request_name)}RequestAcceptAction",
                )
                action_input_data.setdefault("generate", True)
                action_input_data.setdefault(
                    "base-classes", ["AcceptAction"]
                )  # accept action
                action_input_data.setdefault(
                    "imports",
                    [
                        {
                            "import": "invenio_requests.customizations.AcceptAction",
                        },
                    ],
                )
