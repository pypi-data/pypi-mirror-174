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


def to_ratelimits(ratelimits: list[dict]) -> list[RateLimits]:
    """convert ratelimits list of dicts to list of RateLimits type"""
    return [RateLimits(**ratelimit) for ratelimit in ratelimits]


def to_symbols_dict(symbols_list: list[dict]) -> dict[Symbol]:
    """from list of dict of symbols to dict of symbol_name: Symbol type"""
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
        """get server time"""
        return self.serverTime

    @property
    def num_symbols(self):
        """get number of symbols in market"""
        return len(self.symbols)
