import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType, Section
from oarepo_model_builder.datatypes.components import (
    DefaultsModelComponent,
    MarshmallowModelComponent,
)
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.datatypes.model import Link
from oarepo_model_builder.utils.camelcase import camel_case, snake_case
from oarepo_model_builder.utils.python_name import Import
from oarepo_model_builder.validation.utils import ImportSchema
from oarepo_model_builder.utils.links import url_prefix2link

class RequestActionSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    module = ma.fields.String(metadata={"doc": "Class module"})
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

    module = ma.fields.String(metadata={"doc": "Class module"})
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
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    allowed_receiver_ref_types = ma.fields.List(
        ma.fields.String,
        attribute="allowed-receiver-ref-types",
        data_key="allowed-receiver-ref-types",
    )
    allowed_receiver_topic_types = ma.fields.List(
        ma.fields.String,
        attribute="allowed-receiver-topic-types",
        data_key="allowed-receiver-topic-types",
    )
    generate_on_parent = ma.fields.String(
        attribute="generate-on-parent", data_key="generate-on-parent"
    )
    needs_context = ma.fields.Dict(
        keys=ma.fields.String,
        values=ma.fields.String,
        attribute="needs-context",
        data_key="needs-context",
    )

    id_ = ma.fields.String(attribute="id", data_key="id")


class ParentMarshmallowSchema(ma.Schema):
    module = ma.fields.String(metadata={"doc": "Class module"})
    class_ = ma.fields.String(
        attribute="class",
        data_key="class",
    )
    generate = ma.fields.Bool()
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "base classes"},
    )
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class ParentMarshmallowRequestSchema(ma.Schema):
    parent_field = ma.fields.String(data_key="parent-field", attribute="parent-field")
    schema_class = ma.fields.String(data_key="schema-class", attribute="schema-class")
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    module = ma.fields.String(metadata={"doc": "Class module"})
    generate = ma.fields.Bool()


class RequestSchema(ma.Schema):
    module = ma.fields.String(metadata={"doc": "Class module"})
    type = ma.fields.Nested(RequestTypeSchema)
    actions = ma.fields.Dict(
        keys=ma.fields.Str(), values=ma.fields.Nested(RequestActionSchema)
    )
    parent_schema = ma.fields.Nested(
        ParentMarshmallowRequestSchema,
        data_key="parent-marshmallow",
        attribute="parent-marshmallow",
    )


class RequestsComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, MarshmallowModelComponent]

    class ModelSchema(ma.Schema):
        requests = ma.fields.Dict(
            keys=ma.fields.Str(),
            values=ma.fields.Nested(RequestSchema),
            attribute="requests",
            data_key="requests",
        )
    def process_links(self, datatype, section: Section, **kwargs):
        url_prefix = url_prefix2link(datatype.definition["resource-config"]["base-url"])
        # TODO add link to url prefix of the record requests resource
        if datatype.root.profile == "record":
            section.config["links_item"] += [Link(
                    name="requests",
                    link_class="RecordLink",
                    link_args=[f'"{{+api}}{url_prefix}{{id}}/requests"'],
                    imports=[Import("invenio_records_resources.services.RecordLink")],
                )]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        module = datatype.definition["module"]["qualified"]
        profile_module = context["profile_module"]

        requests = set_default(datatype, "requests", {})

        for request_name, request_input_data in requests.items():
            request_module = f"{module}.{profile_module}.requests.{snake_case(request_name).replace('-', '_')}"

            # type
            request_type = request_input_data.setdefault("type", {})
            request_type_module = request_type.setdefault(
                "module", f"{request_module}.types"
            )
            request_type.setdefault(
                "class",
                f"{request_type_module}.{camel_case(request_name)}RequestType",
            )
            request_type.setdefault("generate", True)
            request_type.setdefault(
                "base-classes", ["oarepo_requests.types.generic.OARepoRequestType"]
            )  # accept action
            request_type.setdefault("id", f"{datatype.definition['module']['prefix-snake']}_{snake_case(request_name).replace('-', '_')}")
            request_type.setdefault("generate-on-parent", False)

            # parent schema
            marshmallow = request_input_data.setdefault("parent-marshmallow", {})

            marshmallow.setdefault(
                "parent-field", snake_case(request_name).replace("-", "_")
            )
            marshmallow.setdefault(
                "schema-class",
                "oarepo_requests.services.schemas.NoneReceiverGenericRequestSchema",
            )
            marshmallow.setdefault(
                "module", datatype.definition["marshmallow"]["module"]
            )
            marshmallow.setdefault("generate", True)

            # todo this needs to be updated if other types of actions are considered
            request_actions = request_input_data.setdefault("actions", {})
            for action_name, action_input_data in request_actions.items():
                request_action_module = action_input_data.setdefault(
                    "module", f"{request_module}.actions"
                )
                action_input_data.setdefault(
                    "class",
                    f"{request_action_module}.{camel_case(request_name)}RequestAcceptAction",
                )
                action_input_data.setdefault("generate", True)
                action_input_data.setdefault(
                    "base-classes", ["invenio_requests.customizations.AcceptAction"]
                )  # accept action
                action_input_data.setdefault("imports", [])
