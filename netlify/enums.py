from enum import Enum


class ListSitesFilter(str, Enum):
    all = "all"
    owner = "owner"
    guest = "guest"
