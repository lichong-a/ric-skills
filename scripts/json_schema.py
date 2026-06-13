"""Small dependency-free JSON Schema subset used by RIC machine contracts."""

from __future__ import annotations

import re
import json
import math
from typing import Any


SUPPORTED = {
    "$schema",
    "$id",
    "type",
    "additionalProperties",
    "required",
    "properties",
    "enum",
    "const",
    "minLength",
    "pattern",
    "minimum",
    "maximum",
    "minItems",
    "uniqueItems",
    "items",
    "minProperties",
}


def check_schema(schema: Any, path: str = "$") -> list[str]:
    if not isinstance(schema, dict):
        return [f"{path}: schema must be an object"]
    errors = [f"{path}: unsupported keyword {key!r}" for key in schema if key not in SUPPORTED]
    for key in ("properties",):
        value = schema.get(key, {})
        if not isinstance(value, dict):
            errors.append(f"{path}.{key}: must be an object")
        else:
            for name, child in value.items():
                errors.extend(check_schema(child, f"{path}.{key}.{name}"))
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    if isinstance(required, list) and isinstance(properties, dict):
        for name in required:
            if name not in properties:
                errors.append(f"{path}: required property {name!r} is not declared in properties")
    additional = schema.get("additionalProperties")
    if isinstance(additional, dict):
        errors.extend(check_schema(additional, f"{path}.additionalProperties"))
    items = schema.get("items")
    if isinstance(items, dict):
        errors.extend(check_schema(items, f"{path}.items"))
    return errors


def _matches_type(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
    }.get(expected, False)


def validate(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type and not _matches_type(instance, expected_type):
        return [f"{path}: expected {expected_type}, got {type(instance).__name__}"]
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value is not in enum")
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: value does not match const")
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errors.append(f"{path}: string is shorter than minLength")
        if "pattern" in schema and re.fullmatch(schema["pattern"], instance) is None:
            errors.append(f"{path}: string does not match pattern")
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if not math.isfinite(instance):
            errors.append(f"{path}: number must be finite")
            return errors
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: number is below minimum")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: number is above maximum")
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            errors.append(f"{path}: array has fewer than minItems")
        if schema.get("uniqueItems"):
            rendered = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in instance]
            if len(rendered) != len(set(rendered)):
                errors.append(f"{path}: array items are not unique")
        if isinstance(schema.get("items"), dict):
            for index, item in enumerate(instance):
                errors.extend(validate(item, schema["items"], f"{path}[{index}]"))
    if isinstance(instance, dict):
        if len(instance) < schema.get("minProperties", 0):
            errors.append(f"{path}: object has fewer than minProperties")
        for name in schema.get("required", []):
            if name not in instance:
                errors.append(f"{path}: missing required property {name!r}")
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for name, value in instance.items():
            if name in properties:
                errors.extend(validate(value, properties[name], f"{path}.{name}"))
            elif additional is False:
                errors.append(f"{path}: unexpected property {name!r}")
            elif isinstance(additional, dict):
                errors.extend(validate(value, additional, f"{path}.{name}"))
    return errors
