from invenio_requests.customizations import RequestType

from .request_test_actions import ActuallyApproveRecordAction


# todo what about using auto-generated actions with custom types? could generate circular dependencies
class MyTypeCustomClass(RequestType):
    type_id = "my_type"
    name = "My_type"

    available_actions = {
        **RequestType.available_actions,
        "accept": ActuallyApproveRecordAction,
    }

    allowed_topic_ref_types = ["Thesis"]
