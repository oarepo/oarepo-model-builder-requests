# OARepo model builder requests
Plugin for oarepo-model-builder to allow specifying requests 
tied to the base model, based on invenio requests. <br>

Requests are requests for an action concerning an instance of the model (called 
topic in this context), 
for example to publish the topic.

The requests are specified as request types (each type has its own class). 
Each request type has pre-specified actions from the invenio framework.<br> 
The plugin allows to customize the accept action.
<br><br>
By default, along with changing the request status,
the generated accept action fetches the associated record. It's up to the 
developer to decide what to do with it further.
<br><br>
Types of requests can be added to the model through "requests" section 
in the yaml file of the model. There can be any number of them.<br>
Options in the yaml:
<ul>
<li>
"class": Class for the Type of the request. 
Used if the user wants to use a custom request type class.
</li>
<li>
"generate": True by defualt, False is 
typically used when user provides custom Type class.
</li>
<li>
"bases":
Base classes for the Type class.
</li>
<li>
"actions":
A list of customized actions by this type of request. 
Only the accept action is supported for now.
<ul>
<li>
"class": Analogous to type class for the action. By default it's [invenio_requests.customizations.AcceptAction].
</li>
<li>
"generate": Analogous to type class for the action.
</li>
<li>
"bases": Analogous to type class bases for the action.
</li>
</ul>
</li>
</ul>

See model_requested_document.yaml in tests for usage example. 
What is done with the topic if the template accept action class is generated has to be specified manually in the 
requests/actions.py file.