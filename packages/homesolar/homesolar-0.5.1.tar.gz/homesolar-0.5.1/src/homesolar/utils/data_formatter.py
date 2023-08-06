import json
from collections.abc import MutableMapping

from loguru import logger


def parse_to_float_if_possible(string):
    result = string
    try:
        result = float(string)
    except Exception as e:
        logger.warning(f"Cannot parse to float [{e}]")
        result = parse_to_bool_if_possible(string)
    finally:
        return result


def parse_to_bool_if_possible(string):
    if string in ["true", "True"]:
        result = True
    else:
        result = string
        logger.warning("Cannot parse to boolean")
    return result


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def format_sensor_data(data):
    try:
        payload = json.loads(data["payload"])
        fields = flatten_dict(payload)
    except json.JSONDecodeError:
        fields = {"value": str(data["payload"].decode("utf-8"))}
    return {
        "measurement": data["name"],
        "fields": fields
    }


def get_sum_from_serialized_data(data):
    try:
        for table in data:
            if table["name"] == "sum":
                return table["values"][0]["value"]
    except Exception as e:
        logger.warning(f"This data doesn't have sum, returning -1 [{e}]")
        return -1
