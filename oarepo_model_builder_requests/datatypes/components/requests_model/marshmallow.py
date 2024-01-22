from typing import Dict

from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.datatypes.components.model.marshmallow import (
    MarshmallowModelComponent,
)
from oarepo_model_builder.datatypes.components.model.utils import set_default


class RequestsMarshmallowModelComponent(MarshmallowModelComponent):
    eligible_datatypes = [ModelDataType]
    dependency_remap = MarshmallowModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        super().before_model_prepare(datatype, context=context, **kwargs)
        marshmallow: Dict = set_default(datatype, "marshmallow", {})
        marshmallow.get("base-classes", []).append(
            "oarepo_requests.services.schema.RequestsSchemaMixin"
        )
        print()
