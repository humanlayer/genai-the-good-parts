import json
import inspect
from datetime import datetime, timedelta
from random import randint


def get_estimated_delivery_date(tracking_number: str) -> str:
    """
    get the estimated delivery date for a package
    """
    # in reality, we'd look up the tracking number in
    # a database and get a real estimate, but for now just return a random date
    #
    #   db = sqlite.connect('orders.db')
    #   cursor = db.cursor()
    #   ...
    #
    return datetime.now() + timedelta(days=randint(1, 14))


def function_to_schema(func) -> dict:
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    parameters = {}
    for param in signature.parameters.values():
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            raise KeyError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip(),
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }


print(json.dumps(function_to_schema(get_estimated_delivery_date), indent=2))
