import dataclasses
import json
import typing
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List

from cloudspec import CloudSpecParam


@dataclass
class ResourceProperty:
    type_: str = (
        None  # "string" | "boolean" | "integer" | "number" | "object" | "array" | null
    )
    description: str = None
    _ref: str = None  # $ref
    items: "ResourceProperty" = None  # used with properties of type "array"
    properties: Dict[
        str, "ResourceProperty"
    ] = None  # used with properties of type "object" for representing complex object

    format: str = None  # "byte" | "double" | "float" | "int32" | "int64" | "uint32" | "uint64" | null
    # can be used to detail what type the string holds
    enum: List[str] = None  # can be used with type "string" to detail allowed values
    additional_properties: Dict[
        str, str
    ] = None  # can be used for more fine-grained typing
    annotations: Dict[
        str, Any
    ] = None  # can be used to see if it is required for methods


@dataclass
class ResourceSchema:
    """Class representing GCP resource schema as returned by discovery API
    See: https://www.googleapis.com/discovery/v1/apis/compute/v1/rest
    """

    id_: str = None  # ref name
    description: str = None
    properties: Dict[str, ResourceProperty] = None


def parse_file(hub, path: str = "") -> Dict[str, ResourceSchema]:
    with open(path) as json_schema_file:
        schemas = json.load(json_schema_file)
    schemas = schemas["schemas"]
    schemas = {
        resource_name: _dataclass_from_dict(
            hub.tool.gcp.schema_parser.sanitize_schema(resource_schema), ResourceSchema
        )
        for (resource_name, resource_schema) in schemas.items()
    }
    return schemas


def parse_schemas(hub, schema: Dict[str, ResourceSchema]) -> Dict[str, CloudSpecParam]:
    pass


def convert_schemas(hub, schemas: Dict[str, Any]) -> Dict[str, ResourceSchema]:
    return {
        name: hub.tool.gcp.schema_parser.convert_schema(schema)
        for (name, schema) in schemas.items()
    }


def convert_schema_to_cloud_spec_param(hub, resource_schema) -> CloudSpecParam:
    pass


def _dataclass_from_dict(d: Dict[str, Any], klass):
    field_types = {
        class_field.name: class_field.type for class_field in dataclasses.fields(klass)
    }
    raw_field_values = {
        dict_key: dict_value
        for (dict_key, dict_value) in d.items()
        if dict_key in field_types.keys()
    }
    return klass(
        **{
            field_name: _parse_raw_field_value(
                raw_field_value, field_types.get(field_name)
            )
            for (field_name, raw_field_value) in raw_field_values.items()
        }
    )


def _parse_raw_field_value(raw_field_value: Any, expected_type) -> Any:
    if dataclasses.is_dataclass(expected_type):
        return _dataclass_from_dict(raw_field_value, expected_type)
    if expected_type == typing.ForwardRef("ResourceProperty"):
        return _dataclass_from_dict(raw_field_value, ResourceProperty)
    if isinstance(raw_field_value, list) and typing.get_origin(expected_type) == list:
        return [
            _parse_raw_field_value(list_value, typing.get_args(expected_type)[0])
            for list_value in raw_field_value
        ]
    if isinstance(raw_field_value, dict) and typing.get_origin(expected_type) == dict:
        return {
            key: _parse_raw_field_value(value, typing.get_args(expected_type)[1])
            for (key, value) in raw_field_value.items()
        }
    return raw_field_value


def sanitize_schema(hub, schema: Any) -> Any:
    if isinstance(schema, dict):
        return {
            hub.tool.gcp.schema_parser.sanitize_key(
                key
            ): hub.tool.gcp.schema_parser.sanitize_schema(value)
            for (key, value) in schema.items()
        }
    if isinstance(schema, list):
        return [hub.tool.gcp.schema_parser.sanitize_schema(item) for item in schema]
    return schema


def sanitize_key(hub, key: str) -> str:
    return hub.tool.format.keyword.unclash(hub.tool.gcp.case.snake(key))
