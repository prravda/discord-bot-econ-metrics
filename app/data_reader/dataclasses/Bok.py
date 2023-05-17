from dataclasses import dataclass


@dataclass(frozen=True)
class BokGdpEntry:
    ITEM_CODE: str
    ITEM_NAME: str
    UNIT_NAME: str
    TIME: str
    DATA_VALUE: float


@dataclass(frozen=True)
class BokGdp:
    STAT_NAME_SHORT = 'GDP(국내총생산)'
    STAT_NAME_FULL: str
