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

import ast
import base64
import logging
import json
from typing import Any, Dict, List, Optional

import requests

from .models import UserProfile
from .http_client import HTTPClient
from .exceptions import MojangError

log = logging.getLogger(__name__)


class API(HTTPClient):

    _API_BASE_URL = "https://api.mojang.com"
    _SESSIONSERVER_BASE_URL = "https://sessionserver.mojang.com"
    _AUTHSERVER_BASE_URL = "https://authserver.mojang.com"

    def __init__(
        self,
        session: Optional[requests.Session] = None,
        ratelimit_sleep_duration: Optional[int] = 60,
        debug_mode: Optional[bool] = False,
    ):
        super().__init__(session, ratelimit_sleep_duration, debug_mode)

    def get_uuid(
        self,
        username: str,
        timestamp: Optional[int] = None,
    ) -> Optional[str]:
        """Convert a Minecraft name to a UUID.

        Warning: Limited Functionality
            As of November 2020, Mojang stopped supporting the timestamp parameter, which allowed
            users to get UUID of the name at the timestamp provided. If a timestamp is provided,
            it is silently ignored and the current UUID is returned. Please remind them to fix this here:
            [WEB-3367](https://bugs.mojang.com/browse/WEB-3367).

        Args:
            username:  The Minecraft username to be converted.
            timestamp (optional): Get the username's UUID at a specified UNIX timestamp.
                You can also get the username's first UUID by passing `0` to this parameter.
                However, this only works if the name was changed at least once, or if the account is legacy.

        Returns:
            The UUID (`str`) or `None` if the username does not exist.

        Example:
            ```py
            uuid = api.get_uuid("Notch")

            if not uuid:
                print("The username Notch is not taken")
            else:
                print(f"Notch's UUID is {uuid}")
            ```
        """

        if timestamp:
            url = f"{self._API_BASE_URLf}/users/profiles/minecraft/{username}?at={timestamp}"
        else:
            url = f"{self._API_BASE_URL}/users/profiles/minecraft/{username}"

        resp = self.session.get(url)

        if resp.status_code == 400:
            return None

        try:
            return resp.json()["id"]
        except json.decoder.JSONDecodeError:
            return None

    def get_uuids(self, names: List[str]) -> Dict[str, str]:
        """Convert up to 10 usernames to UUIDs in a single network request.

        Args:
            names: The Minecraft username(s) to be converted.
                If more than 10 are included, only the first 10 will be parsed.

        Returns:
            A dictionary object that contains the converted usernames. Names are also case-corrected.
            If a username does not exist, it will not be included in the returned dictionary.

        Example:
            ```py
            usernames = ["Notch", "Herobrine", "Dream"]

            players = api.get_uuids(usernames)

            for name, uuid in players.items():
                print(name, uuid)
            ```
        """
        if not isinstance(names, list):
            raise TypeError(
                "Invalid data type passed. Make sure that you are passing a list of UUIDs instead of a string or dictionary."
            )

        if len(names) > 10:
            names = names[:10]

        data = self.session.post(
            f"{self._API_BASE_URL}/profiles/minecraft", json=names
        ).json()

        if not isinstance(data, list):
            if data.get("error"):
                raise MojangError(data["errorMessage"])
            else:
                raise MojangError(data)

        return {name_data["name"]: name_data["id"] for name_data in data}

    def get_username(self, uuid: str) -> Optional[str]:
        """Convert a UUID to a username.

        Args:
            uuid: The Minecraft UUID to be converted to a username.

        Returns:
            The username. `None` otherwise.

        Example:
            ```py
            username = api.get_username("e149b689-d25c-4ace-a9ea-4be1e8407f85")

            if not username:
                print("UUID does not appear to be valid.")
            ```
        """
        resp = self.session.get(
            f"{self._SESSIONSERVER_BASE_URL}/session/minecraft/profile/{uuid}"
        )

        if resp.status_code == 400:
            return None

        try:
            return resp.json()["name"]
        except json.decoder.JSONDecodeError:
            return None

    def get_profile(self, uuid: str) -> Optional[UserProfile]:
        """Get more information about a user from their UUID

        Args:
            uuid: The Minecraft UUID

        Returns:
            `UserProfile` object. Otherwise, `None` if the profile does not exist.

        Example:
            ```py
            uuid = api.get_uuid("Notch")

            if uuid:
                profile = api.get_profile(uuid)

                print(profile.name)
                print(profile.skin_url)
                # other possible profile attributes include skin_model, cape_url,
                # is_legacy_profile, and timestamp
            ```
        """
        resp = self.session.get(
            f"{self._SESSIONSERVER_BASE_URL}/session/minecraft/profile/{uuid}"
        )

        try:
            value = resp.json()["properties"][0]["value"]
        except (KeyError, json.decoder.JSONDecodeError):
            return None
        user_profile = ast.literal_eval(base64.b64decode(value).decode())
        return UserProfile(user_profile)

    def get_blocked_servers(self) -> List[str]:
        """Get a list of SHA1 hashes of blacklisted Minecraft servers that do not follow EULA.
        These servers have to abide by the EULA or they will be shut down forever. The hashes are not cracked.

        Returns:
            Blacklisted server hashes

        Example:
            ```py
            servers = api.get_blocked_servers()

            for hash in servers:
                print(hash)
            ```
        """
        resp = self.session.get(f"{self._SESSIONSERVER_BASE_URL}/blockedservers")
        return resp.text.splitlines()

    def refresh_access_token(
        self, access_token: str, client_token: str
    ) -> Dict[str, Any]:
        """Refreshes access token

        Args:
            access_token: The access token to refresh.
            client_token: The client token that was used to obtain the access token.

        Returns:
            A dictionary object that contains the new access token and other account and profile information

        Example:
            ```py
            access_token = "YOUR_ACCESS_TOKEN"
            client_token = "YOUR_CLIENT_TOKEN"

            account = api.refresh_access_token(access_token, client_token)

            print("The new access token is " + account["access_token"])

            # main keys include...
            print(account["access_token"])
            print(account["client_token"])
            print(account["username"])
            print(account["uuid"])

            # these will only be populated if the account has a Minecraft profile
            print(account["profile_id"])
            print(account["profile_name"])
            ```
        """
        payload = {
            "accessToken": access_token,
            "clientToken": client_token,
            "requestUser": True,
        }

        account = {}
        data = self.session.post(
            f"{self._AUTHSERVER_BASE_URL}/refresh", json=payload
        ).json()

        account["username"] = data["user"]["username"]
        account["uuid"] = data["user"]["id"]
        account["access_token"] = data["accessToken"]
        account["client_token"] = data["clientToken"]
        if data.get("selectedProfile"):
            account["profile_id"] = data["selectedProfile"]["id"]
            account["profile_name"] = data["selectedProfile"]["name"]
        else:
            account["profile_id"] = None
            account["profile_name"] = None
        return account
