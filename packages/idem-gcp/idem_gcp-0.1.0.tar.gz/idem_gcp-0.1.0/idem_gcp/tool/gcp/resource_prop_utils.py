import copy
from typing import Dict
from typing import List
from typing import Set

import yaml
from importlib_resources import files


def __init__(hub):
    file_text = (
        files("idem_gcp.resources")
        .joinpath("properties.yaml")
        .read_text(encoding="utf-8")
    )
    hub.tool.gcp.RESOURCE_PROPS = yaml.safe_load(file_text)


resource_id_delimiter = "^^^"


def get_create_properties(hub, resource_type: str, convert_to_present=True) -> Set:
    resource_methods_properties = hub.tool.gcp.RESOURCE_PROPS[resource_type]
    raw_props = set(
        resource_methods_properties.get("insert", {})
        or resource_methods_properties.get("create", {})
    )
    if raw_props and convert_to_present:
        return hub.tool.gcp.conversion_utils.convert_raw_properties_to_present(
            raw_props
        )
    return raw_props


def get_update_properties(hub, resource_type: str, convert_to_present=True) -> Set:
    raw_props = set(hub.tool.gcp.RESOURCE_PROPS[resource_type].get("update", {}))
    if convert_to_present:
        return hub.tool.gcp.conversion_utils.convert_raw_properties_to_present(
            raw_props
        )
    return raw_props


def get_get_properties(hub, resource_type: str, convert_to_present=True) -> Set:
    raw_props = set(hub.tool.gcp.RESOURCE_PROPS[resource_type].get("get", {}))
    if convert_to_present:
        return hub.tool.gcp.conversion_utils.convert_raw_properties_to_present(
            raw_props
        )
    return raw_props


def get_delete_properties(hub, resource_type: str, convert_to_present=True) -> Set:
    raw_props = set(hub.tool.gcp.RESOURCE_PROPS[resource_type].get("delete", {}))
    if convert_to_present:
        return hub.tool.gcp.conversion_utils.convert_raw_properties_to_present(
            raw_props
        )
    return raw_props


def get_non_updatable_properties(hub, resource_type: str) -> Set:
    return hub.tool.gcp.resource_prop_utils.get_create_properties(
        resource_type
    ) - hub.tool.gcp.resource_prop_utils.get_update_properties(resource_type)


def get_present_properties(hub, resource_type: str) -> Set:
    return hub.tool.gcp.resource_prop_utils.get_create_properties(
        resource_type, False
    ).union(
        hub.tool.gcp.resource_prop_utils.get_update_properties(resource_type, False)
    )


def get_exclude_paths(hub, resource_type: str) -> Set:
    return set(hub.tool.gcp.RESOURCE_PROPS[resource_type].get("exclude_paths", {}))


def extract_resource_id(hub, input_props: Dict, resource_type: str) -> Dict:
    # TODO: check that GET, UPDATE, DELETE methods all get the same path params
    # resource_id_path = hub.tool.gcp.resource_prop_utils.get_resource_path(resource_type)

    # resource_id_prop_values = []
    # for resource_id_prop in resource_id_path:
    #     if resource_id_prop in input_props:
    #         resource_id_prop_values.append(input_props[resource_id_prop])
    #     #     TODO: handle this and other corner cases
    #     # elif resource_id_prop == "resourceId" and "id" in input_props:
    #     #     resource_id_prop_values.append(input_props["id"])
    #     elif "name" in input_props:
    #         resource_id_prop_values.append(input_props["name"])
    #     elif "id" in input_props:
    #         resource_id_prop_values.append(input_props["id"])
    #     else:
    #         raise "Unknown value for resource id element!"

    # resource_id = resource_id_delimiter.join(resource_id_prop_values)

    return hub.tool.gcp.resource_prop_utils.parse_link_to_resource_id(
        input_props.get("selfLink"), resource_type
    )


def get_resource_path(hub, resource_type: str) -> List:
    resource_path = resource_type.split(".")
    hub_ref = hub.metadata.gcp
    for resource_path_segment in resource_path:
        hub_ref = hub_ref[resource_path_segment]

    return hub_ref["PATH"]


def get_resource_id_property_name(hub, resource_type: str, method_name: str) -> str:
    resource_id_props = hub.tool.gcp.RESOURCE_PROPS[resource_type]["resource_id"]
    method_properties = {}
    if method_name == "get":
        method_properties = hub.tool.gcp.resource_prop_utils.get_get_properties(
            resource_type
        )
    elif method_name == "insert" or method_name == "create":
        method_properties = hub.tool.gcp.resource_prop_utils.get_create_properties(
            resource_type
        )
    elif method_name == "update":
        method_properties = hub.tool.gcp.resource_prop_utils.get_update_properties(
            resource_type
        )
    elif method_name == "delete":
        method_properties = hub.tool.gcp.resource_prop_utils.get_delete_properties(
            resource_type
        )

    for resource_id_prop in resource_id_props:
        if resource_id_prop in method_properties:
            return resource_id_prop

    return ""


def get_elements_from_resource_id(hub, resource_type: str, resource_id: str) -> Dict:
    resource_path = hub.tool.gcp.resource_prop_utils.get_resource_path(resource_type)
    src = resource_path.split("/")
    act = resource_id.split("/")
    result = {}

    idx = -1
    key = None
    val = None
    for s in reversed(src):
        if s.startswith("{") and s.endswith("}"):
            val = act[idx]
            key = s[1:-1]

        idx -= 1
        if idx % 2 != 0:
            result[key] = val

    return result


def parse_link_to_resource_id(hub, link, resource_type: str):
    result = hub.tool.gcp.resource_prop_utils.get_resource_path(resource_type)
    src = result.split("/")
    act = link.split("/")

    idx = -1
    key = None
    val = None

    for s in reversed(src):
        if s.startswith("{") and s.endswith("}"):
            val = act[idx]
            key = s

        idx -= 1
        if idx % 2 != 0:
            result = result.replace(key, val)

    return result


def parse_link_to_zone(hub, link: str) -> str:
    return link.split("/")[-1]


def get_path_parameters(hub, resource_type):
    resource_path = hub.tool.gcp.resource_prop_utils.get_resource_path(resource_type)
    src = resource_path.split("/")
    result = set()

    for s in src:
        if s.startswith("{") and s.endswith("}"):
            result.add(s[1:-1])

    return result


def format_path_params(hub, resource, resource_type):
    resource_copy = copy.deepcopy(resource)
    path_params = hub.tool.gcp.resource_prop_utils.get_path_parameters(resource_type)
    for path_el in path_params:
        if resource_copy.get(path_el):
            resource_copy[path_el] = resource_copy[path_el].split("/")[-1]

    return resource_copy
