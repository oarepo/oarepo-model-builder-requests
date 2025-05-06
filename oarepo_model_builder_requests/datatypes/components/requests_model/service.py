from oarepo_model_builder.datatypes import DataType, ModelDataType
from oarepo_model_builder.datatypes.components import ServiceModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default


class RequestsServiceModelComponent(ServiceModelComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [ServiceModelComponent]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile not in {"record", "draft"}:
            return
        record_service_config = set_default(datatype, "service-config", {})
        record_service_config.setdefault("components", []).append(
            "{{oarepo_requests.services.components.autorequest.AutorequestComponent}}"
        )