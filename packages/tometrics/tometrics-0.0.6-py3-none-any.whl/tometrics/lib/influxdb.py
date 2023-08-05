#!/usr/bin/python3
from dataclasses import dataclass
from unicodedata import name
import requests

# Local imports
from tometrics.lib.generic_interface import GenericInterface
from tometrics.lib.metric import Metric
from typing import List


class FailedBucketCreation(Exception):
    def __init__(self, message="Unknown", errors={}):
        super().__init__(message)
        self.errors = errors


class InfluxDBClient(GenericInterface):
    def __init__(self, backend_url: str, bucket: str):
        self.backend_url = backend_url
        self.bucket = bucket

        # Create the db if it does not exist
        # curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE mydb"
        response = requests.post(
            f"{self.backend_url}/query",
            params={"q": f"CREATE DATABASE {self.bucket}"},
        )
        if response.status_code != 200:
            print(response.text)
            raise FailedBucketCreation(f"Failed to create database {self.bucket}")

    # def send(
    #     self,
    #     name: str,
    #     timestamp_ns: int,
    #     data: map = {},
    #     metadata: map = {},
    # ):
    #     """
    #     curl -i -XPOST 'http://localhost:8086/write?db=mydb' --data-binary 'cpu_load_short,host=server01,region=us-west value=0.64 1434055562000000000'"""
    #     formatted_metadata = ""
    #     for k, v in metadata.items():
    #         formatted_metadata += f",{k}={v}"

    #     formatted_data = ""
    #     for k, v in data.items():
    #         pre_delimin = '' if len(formatted_data) == 0 else ','
    #         formatted_data += f"{pre_delimin}{k}={v}"

    #     response = requests.post(
    #         f"{self.backend_url}/write?db={self.bucket}",
    #         f"{name}{formatted_metadata} {formatted_data} {timestamp_ns}",
    #     )
    #     if response.status_code != 204:
    #         print(response.text, response.status_code)
    #         print(f"Failed to push {name} metric ({','.join(data)}) at {timestamp_ns}")

    def send_bulk(
        self,
        metrics: List[Metric]
    ):
        """
        curl -i -XPOST 'http://localhost:8086/write?db=mydb' --data-binary 'cpu_load_short,host=server01,region=us-west value=0.64 1434055562000000000'"""
        # Build all the text lines for the curl
        lines = []
        for metric in metrics:
            # Destructure for readability
            name = metric.name
            timestamp_ns = metric.timestamp_ns
            data = metric.data
            metadata = metric.metadata

            formatted_metadata = ""
            for k, v in metadata.items():
                formatted_metadata += f",{k}={v}"

            formatted_data = ""
            for k, v in data.items():
                pre_delimin = '' if len(formatted_data) == 0 else ','
                formatted_data += f"{pre_delimin}{k}={v}"

            lines.append(f"{name}{formatted_metadata} {formatted_data} {timestamp_ns}")


        response = requests.post(
            f"{self.backend_url}/write?db={self.bucket}",
            '\n'.join(lines)
        )
            
        if response.status_code != 204:
            print(response.text, response.status_code)
            print(f"Failed to push {','.join([x.name for x in metrics])} metric")
