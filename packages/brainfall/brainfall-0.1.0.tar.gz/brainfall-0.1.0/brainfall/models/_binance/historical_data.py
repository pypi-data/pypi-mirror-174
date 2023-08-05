from attrs import define, field
from numpy import float32, uint32
from pendulum import DateTime

from brainfall.utils.converters import ms_ts_to_datetime_ndarray, to_ndarray_of


@define(kw_only=True)
class HistoricalData:
    open_time: DateTime = field(converter=ms_ts_to_datetime_ndarray)
    close_time: DateTime = field(converter=ms_ts_to_datetime_ndarray)
    open_price: float = field(converter=to_ndarray_of(float32))
    high_price: float = field(converter=to_ndarray_of(float32))
    low_price: float = field(converter=to_ndarray_of(float32))
    close_price: float = field(converter=to_ndarray_of(float32))
    volume: float = field(converter=to_ndarray_of(float32))
    quote_asset_volume: float = field(converter=to_ndarray_of(float32))
    taker_buy_base_asset_volume: float = field(converter=to_ndarray_of(float32))
    taker_buy_quote_asset_volume: float = field(converter=to_ndarray_of(float32))
    num_trades: int = field(converter=to_ndarray_of(uint32))
    ignore: str = field(repr=False)
