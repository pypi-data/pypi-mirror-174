#!/usr/bin/python3
import time
from enum import Enum

# Local imports
from tometrics.lib.influxdb import InfluxDBClient
from tometrics.lib.metric import Metric
from typing import List


class UnsupportedClient(Exception):
    def __init__(self, message="Unknown", errors={}):
        super().__init__(message)
        self.errors = errors


class ClientTypes(Enum):
    influxDB = "InfluxDB"


class ToMetrics:
    """
    A wrapper for easily pushing metrics to a backend.

    Note: current implementation is not mean for high frequency pushing (no buffering is used)
    :param bucket The bucket/table/database we are pushing data into.
    :param static_metric_name string If we only are pushing one type of value, we can optionally just set the name once
    :param static_metric_metadata map If there are tags that do not change for all the data we are pushing, we can set those once
    """

    def __init__(
        self,
        backend_url: str,
        client_type: ClientTypes,
        # Data specific params
        bucket: str,
        static_metric_name: str,
        static_metric_metadata: map = {},
        # Additional optional args
        username: str = None,
        password: str = None,
        verbose: bool = True,
    ):
        if verbose:
            print(
                f'[ToMetrics] Initializing "{bucket}|{static_metric_name}" streaming to {client_type} via "{backend_url}"'
            )

        # Init member vars
        self.backend_url = backend_url.rstrip("/")
        self.client_type = client_type
        self.username = username
        self.password = password
        self.verbose = verbose

        self.bucket = bucket
        self.static_metric_name = static_metric_name
        self.static_metric_metadata = static_metric_metadata

        # Setup the client
        self.client = None
        if client_type == ClientTypes.influxDB:
            self.client = InfluxDBClient(self.backend_url, self.bucket)
        else:
            raise UnsupportedClient(f"{client_type} is currently not supported")

    def send(self, data: map, metadata: map = {}, timestamp_override=None):
        """
        Delegate to the bulk impl.
        :param data Dict of key value pairs that holds the data/fields for our sample
        :param metadata Dict of key value pairs that holds the metadata describing our sample
        TODO we could do some helpful caching of the name if we only plan to send one type of value?
        TODO ^ also for tags
        """
        timestamp = timestamp_override or time.time_ns()
        all_metadata = self.static_metric_metadata
        all_metadata.update(metadata)

        self.send_bulk([Metric(self.static_metric_name, timestamp, data, all_metadata)])

    def send_bulk(self, metrics: List[Metric]):
        """
        Simply delegate to the client to send a data.
        :param data Dict of key value pairs that holds the data/fields for our sample
        :param metadata Dict of key value pairs that holds the metadata describing our sample
        TODO we could do some helpful caching of the name if we only plan to send one type of value?
        TODO ^ also for tags
        """
        self.client.send_bulk(metrics)
