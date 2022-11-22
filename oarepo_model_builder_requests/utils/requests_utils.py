from oarepo_model_builder.utils.camelcase import camel_case


def get_action_class_name(request):
    return getattr(request, "custom_class_name", f"{camel_case(request)}RequestAcceptAction")

def process_requests(requests):
    ret = {}
    for request_name, request_data in requests.items():
        ret[request_name] = {
            "action_class":
                getattr(request_data, "custom_class_name",
                        f"{camel_case(request_name)}RequestAcceptAction"),
            "type_class":
                f"{camel_case(request_name)}RequestType"
        }
    return ret
