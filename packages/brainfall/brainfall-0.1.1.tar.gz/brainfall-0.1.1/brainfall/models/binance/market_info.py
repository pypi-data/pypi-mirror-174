from attrs import define, field
from pendulum import DateTime

from brainfall.utils.converters import ms_ts_to_datetime


@define
class RateLimits:
    rateLimitType: str = field()
    interval: str = field()
    intervalNum: int = field(converter=int)
    limit: int = field(converter=int)


@define
class Symbol:
    symbol: str
    baseAsset: str
    quoteAsset: str
    status: str
    baseAssetPrecision: int = field(converter=int)
    quotePrecision: int = field(converter=int)
    quoteAssetPrecision: int = field(converter=int)
    baseCommissionPrecision: int = field(converter=int)
    quoteCommissionPrecision: int = field(converter=int)
    isSpotTradingAllowed: bool
    isMarginTradingAllowed: bool
    cancelReplaceAllowed: bool
    allowTrailingStop: bool
    quoteOrderQtyMarketAllowed: bool
    icebergAllowed: bool
    ocoAllowed: bool
    orderTypes: list[str]
    permissions: list[str]
    filters: list

    @property
    def base(self):
        return self.baseAsset

    @property
    def quote(self):
        return self.quoteAsset


def to_ratelimits(ratelimits):
    return [RateLimits(**ratelimit) for ratelimit in ratelimits]


def to_symbols_dict(symbols_list):
    return {values["symbol"]: Symbol(**values) for values in symbols_list}


@define
class MarketInfo:
    timezone: str
    exchangeFilters: list
    rateLimits: list[RateLimits] = field(converter=to_ratelimits)
    symbols: dict = field(converter=to_symbols_dict)
    serverTime: DateTime = field(converter=ms_ts_to_datetime)

    @property
    def server_time(self):
        return self.serverTime

    @property
    def num_symbols(self):
        return len(self.symbols)

    @property
    def rate_limits(self):
        return self.rateLimits

    @property
    def filters(self):
        return self.exchangeFilters
