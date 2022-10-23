import dataclasses
import datetime
from inspect import isclass
from types import NoneType, UnionType
from typing import Any, TypeVar, cast

from dateutil import parser


class FieldValidationError(Exception):
    """
    Field validation exception wrapper
    """

    def __init__(self, field: str, type_: type, value: Any):
        self.field = field
        self.type = type_
        self.value = value

    def __repr__(self) -> str:
        return (
            "<FieldValidationError("
            f"field={self.field}, "
            f"type={self.type}, "
            f"value={self.value}"
            ")>"
        )

    def __str__(self) -> str:
        return (
            f'Field validation error parsing "{self.value}"'
            f"into {self.field}, expected type {self.type}"
        )


class ValidationError(Exception):
    def __init__(self, cls: type, errors: list[FieldValidationError]):
        self.message = f"There were errors converting dict to {cls}"
        self.errors = errors


T = TypeVar("T", bound="ExtendedDataclass")


class ExtendedDataclass:
    """
    Extended dataclass is a smart container wrapper allowing you
    to construct a dataclass from a dictionary.
    """

    @classmethod
    def from_dict(cls: type[T], d: dict[str, Any]) -> T:
        errors: list[FieldValidationError] = []

        # Pre-populate an empty array to allow for nullable fields to be preset
        # Even if we populate non-nullable fields this will get rejected later
        mapped_dict = {field.name: None for field in dataclasses.fields(cls)}

        for (key, value) in d.items():
            try:
                field = cls.get_field(key)
                if field is not None:
                    mapped_dict[key] = parse_field_value(field, value)
            except FieldValidationError as err:
                errors.append(err)

        if len(errors) > 0:
            raise ValidationError(cls, errors)

        return cls(**mapped_dict)

    @classmethod
    def get_field(cls, name: str) -> dataclasses.Field | None:
        matched_fields = [
            field for field in dataclasses.fields(cls) if field.name == name
        ]
        if len(matched_fields) == 0:
            return None
        return matched_fields[0]


def parse_field_value(field: dataclasses.Field, value: Any) -> Any:
    """
    Field value parsing, need some more tests around this
    """
    try:
        return _parse_field_type(field.type, value)
    except (ValueError, TypeError) as exc:
        raise FieldValidationError(
            field=field.name, type_=field.type, value=value
        ) from exc


def _parse_field_type(_type: type, value: Any) -> Any:
    if _type == Any:
        return value
    if _type.__class__ == UnionType:
        if value is None and NoneType in getattr(_type, "__args__"):
            return None
        # Recursive handling for UnionType, handle first matching type
        for subtype in getattr(_type, "__args__"):
            try:
                return _parse_field_type(subtype, value)
            except (TypeError, ValueError):
                continue
        raise ValueError()  # Raise if no type succeeds to be matched
    if isclass(_type) and issubclass(_type, ExtendedDataclass):
        return _type.from_dict(value)
    if _type == list or _get_generic_typeclass(_type) == list:
        if _is_generic_type(_type):
            return _validated_instance(_type, value)
        types = getattr(_type, "__args__")
        return [_parse_field_type(types[0], i) for i in value]
    if _type == set or _get_generic_typeclass(_type) == set:
        if _is_generic_type(_type):
            return _validated_instance(_type, value)
        types = getattr(_type, "__args__")
        return {_parse_field_type(types[0], i) for i in value}
    if _type == tuple or _get_generic_typeclass(_type) == tuple:
        if _is_generic_type(_type):
            return _validated_instance(_type, value)
        return tuple(
            _parse_field_type(_type, value[i])
            for (i, _type) in enumerate(getattr(_type, "__args__"))
        )
    if (_type == dict or _get_generic_typeclass(_type) == dict) and isinstance(
        value, dict
    ):
        if _is_generic_type(_type):
            return _validated_instance(_type, value)
        types = getattr(_type, "__args__")
        return {
            _parse_field_type(types[0], dict_key): _parse_field_type(types[1], dict_val)
            for (dict_key, dict_val) in value.items()
        }
    if _type == datetime.datetime:
        if isinstance(value, str):
            return parser.isoparse(value)

        return datetime.datetime.utcfromtimestamp(value)
    if _type == datetime.date:
        if isinstance(value, str):
            return parser.isoparser().parse_isodate(value)

        return datetime.date.fromordinal(value)
    if _type == float and isinstance(value, int):
        return _validated_instance(_type, float(value))

    return _validated_instance(_type, value)


TInstance = TypeVar("TInstance", bound=object)


def _validated_instance(_type: type, value: TInstance) -> TInstance:
    if not isinstance(value, _type):
        raise ValueError()
    return cast(TInstance, value)


def _get_generic_typeclass(_type: type) -> type | None:
    """
    Returns the generic typeclass, i.e. `list`, `dict`, `tuple`, `set`.
    Implementation may be different depending on python version.
    """
    return getattr(_type, "__origin__", None)


def _is_generic_type(_type: type) -> bool:
    """
    Returns true if the generic type has no subclass,
    i.e. `list` instead of `list[str]`.
    Implementation may be different depending on python version.
    """
    return not getattr(_type, "__args__", None)
