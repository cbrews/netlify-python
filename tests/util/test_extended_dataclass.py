import dataclasses
import datetime
from pprint import pprint
from typing import Any

import pytest
from dateutil.tz import tzutc

from netlify.util.extended_dataclass import (
    ExtendedDataclass,
    FieldValidationError,
    ValidationError,
    parse_field_value,
)


def test_get_field__success():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_str: str

    field_str = BasicClass.get_field("field_str")
    assert isinstance(field_str, dataclasses.Field)
    assert field_str.name == "field_str"


def test_get_field__not_found():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_str: str

    not_found_field = BasicClass.get_field("not_found_field")
    assert not_found_field is None


def test_field_validation_error():
    error = FieldValidationError(field="test", type_=str, value=None)
    pprint(error)
    assert str(error) is not None
    assert error.field == "test"
    assert error.type == str
    assert error.value is None


def test_parse_field_value__str():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_str: str

    field_str = BasicClass.get_field("field_str")
    assert field_str is not None

    assert parse_field_value(field_str, "test_str") == "test_str"

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_str, None)

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_str, ["test_str"])


def test_parse_field_value__int():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_int: int

    field_int = BasicClass.get_field("field_int")
    assert field_int is not None

    assert parse_field_value(field_int, 1) == 1

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_int, None)


def test_parse_field_value__float():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_float: float

    field_float = BasicClass.get_field("field_float")
    assert field_float is not None

    assert parse_field_value(field_float, 1.0) == 1.0
    assert parse_field_value(field_float, 1) == 1.0

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_float, None)


def test_parse_field_value__bool():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_bool: bool

    field_bool = BasicClass.get_field("field_bool")
    assert field_bool is not None

    assert parse_field_value(field_bool, False) is False
    assert parse_field_value(field_bool, True) is True

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_bool, None)


def test_parse_field_value__optional_primitive():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_bool: bool | None

    field_bool = BasicClass.get_field("field_bool")
    assert field_bool is not None

    assert parse_field_value(field_bool, True) is True
    assert parse_field_value(field_bool, False) is False
    assert parse_field_value(field_bool, None) is None


def test_parse_field_value__datetime_from_str():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_datetime: datetime.datetime

    field_datetime = BasicClass.get_field("field_datetime")
    assert field_datetime is not None

    converted_datetime = parse_field_value(field_datetime, "2022-01-01T00:00:00Z")
    assert isinstance(converted_datetime, datetime.datetime)
    assert converted_datetime == datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=tzutc())

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_datetime, None)


def test_parse_field_value__datetime_from_int():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_datetime: datetime.datetime

    field_datetime = BasicClass.get_field("field_datetime")
    assert field_datetime is not None

    converted_datetime = parse_field_value(field_datetime, 1666215324)
    assert isinstance(converted_datetime, datetime.datetime)
    assert converted_datetime == datetime.datetime(2022, 10, 19, 21, 35, 24)

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_datetime, None)


def test_parse_field_value__date_from_str():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_date: datetime.date

    field_date = BasicClass.get_field("field_date")
    assert field_date is not None

    converted_date = parse_field_value(field_date, "2022-01-01")
    assert isinstance(converted_date, datetime.date)
    assert converted_date == datetime.date(2022, 1, 1)

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_date, None)


def test_parse_field_value__date_from_int():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_date: datetime.date

    field_date = BasicClass.get_field("field_date")
    assert field_date is not None

    converted_date = parse_field_value(field_date, 738156)
    assert isinstance(converted_date, datetime.date)
    assert converted_date == datetime.date(2022, 1, 1)

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_date, None)


def test_parse_value__list_generic():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_list: list

    field_list = BasicClass.get_field("field_list")
    assert field_list is not None

    assert parse_field_value(field_list, []) == []
    assert parse_field_value(field_list, ["test"]) == ["test"]
    assert parse_field_value(field_list, ["test", 2]) == ["test", 2]

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_list, None)

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_list, {})


def test_parse_field_value__list_of_string():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_list: list[str]

    field_list = BasicClass.get_field("field_list")
    assert field_list is not None

    assert parse_field_value(field_list, []) == []
    assert parse_field_value(field_list, ["test", "test2"]) == ["test", "test2"]

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_list, None)

    with pytest.raises(FieldValidationError):
        parse_field_value(field_list, [1, 2, 3])


def test_parse_field_value__list_optional():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_list: list[str] | None

    field_list = BasicClass.get_field("field_list")
    assert field_list is not None

    assert parse_field_value(field_list, []) == []
    assert parse_field_value(field_list, ["test", "test2"]) == ["test", "test2"]
    assert parse_field_value(field_list, None) is None


def test_parse_field_value__tuple_generic():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_tuple: tuple

    field_tuple = BasicClass.get_field("field_tuple")
    assert field_tuple is not None

    assert parse_field_value(field_tuple, ("test", 1)) == ("test", 1)

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_tuple, None)


def test_parse_field_value__tuple_specific():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_tuple: tuple[str, int]

    field_tuple = BasicClass.get_field("field_tuple")
    assert field_tuple is not None

    assert parse_field_value(field_tuple, ("test", 1)) == ("test", 1)

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_tuple, None)


def test_parse_field_value__tuple_optional():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_tuple: tuple[str, int] | None

    field_tuple = BasicClass.get_field("field_tuple")
    assert field_tuple is not None

    assert parse_field_value(field_tuple, ("test", 1)) == ("test", 1)
    assert parse_field_value(field_tuple, None) is None


def test_parse_field_value__set_generic():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_set: set

    field_set = BasicClass.get_field("field_set")
    assert field_set is not None

    assert parse_field_value(field_set, set(["test"])) == set(["test"])

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_set, None)


def test_parse_field_value__set_specific():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_set: set[int]

    field_set = BasicClass.get_field("field_set")
    assert field_set is not None

    assert parse_field_value(field_set, set([1, 2])) == set([1, 2])

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_set, None)

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_set, set(["test"]))


def test_parse_field_value__set_optional():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_set: set[int] | None

    field_set = BasicClass.get_field("field_set")
    assert field_set is not None

    assert parse_field_value(field_set, set([1, 2])) == set([1, 2])
    assert parse_field_value(field_set, None) is None


def test_parse_field_value__dict_generic():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_dict: dict

    field_dict = BasicClass.get_field("field_dict")
    assert field_dict is not None

    assert parse_field_value(field_dict, {"key": "value"}) == {"key": "value"}

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_dict, None)


def test_parse_field_value__dict_specific():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_dict: dict[str, str]

    field_dict = BasicClass.get_field("field_dict")
    assert field_dict is not None

    assert parse_field_value(field_dict, {"key": "value"}) == {"key": "value"}

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_dict, None)

    with pytest.raises(FieldValidationError):
        assert parse_field_value(field_dict, {"key": 1})


def test_parse_field_value__dict_optional():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_dict: dict[str, str] | None

    field_dict = BasicClass.get_field("field_dict")
    assert field_dict is not None

    assert parse_field_value(field_dict, {"key": "value"}) == {"key": "value"}
    assert parse_field_value(field_dict, None) is None


def test_parse_field_value__subclass():
    @dataclasses.dataclass
    class SubBasicClass(ExtendedDataclass):
        field_str: str

    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_subclass: SubBasicClass

    field_subclass = BasicClass.get_field("field_subclass")
    assert field_subclass is not None

    subclass = parse_field_value(field_subclass, {"field_str": "test"})
    assert isinstance(subclass, SubBasicClass)
    assert subclass.field_str == "test"


def test_parse_field_value__subclass_optional():
    @dataclasses.dataclass
    class SubBasicClass(ExtendedDataclass):
        field_str: str

    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_subclass: SubBasicClass | None

    field_subclass = BasicClass.get_field("field_subclass")
    assert field_subclass is not None

    subclass = parse_field_value(field_subclass, {"field_str": "test"})
    assert isinstance(subclass, SubBasicClass)
    assert subclass.field_str == "test"

    assert parse_field_value(field_subclass, None) is None


def test_parse_field_value__any():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_any: Any

    field_any = BasicClass.get_field("field_any")
    assert field_any is not None

    assert parse_field_value(field_any, "str") == "str"
    assert parse_field_value(field_any, 1) == 1
    assert parse_field_value(field_any, True) is True
    assert parse_field_value(field_any, None) is None
    assert parse_field_value(field_any, ["str"]) == ["str"]


def test_extended_dataclass_from_dict__valid():
    @dataclasses.dataclass
    class BasicSubClass(ExtendedDataclass):
        field_int: int

    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_str: str
        field_bool: bool
        field_float: float
        field_int: int
        field_optional_int: int | None
        field_sub_class: BasicSubClass | None
        field_optional_list: list[int] | None
        field_required_list: list

    basic_class_instance = BasicClass.from_dict(
        {
            "field_str": "my_str",
            "field_bool": False,
            "field_float": 100.0,
            "field_int": 39,
            "field_optional_int": None,
            "field_ignored": "HELLO",
            "field_sub_class": {
                "field_int": 55,
            },
            "field_optional_list": [1],
            "field_required_list": [10],
        }
    )

    assert basic_class_instance.field_str == "my_str"
    assert basic_class_instance.field_bool is False
    assert basic_class_instance.field_float == 100.0
    assert basic_class_instance.field_int == 39
    assert basic_class_instance.field_optional_int is None
    assert basic_class_instance.field_sub_class is not None
    assert basic_class_instance.field_sub_class.field_int == 55
    assert basic_class_instance.field_optional_list == [1]
    assert basic_class_instance.field_required_list == [10]


def test_extended_dataclass_from_dict__invalid():
    @dataclasses.dataclass
    class BasicClass(ExtendedDataclass):
        field_str: str
        field_bool: bool
        field_float: float
        field_int: int
        field_optional_int: int | None

    with pytest.raises(ValidationError) as exc_info:
        BasicClass.from_dict(
            {
                "field_str": "my_str",
                "field_bool": None,
                "field_float": 100,
                "field_int": 1.0,
                "field_optional_int": "str",
            }
        )

    exception = exc_info.value
    assert isinstance(exception, ValidationError)
    assert len(exception.errors) == 3
