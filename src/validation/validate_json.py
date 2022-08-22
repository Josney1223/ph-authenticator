from jsonschema import validate, exceptions

login_schema: dict = {
    "type" : "object",
    "required": [ "username", "password" ],
    "properties" : {
        "username" : {"type" : "string"},
        "password" : {"type" : "string"}
    }
}

register_schema: dict = {
    "type" : "object",
    "required": [ "cpf", "email", "password" ],
    "properties" : {
        "cpf" : {"type" : "string"},
        "email" : {"type" : "string"},
        "password" : {"type" : "string"}
    }
}

pwd_reset_schema: dict = {
    "type" : "object",
    "required": [ "cpf", "email" ],
    "properties" : {
        "cpf" : {"type" : "string"},
        "email" : {"type" : "string"}
    }
}

def validator(request_json: dict, validator_schema: str) -> bool:
    schema: str

    if validator_schema in ("login"):
        schema = login_schema
    elif validator_schema in ("signin"):
        schema = register_schema
    elif validator_schema in ("reset_pwd"):
        schema = pwd_reset_schema
    else:
        return False

    try:
        validate(instance=request_json, schema=schema)
    except exceptions.ValidationError as err:
        return False
    except exceptions.SchemaError as err:
        raise err.args
    return True