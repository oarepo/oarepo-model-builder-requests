from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.datatypes.components import RecordItemModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default


class RequestsRecordItemModelComponent(RecordItemModelComponent):
    eligible_datatypes = [ModelDataType]
    dependancy_remap = RecordItemModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        record_item_config = set_default(datatype, "record-item", {})
        user_components = "components" in record_item_config
        super().before_model_prepare(datatype, context=context, **kwargs)
        if not user_components:
            record_item_config.setdefault("components", [])
            record_item_config["components"] += [
                "{{oarepo_requests.services.results.RequestsComponent}}()",
                "{{oarepo_requests.services.results.RequestTypesComponent}}()",
            ]
