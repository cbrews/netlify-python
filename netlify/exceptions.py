from pydantic import BaseModel


class NetlifyErrorSchema(BaseModel):
    code: int
    message: str


class NetlifyError(Exception):
    method: str
    path: str
    code: int
    message: str

    def __init__(self, method: str, path: str, error: NetlifyErrorSchema):
        self.method = method
        self.path = path
        self.code = error.code
        self.message = error.message

        super().__init__(
            f"Netlify request to {self.method} {self.path} did not succeed. "
            f"code: {self.code}, message: '{self.message}'"
        )


# Backwards compatibility
NetlifyException = NetlifyError
