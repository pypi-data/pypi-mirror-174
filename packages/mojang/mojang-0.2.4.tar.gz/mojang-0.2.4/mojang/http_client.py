"""
The MIT License (MIT)

Copyright (c) 2020-present https://github.com/summer

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import time
from typing import Any
import logging

import requests

from http.client import HTTPConnection

log = logging.getLogger(__name__)


class HTTPClient:
    def __init__(
        self,
        session: requests.Session = None,
        ratelimit_sleep_duration: int = 60,
        debug_mode: bool = False,
    ):
        self.ratelimit_sleep_duration = ratelimit_sleep_duration

        if session:
            self.session = session
        else:
            self.session = requests.Session()

            self.session.headers.update(
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    "(KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
                }
            )

        if debug_mode:
            HTTPConnection.debuglevel = 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("requests.packages.urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def request(self, method: str, url: str, **kwargs: Any) -> Any:
        """Internal request handler"""

        for i in range(10):
            resp = self.session.request(method, url, **kwargs)

            log.debug(f"Making API request: {method} {url}\n")

            if resp.ok:
                return resp

            if resp.status_code == 429:
                log.warning(f"The server is ratelimiting us at the moment: {url}")
                log.warning(
                    f"Sleeping for {self.ratelimit_sleep_duration} seconds before trying again..."
                )
                time.sleep(self.ratelimit_sleep_duration)
                continue
            elif resp.status_code == 529:
                log.warning(f"The server is overloaded at the moment: {url}")
            elif resp.status_code == 500:
                log.warning(f"The server is denying our requests: {url}")
            else:
                return resp

            time.sleep(2**i)

        # We've run out of request retries
        raise Exception(resp, resp.text)

    def _get(self, url: str, **kwargs: Any) -> Any:
        return self.request("GET", url, **kwargs)

    def _post(self, url: str, **kwargs: Any) -> Any:
        return self.request("POST", url, **kwargs)

    def _put(self, url: str, **kwargs: Any) -> Any:
        return self.request("PUT", url, **kwargs)

    def _delete(self, url: str, **kwargs: Any) -> Any:
        return self.request("DELETE", url, **kwargs)
