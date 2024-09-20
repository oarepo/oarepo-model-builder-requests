from oarepo_model_builder.invenio.invenio_record_resource_setup_cfg import (
    InvenioRecordResourceSetupCfgBuilder,
)
from oarepo_model_builder.outputs.cfg import CFGOutput
from oarepo_model_builder.utils.python_name import split_package_base_name

from oarepo_model_builder_requests.invenio.record_requests_resource_setup_cfg import \
    RecordRequestsResourceSetupCfgBuilder


class RecordRequestTypesResourceSetupCfgBuilder(
    RecordRequestsResourceSetupCfgBuilder
):
    TYPE = "record_request_types_resource_setup_cfg"
    key = "record-request-types"
