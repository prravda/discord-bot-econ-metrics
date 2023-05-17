from typing import TypedDict


class Locale(TypedDict):
    KOR: str
    ENG: str


class CodeWithLocale(TypedDict):
    EXPR: Locale
    VAL: str


class BokStatCodeTable(TypedDict):
    GDP: str


class BokStatCodePeriod(TypedDict):
    ANNUAL: CodeWithLocale
    HALF_ANNUAL: CodeWithLocale
    QUARTER: CodeWithLocale
    MONTH: CodeWithLocale
    HALF_MONTH: CodeWithLocale
    DAY: CodeWithLocale


BOK_STAT_CODETABLE: BokStatCodeTable = {
    'GDP': '200Y005'
}

BOK_STAT_CODE_PERIOD: BokStatCodePeriod = {
    'ANNUAL': {
        'EXPR': {
            'KOR': '년',
            'ENG': 'Annual',
        },
        'VAL': 'A',
    },
    'HALF_ANNUAL': {
        'EXPR': {
            'KOR': '반년',
            'ENG': 'Half Annual',
        },
        'VAL': 'S',
    },
    'QUARTER': {
        'EXPR': {
            'KOR': '분기',
            'ENG': 'Quarter',
        },
        'VAL': 'Q',
    },
    'MONTH': {
        'EXPR': {
            'KOR': '월',
            'ENG': 'Month',
        },
        'VAL': 'M',
    },
    'HALF_MONTH': {
        'EXPR': {
            'KOR': '반월',
            'ENG': 'Half Month',
        },
        'VAL': 'SM',
    },
    'DAY': {
        'EXPR': {
            'KOR': '일',
            'ENG': 'Day',
        },
        'VAL': 'D',
    },
}
