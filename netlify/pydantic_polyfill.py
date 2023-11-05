from typing import Any, Generic, TypeVar

import pydantic

T = TypeVar("T", bound=pydantic.BaseModel)


class PydanticPolyfill(Generic[T]):
    def __init__(self, cls: type[T]):
        self.cls = cls

    def to_pydantic_object(self, data: dict[str, Any]) -> T:  # pragma: no cover
        if pydantic.__version__ < "2":
            return self.cls.parse_obj(data)  # type: ignore[attr-defined]
        return self.cls.model_validate(data)  # type: ignore[attr-defined]
