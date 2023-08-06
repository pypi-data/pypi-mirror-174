import logging
from collections.abc import Iterable
from typing import Any, Literal

from aio_pika import IncomingMessage, Message

from py_fastapi_logging.data_filter import DataFilter


class MqLogger:
    _data_filter: DataFilter
    _request_id_header_name: str

    def __init__(
        self,
        request_id_header_name: str = "request_id",
        filtered_fields: Iterable[str] = frozenset(),
        marker_filtered: str = "[filtered]",
    ):
        self._request_id_header_name = request_id_header_name
        self._data_filter = DataFilter(filtered_fields or (), marker_filtered)

    def log_received_message(self, message: IncomingMessage, metadata: Any = None) -> None:
        request_id: str | None = None
        if self._request_id_header_name in message.headers:
            request_id = str(message.headers.get(self._request_id_header_name))
        self._log_message(
            action="RECEIVE",
            exchange=message.exchange,
            routing_key=message.routing_key,
            message=message,
            request_id=request_id,
            metadata=metadata,
        )

    def log_published_message(
        self,
        exchange: str,
        routing_key: str,
        message: Message,
        request_id: str | None,
        metadata: Any = None,
    ) -> None:
        self._log_message(
            action="PUBLISH",
            exchange=exchange,
            routing_key=routing_key,
            message=message,
            request_id=request_id,
            metadata=metadata,
        )

    def _log_message(
        self,
        action: Literal["RECEIVE", "PUBLISH"],
        exchange: str | None,
        routing_key: str | None,
        message: Message,
        request_id: str | None,
        metadata: Any,
    ) -> None:
        try:
            payload = message.body.decode("utf8")
            payload = self._data_filter.filter_json_body(payload)
        except Exception:
            logging.exception("Failed to prepare message payload for logging")
            payload = "[failed to decode or filter]"

        logging.info(
            f"{action} {exchange or 'default'}/{routing_key}",
            extra={
                "tags": ["MQ", action],
                "request_id": request_id,
                "payload": {
                    "exchange": exchange,
                    "queue": routing_key,
                    "message": payload,
                    "metadata": metadata,
                },
            },
        )
