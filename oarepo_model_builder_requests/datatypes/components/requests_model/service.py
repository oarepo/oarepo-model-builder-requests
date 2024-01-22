
from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.datatypes.components import ServiceModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default


class RequestsPatchServiceModelComponent(ServiceModelComponent):
    eligible_datatypes = [ModelDataType]
    affects = [ServiceModelComponent]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        config = set_default(datatype, "service-config", {})
        if config.get("result-item-class", None):
            self.user_value = True
        else:
            self.user_value = False

    def after_model_prepare(self, datatype, *, context, **kwargs):
        config = set_default(datatype, "service-config", {})
        if not self.user_value:
            config[
                "result-item-class"
            ] = "oarepo_requests.services.results.RequestsAwareRecordItem"
