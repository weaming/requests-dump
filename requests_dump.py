#!/usr/bin/env python3
# coding: utf-8
"""
Author       : weaming
Created Time : 2019-01-14 13:07:43
"""

import sys
from io import BytesIO

# requests use urllib3 to do http request
from urllib3.packages.six.moves.http_client import HTTPConnection
import requests

version = "0.1"


def insert_middlewares(pre_funcs=None, post_funcs=None):
    pre_funcs = pre_funcs or []
    post_funcs = post_funcs or []

    def decorator(func):
        def new_fn(*args, **kwargs):
            for fn in pre_funcs:
                fn(*args, **kwargs)
            rv = func(*args, **kwargs)
            for fn in post_funcs:
                fn(rv)
            return rv

        return new_fn

    return decorator


class Capturer:
    def __init__(self, dump=True, dump_file=sys.stderr, decode=True):
        self.dump = dump
        self.dump_file = dump_file
        self.decode = decode

        self.buffer = BytesIO()
        self.capture_requests()

    def send(self, *args, **kwargs):
        """wapper to satisfy insert_middlewares()"""
        self.write(args[1])

    def try_dump(self, data: bytes):
        if self.dump:
            self.dump_file.write(data.decode() if self.decode else data)

    def write(self, data: bytes):
        self.buffer.write(data)
        self.try_dump(data)

    def getall(self):
        return self.buffer.getvalue()

    def capture_requests(self):
        self.origin_send = HTTPConnection.send
        HTTPConnection.send = insert_middlewares([self.send])(HTTPConnection.send)

    def unpatch(self):
        HTTPConnection.send = self.origin_send

    def finish(self):
        if self.dump:
            self.dump_file.write("\n" if self.decode else b"\n")


# consider use https://toolbelt.readthedocs.io/en/latest/dumputils.html instead
request_template = """{} {} HTTP/1.1
{}

{}"""

response_template = """HTTP/1.1 {} {}
{}

{}"""


def pretty_request(req):
    from urllib.parse import urlparse

    if isinstance(req, requests.Request):
        req = req.prepare()

    headers = {"Host": urlparse(req.url).netloc}
    headers.update(req.headers)
    return request_template.format(
        req.method,
        urlparse(req.url).path,
        "\n".join("{}: {}".format(k, v) for k, v in headers.items()),
        req.body,
    )


def pretty_response(res):
    return response_template.format(
        res.status_code,
        res.reason,
        "\n".join("{}: {}".format(k, v) for k, v in res.headers.items()),
        res.text,
    )
