from typing import Dict

from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.datatypes.components import UIMarshmallowModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default


class RequestsUIMarshmallowModelComponent(UIMarshmallowModelComponent):
    eligible_datatypes = [ModelDataType]
    dependency_remap = UIMarshmallowModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        super().before_model_prepare(datatype, **kwargs)
        marshmallow: Dict = set_default(datatype, "ui", "marshmallow", {})
        # TODO this is in builtin models; what is the correct approach to override this?
        append_ui_record_requests = True
        if append_ui_record_requests:
            marshmallow["base-classes"].append("oarepo_requests.services.ui_schema.UIRequestsSerializationMixin")



