from collections.abc import Callable

from binance.spot import Spot
from binance.websocket.spot.websocket_client import (
    SpotWebsocketClient as WebsocketClient,
)
from pendulum import DateTime

from brainfall.models.binance import HistoricalData, KlineSocketData, MarketInfo
from brainfall.utils.converters import ms_ts_to_datetime


class Binance:
    SUPPORTED_INTERVALS = [
        "1m",
        "3m",
        "5m",
        "15m",
        "30m",
        "1h",
        "2h",
        "4h",
        "6h",
        "8h",
        "12h",
        "1d",
        "3d",
        "1w",
        "1M",
    ]
    KLINES_COLS = [
        "open_time",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
        "close_time",
        "quote_asset_volume",
        "num_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "ignore",
    ]

    def __init__(self, **kwargs):
        self.client = Spot(**kwargs)
        self.ws_client = WebsocketClient()
        self.ws_client.start()
        self._active_ws = 0

    def server_time(self) -> DateTime | None:
        """Get server time from Binance"""
        time = self.client.time().get("serverTime")
        return ms_ts_to_datetime(time) if time else None

    def klines(self, symbol: str, interval: str, **kwargs) -> HistoricalData:
        """Get latest 500 (configurable) klines for the requested symbol/interval"""
        klines = self.client.klines(symbol=symbol, interval=interval, **kwargs)
        return HistoricalData(**dict(zip(self.KLINES_COLS, zip(*klines))))  # old->new

    def start_kline_socket(
        self, symbol: str, interval: str, callback: Callable
    ) -> None:
        """Start a kline websocket that calls the callback function on every reply"""
        wrapped_callback = self._kline_socket_callback_wrapper(callback)
        self.ws_client.kline(
            callback=wrapped_callback,
            symbol=symbol,
            interval=interval,
            id=self._active_ws + 1,
        )
        self._active_ws += 1

    def stop_kline_socket(self, symbol: str, interval: str) -> None:
        """Stop a kline websocket that was started with Binance.start_kline_socket"""
        self.ws_client.stop_socket(f"{symbol.lower()}@kline_{interval}")

    def market_info(self) -> MarketInfo:
        """Get market info; includes timezone, symbols, filters, and rate limits"""
        return MarketInfo(**self.client.exchange_info())

    def stop(self) -> None:
        """Stop websocket client"""
        self.ws_client.stop()

    @staticmethod
    def _kline_socket_callback_wrapper(func: Callable) -> Callable:
        """Websocket callback wrapper to parse kline received data as KlineSocketData"""

        def _socket_callback_wrapper(msg):
            if "result" in msg:
                return
            nested_msg = msg.pop("k", {})
            msg.update(nested_msg)
            data = KlineSocketData(**msg)
            return func(data)

        return _socket_callback_wrapper
