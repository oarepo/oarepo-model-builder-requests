from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.utils.python_name import convert_config_to_qualified_name
from copy import deepcopy

import marshmallow as ma
from oarepo_model_builder.validation.utils import ImportSchema


class RequestsExtSchema(ma.Schema):
    generate = ma.fields.Bool(metadata={"doc": "Generate blueprint, defaults to true"})
    alias = ma.fields.Str(
        metadata={
            "doc": "Alias under which the blueprint will be registered in the setup.cfg"
        }
    )
    module = ma.fields.Str(metadata={"doc": "Module that will contain the blueprint"})
    function = ma.fields.Str(metadata={"doc": "Fully qualified blueprint function"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema),
        required=False,
        metadata={"doc": "Python imports"},
    )  # imports must be here as well as it is used on model's root (without field)

    class Meta:
        unknown = ma.RAISE

class RequestsExtModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        api_requests_blueprint = ma.fields.Nested(
            RequestsExtSchema,
            attribute="api-requests-blueprint",
            data_key="api-requests-blueprint",
            metadata={"doc": "API blueprint details"},
        )

    def process_mb_invenio_requests_config(self, datatype, section, **kwargs):
        cfg = section.config
        cfg["resource"] = datatype.definition["requests-record-resource"]
        cfg["service"] = datatype.definition["requests-record-service"]
        # this should? be ok here, all that's required it turn this off
        cfg["resource-config"] = deepcopy(datatype.definition["resource-config"])
        cfg["service-config"] = deepcopy(datatype.definition["service-config"])
        cfg["resource-config"]["skip"] = True
        cfg["service-config"]["skip"] = True

    def process_mb_invenio_record_requests_resource_setup_cfg(self, datatype, section, **kwargs):
        cfg = section.config
        cfg["api-blueprint"] = datatype.definition["api-requests-blueprint"]
        cfg["app-blueprint"] = datatype.definition["app-requests-blueprint"]
    def process_mb_invenio_requests_api_views(self, datatype, section, **kwargs):
        cfg = section.config
        cfg["api-blueprint"] = datatype.definition["api-requests-blueprint"]

    def process_mb_invenio_requests_app_views(self, datatype, section, **kwargs):
        cfg = section.config
        cfg["app-blueprint"] = datatype.definition["app-requests-blueprint"]

    def process_mb_invenio_requests_ext_resource(self, datatype, section, **kwargs):
        cfg = section.config
        cfg["resource"] = datatype.definition["requests-record-resource"]
        cfg["service"] = datatype.definition["requests-record-service"]

    def process_requests_ext_resource(self, datatype, section, **kwargs):
        cfg = section.config
        cfg["ext-service-name"] = "service_requests"
        cfg["ext-resource-name"] = "resource_requests"
        cfg["resource"] = datatype.definition["requests-record-resource"]
        cfg["service"] = datatype.definition["requests-record-service"]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        requests_module = "requests"

        record_requests_config_cls = "oarepo_requests.resources.draft.config.DraftRecordRequestsResourceConfig"

        alias = datatype.definition["module"]["alias"]
        requests_alias = f"{alias}_requests"
        module = datatype.definition["module"]["qualified"]

        api = set_default(datatype, "api-requests-blueprint", {})
        api.setdefault("generate", True)
        api.setdefault("alias", requests_alias)
        #api.setdefault("extra_code", "")
        api_module = api.setdefault(
            "module",
            f"{module}.views.{requests_module}.api",
        )
        api.setdefault(
            "function",
            f"{api_module}.create_api_blueprint",
        )
        api.setdefault("imports", [])
        convert_config_to_qualified_name(api, name_field="function")

        app = set_default(datatype, "app-requests-blueprint", {})
        app.setdefault("generate", True)
        app.setdefault("alias", requests_alias)
        app.setdefault("extra_code", "")
        ui_module = app.setdefault(
            "module",
            f"{module}.views.{requests_module}.app",
        )
        app.setdefault(
            "function",
            f"{ui_module}.create_app_blueprint",
        )
        app.setdefault("imports", [])
        convert_config_to_qualified_name(app, name_field="function")


        module_container = datatype.definition["module"]
        resource = set_default(datatype, "requests-record-resource", {})
        resource.setdefault("generate", True)
        resource.setdefault(
            "config-key",
            f"{module_container['base-upper']}_{requests_module.upper()}_RESOURCE_CLASS",
        )
        resource.setdefault(
            "class",
            f"oarepo_requests.resources.draft.resource.DraftRecordRequestsResource",
        )

        resource.setdefault(
            "additional-args",
            [
                "record_requests_config={{" + record_requests_config_cls + "}}()",
            ]
        )
        resource.setdefault("skip", False)

        service = set_default(datatype, "requests-record-service", {})

        service.setdefault("generate", True)
        service.setdefault(
            "config-key",
            f"{module_container['base-upper']}_{requests_module.upper()}_SERVICE_CLASS",
        )
        service.setdefault("class", f"oarepo_requests.services.draft.service.DraftRecordRequestsService")
        service.setdefault(
            "additional-args",
            [
                f"record_service=self.service_records",
            ]
        )
        service.setdefault("skip", False)
