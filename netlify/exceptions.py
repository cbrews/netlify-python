from dataclasses import dataclass

from netlify.util.extended_dataclass import ExtendedDataclass as EDC


@dataclass
class NetlifyError(EDC):
    code: int
    message: str


class NetlifyException(Exception):
    method: str
    path: str
    code: int
    message: str

    def __init__(self, method: str, path: str, error: NetlifyError):
        self.method = method
        self.path = path
        self.code = error.code
        self.message = error.message

        super().__init__(
            f"Netlify request to {self.method} {self.path} did not succeed. "
            f"code: {self.code}, message: '{self.message}'"
        )
