from enum import Enum


class ListSitesFilter(str, Enum):
    all = "all"
    owner = "owner"
    guest = "guest"


class Period(str, Enum):
    monthly = "monthly"
    yearly = "yearly"
