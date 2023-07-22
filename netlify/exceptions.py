from typing import Any

from pydantic import BaseModel


class NetlifyErrorSchema(BaseModel):
    code: int | None = None
    message: str | None = None
    errors: dict[str, Any] | None = None


class NetlifyError(Exception):
    method: str
    path: str
    code: int | None
    message: str | None
    errors: dict[str, Any] | None

    def __init__(self, method: str, path: str, error: NetlifyErrorSchema):
        self.method = method
        self.path = path
        self.code = error.code
        self.message = error.message
        self.errors = error.errors

        super().__init__(
            f"Netlify request to {self.method} {self.path} did not succeed. "
            f"code: {self.code}"
            if self.code is not None
            else "" f"message: {self.message}"
            if self.message is not None
            else "" f"errors: {self.errors}"
            if self.errors is not None
            else ""
        )


# Backwards compatibility
NetlifyException = NetlifyError
