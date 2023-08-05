from attrs import define, field
from pendulum import DateTime

from brainfall.models import Intervals
from brainfall.utils.converters import ms_ts_to_datetime


@define
class KlineSocketData:
    e: str = field()  # event type
    s: str = field()  # symbol
    B: str = field(repr=False)  # ignore
    i: Intervals = field(converter=Intervals)  # interval
    n: int = field(converter=int)  # number of trades
    f: int = field(converter=int)  # first trade id
    L: int = field(converter=int)  # last trade id
    o: float = field(converter=float)  # open
    c: float = field(converter=float)  # close
    h: float = field(converter=float)  # high
    l: float = field(converter=float)  # low
    v: float = field(converter=float)  # base asset volume
    q: float = field(converter=float)  # quote asset volume
    V: float = field(converter=float)  # taker buy base asset volume
    Q: float = field(converter=float)  # taker buy quote asset volume
    x: bool = field(converter=bool)  # is this kline closed
    E: DateTime = field(  # event ts
        converter=ms_ts_to_datetime, repr=DateTime.to_datetime_string
    )
    t: DateTime = field(  # kline start ts
        converter=ms_ts_to_datetime, repr=DateTime.to_datetime_string
    )
    T: DateTime = field(  # kline close ts
        converter=ms_ts_to_datetime, repr=DateTime.to_datetime_string
    )

    @property
    def open(self):
        return self.o

    @property
    def close(self):
        return self.c

    @property
    def high(self):
        return self.h

    @property
    def low(self):
        return self.l

    @property
    def symbol(self):
        return self.s

    @property
    def interval(self):
        return self.i

    @property
    def timestamp(self):
        return self.E

    @property
    def open_time(self):
        return self.t

    @property
    def close_time(self):
        return self.T
