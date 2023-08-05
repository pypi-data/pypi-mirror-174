from enum import Enum


class Intervals(Enum):
    MINS1 = "1m"
    MINS3 = "3m"
    MINS5 = "5m"
    MINS15 = "15m"
    MINS30 = "30m"
    HOURS1 = "1h"
    HOURS2 = "2h"
    HOURS4 = "4h"
    HOURS8 = "8h"
    HOURS12 = "12h"
    DAYS1 = "1d"
    DAYS3 = "3d"
    WEEKS1 = "1w"
    MONTHS1 = "1M"
    YEARS1 = "1y"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
