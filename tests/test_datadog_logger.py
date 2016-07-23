from datadog_logger.handler import DatadogLogHandler

import logging
import mock
import sys
import traceback
import unittest


def make_exc_info():
    try:
        raise RuntimeError("message")
    except:
        return sys.exc_info()


class TestDatadogLogger(unittest.TestCase):
    @mock.patch("datadog_logger.handler.datadog", autospec=True)
    def test_logs_to_datadog(self, mock_dd):
        handler = DatadogLogHandler()

        record = logging.makeLogRecord({
            "msg": "Some message"
        })

        handler.emit(record)

        mock_dd.api.Event.create.assert_called_with(
            title="Some message", text="Some message")

    @mock.patch("datadog_logger.handler.datadog", autospec=True)
    def test_logs_formatted_message_as_text(self, mock_dd):
        handler = DatadogLogHandler()

        exc_info = make_exc_info()

        record = logging.makeLogRecord({
            "msg": "Some message",
            "exc_info": exc_info
        })

        expected_text = "\n".join(
            ["Some message", "".join(traceback.format_exception(*exc_info))]).rstrip("\n")

        handler.emit(record)

        mock_dd.api.Event.create.assert_called_with(
            title="Some message", text=expected_text)

    @mock.patch("datadog_logger.handler.datadog", autospec=True)
    def test_includes_tags_from_constructor(self, mock_dd):
        handler = DatadogLogHandler(tags=["some:tag"])

        record = logging.makeLogRecord({
            "msg": "Some message"
        })

        handler.emit(record)

        mock_dd.api.Event.create.assert_called_with(
            title="Some message", text="Some message",
            tags=["some:tag"])

    @mock.patch("datadog_logger.handler.datadog", autospec=True)
    def test_includes_mentions_from_constructor(self, mock_dd):
        handler = DatadogLogHandler(mentions=["@mention-1", "@mention-2"])

        record = logging.makeLogRecord({
            "msg": "Some message"
        })

        handler.emit(record)

        mock_dd.api.Event.create.assert_called_with(
            title="Some message", text="Some message\n\n@mention-1 @mention-2")

    @mock.patch("datadog_logger.handler.datadog", autospec=True)
    def test_includes_maps_debug_to_info(self, mock_dd):
        handler = DatadogLogHandler()

        record = logging.makeLogRecord({
            "msg": "Some message",
            "levelno": logging.DEBUG
        })

        handler.emit(record)

        mock_dd.api.Event.create.assert_called_with(
            title="Some message", text="Some message",
            alert_type="info")

    @mock.patch("datadog_logger.handler.datadog", autospec=True)
    def test_includes_maps_info_to_info(self, mock_dd):
        handler = DatadogLogHandler()

        record = logging.makeLogRecord({
            "msg": "Some message",
            "levelno": logging.INFO
        })

        handler.emit(record)

        mock_dd.api.Event.create.assert_called_with(
            title="Some message", text="Some message",
            alert_type="info")

    @mock.patch("datadog_logger.handler.datadog", autospec=True)
    def test_includes_maps_warning_to_warning(self, mock_dd):
        handler = DatadogLogHandler()

        record = logging.makeLogRecord({
            "msg": "Some message",
            "levelno": logging.WARNING
        })

        handler.emit(record)

        mock_dd.api.Event.create.assert_called_with(
            title="Some message", text="Some message",
            alert_type="warning")

    @mock.patch("datadog_logger.handler.datadog", autospec=True)
    def test_includes_maps_error_to_error(self, mock_dd):
        handler = DatadogLogHandler()

        record = logging.makeLogRecord({
            "msg": "Some message",
            "levelno": logging.ERROR
        })

        handler.emit(record)

        mock_dd.api.Event.create.assert_called_with(
            title="Some message", text="Some message",
            alert_type="error")

    @mock.patch("datadog_logger.handler.datadog", autospec=True)
    def test_includes_maps_critical_to_error(self, mock_dd):
        handler = DatadogLogHandler()

        record = logging.makeLogRecord({
            "msg": "Some message",
            "levelno": logging.CRITICAL
        })

        handler.emit(record)

        mock_dd.api.Event.create.assert_called_with(
            title="Some message", text="Some message",
            alert_type="error")
