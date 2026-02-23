import os

import requests

METABASE_API_KEY = os.getenv("METABASE_API_KEY")
BASE_URL = os.getenv("METABASE_BASE_URL")
headers = {
    "Content-Type": "application/json",
    "x-api-key": METABASE_API_KEY,
}

if not METABASE_API_KEY:
    raise ValueError("METABASE_API_KEY environment variable must be set.")

if not BASE_URL:
    raise ValueError("METABASE_BASE_URL environment variable must be set.")


def call_metabase_api(query_endpoint: str, method: str = "GET", data: str = ""):
    if method == "PUT":
        response = requests.put(
            f"{BASE_URL}/{query_endpoint}", headers=headers, json=data
        )
    elif method == "POST":
        response = requests.post(
            f"{BASE_URL}/{query_endpoint}", headers=headers, data=data
        )
    elif method == "GET":
        response = requests.get(f"{BASE_URL}/{query_endpoint}", headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    if response.status_code in [200, 202]:
        return response.json()
    else:
        print(
            "!!!! ERROR:", response.status_code, response.text[:30].replace("\n", " ")
        )
        return None


def get_source_table(query):
    stages = query.get("stages", [])
    if not stages:
        return None

    first_stage = stages[0]
    if not isinstance(first_stage, dict):
        return None

    return first_stage.get("source-table")


def _get_new_field_id(table, old_field_id):
    field_name = next(
        (
            field_name
            for field_name, field_id in table.old_fields.items()
            if field_id == old_field_id
        ),
        None,
    )
    if not field_name:
        field_name = get_field_name(old_field_id)

    return table.new_fields[field_name]


def get_field_name(field_id):
    query_endpoint = f"field/{field_id}"
    return call_metabase_api(query_endpoint)["name"]


def modify_field_values(data, table):
    # Check if the data is a list
    if isinstance(data, list):
        # MBQL 5 field refs are ["field", <options>, <field_id_or_name>]
        if (
            len(data) == 3
            and data[0] == "field"
            and isinstance(data[2], (int, float))
            and table.is_field_in_old_table(data[2])
        ):
            data[2] = _get_new_field_id(table, data[2])  # Modify the field id
        else:
            # Otherwise, recursively check each element of the list
            for i in range(len(data)):
                modify_field_values(data[i], table)
    elif isinstance(data, dict):
        # If it's a dictionary, iterate over its values
        for key in data:
            modify_field_values(data[key], table)
    return data
