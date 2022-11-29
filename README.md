# OARepo model builder requests
Plugin ("wrapper") for oarepo-model-builder to allow specifying requests 
tied to the model. <br>

Requests are requests for an action concerning an instance of the model (called topic), for example to publish the topic.
Applicable requests can be added to the model through "requests" section in the yaml file of the model. There can be any number of them.
<br>
Options:
<ul>
<li>
"action-class": Specify class for the accept action done by the request. 
By default, a template action class
which fetches the topic and saves it is generated. The action done on the topic has to be defined by the user.
</li>
<li>
"action-class-name": Specify the name of the generated template action class. If not specified, request name in camel case + "AcceptAction" is used.
</li>
<li>
"action-class-bases": Specify the base classes from which the 
generated template action classes inherits. 
By default it's [invenio_requests.customizations.AcceptAction].
</li>
<li>
"generate-action-class": Tell the model builder whether it should generate the accept action class templete. True by default.
</li>
<li>
RequestType allows the same customizations, the name of the properties are analogical after replacing "action" with "type".
</li>
</ul>

See model_requested_document.yaml in tests for usage example. 
What is done with the topic if the template accept action class is generated has to be specified manually in the 
requests/actions.py file.