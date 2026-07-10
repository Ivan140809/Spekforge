from spekforge.models.endpoint import EndpointSpec, HTTPMethod, AuthType
from spekforge.models.param import ParamSpec, ParamLocation
from spekforge.models.schema import SchemaSpec

def test_endpoint_spec_minimal():
    endpoint = EndpointSpec(method=HTTPMethod.GET, path="/pets/{id}")

    assert endpoint.method == HTTPMethod.GET
    assert endpoint.path == "/pets/{id}"
    assert endpoint.auth == AuthType.NONE
    assert endpoint.parameters == []

def test_endpoint_spec_with_params_and_responses():
    pet_schema = SchemaSpec(
        name="Pet",
        properties={
            "id": SchemaSpec(type="integer"),
            "name": SchemaSpec(type="string"),
        },
        required=["id", "name"],
    )
    id_param= ParamSpec(name="id", location=ParamLocation.PATH, required=True, type="integer")

    endpoint = EndpointSpec(
        method=HTTPMethod.GET,
        path="/pets/{id}",
        parameters=[id_param],
        responses={"200": pet_schema},
    )

    assert endpoint.parameters[0].name == "id"
    assert endpoint.responses["200"].properties["name"].type == "string"