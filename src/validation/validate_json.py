from jsonschema import Draft202012Validator, exceptions
from json import load

def validator(dictionary: dict, validator_type: str) -> bool:
    """validator _summary_
        Compara o dicionário está dentro de configurações especificadas dentro de um json.
        
        O JSON será buscado através de um alias pré-definido.

    Parameters
    ----------
    dictionary : dict
        O dicionário a ser validado
    validator_type : str
        O alias do schema com qual o dicionário deve ser validado

    Returns
    -------
    bool
        true se o dicionário está correto
        false se o dicionário está errado
    """
    schema: dict = {}
    
    if validator_type in ("login", "signin", "reset_pwd"):
        schema = get_json_schema(validator_type)
    else:
        return False
        
    try:
        Draft202012Validator(schema).validate(instance=dictionary)
    except exceptions.ValidationError as err:
        return False
    except exceptions.SchemaError as err:
        print(err.args)
    return True

def get_json_schema(validator_type: str) -> dict:
    """get_json_schema _summary_
        Busca o schema de um json válido em um arquivo.
        
        Padronização: gerar o seguinte dir
        
        ├───validation
        │   │   validator.py
        │   │   __init__.py
        │   │
        │   ├───schemas
        │   │       opcao_de_compra.json
        │   │       procuracao.json
        │   │       proposta.json
            
        Onde validator se encontra esse código e schemas se encontra os JSON de validação
        Para informações sobre gerar os JSON de validação.
        https://json-schema.org/understanding-json-schema/index.html# 
               
    Parameters
    ----------
    validator_type : str
        O alias que deve ser usado para buscar o validador

    Returns
    -------
    dict
        O schema validador
    """
    path: str = ""
    
    if validator_type in ("login"):
        path = "src/validation/schemas/login_schema.json"
    elif validator_type in ("signin"):
        path = "src/validation/schemas/register_schema.json"
    elif validator_type in ("reset_pwd"):
        path = "src/validation/schemas/pwd_reset_schema.json"
    else:
        return False
    
    with open(path, "r", encoding="utf-8") as file: 
        return load(file)    