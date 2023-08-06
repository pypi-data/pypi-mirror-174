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
from typing import Any, Dict, Optional
import re
import logging
import json

import requests

from .http_client import HTTPClient
from .exceptions import (
    MojangError,
    HTTPException,
    LoginError,
    MissingMinecraftLicense,
    MissingMinecraftProfile,
)
from .models import UserProfile, Profile, Skin, Cape, NameInformation

log = logging.getLogger(__name__)


BASE_API_URL = "https://api.minecraftservices.com"

_XErrors = {
    2148916233: "The account doesn't have an Xbox account.",
    2148916235: "The account is from a country where Xbox Live is not available/banned.",
    2148916236: "The account needs adult verification on Xbox page. (South Korea)",
    2148916237: "The account needs adult verification on Xbox page. (South Korea)",
    2148916238: "The account is a child (under 18) and cannot proceed unless the account is added to a Family by an adult.",
}


class MojangAuth(HTTPClient):
    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        bearer_token: Optional[str] = None,
        session: Optional[requests.Session] = None,
        ratelimit_sleep_duration: Optional[int] = 60,
        debug_mode: Optional[bool] = False,
    ):
        super().__init__(session, ratelimit_sleep_duration, debug_mode)

        self.email = email
        self.password = password
        self.bearer_token = bearer_token

        if bearer_token:
            self._set_authorization_header(bearer_token)
        elif not email and not password:
            raise TypeError(
                "Either an email/password or bearer token must be supplied."
            )
        else:
            self._login()

        self._validate_session()

    def _validate_session(self):
        resp = self._get(f"{BASE_API_URL}/entitlements/mcstore")

        if not resp.text:
            raise LoginError("The bearer token is invalid.")

        if resp.status_code == 401:
            raise MissingMinecraftLicense

        data = resp.json()

        if not bool(data["items"]):
            raise MissingMinecraftLicense

        # This check still needs to be verified
        resp = self._get(f"{BASE_API_URL}/minecraft/profile")
        if not resp.ok:
            raise MissingMinecraftProfile

    def _set_authorization_header(self, bearer_token: str) -> None:
        if not bearer_token.startswith("Bearer"):
            bearer_token = f"Bearer {bearer_token}"

        self.session.headers.update({"Authorization": f"{bearer_token}"})

    def _get_oauth2_token_and_url(self):
        """Begins the Microsoft OAuth2 Flow"""
        params = {
            "client_id": "000000004C12AE6F",
            "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
            "scope": "service::user.auth.xboxlive.com::MBI_SSL",
            "display": "touch",
            "response_type": "token",
            "locale": "en",
        }

        resp = self._get("https://login.live.com/oauth20_authorize.srf", params=params)

        # Parses the values via regex since the HTML can't be parsed
        value = re.search(r'value="(.+?)"', resp.text)[0].replace('value="', "")[:-1]
        url = re.search(r"urlPost:'(.+?)'", resp.text)[0].replace("urlPost:'", "")[:-1]

        return value, url

    def _authenticate_with_microsoft(self, token: str, url: str):
        """Authenticates with Microsoft"""
        payload = {
            "login": self.email,
            "loginfmt": self.email,
            "passwd": self.password,
            "PPFT": token,
        }

        resp = self._post(url, data=payload)
        if "access_token" not in resp.url:
            raise LoginError

        raw_login_data = resp.url.split("#")[1]
        data = dict(item.split("=") for item in raw_login_data.split("&"))

        access_token = requests.utils.unquote(data["access_token"])
        refresh_token = requests.utils.unquote(data["refresh_token"])

        return access_token, refresh_token

    def _authenticate_with_xboxlive(self, access_token: str):
        """Authenticates with XBL"""
        json_data = {
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": access_token,
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
        }

        resp = self._post(
            "https://user.auth.xboxlive.com/user/authenticate", json=json_data
        )

        xbl_token = resp.json()["Token"]
        user_hash = resp.json()["DisplayClaims"]["xui"][0]["uhs"]

        return xbl_token, user_hash

    def _get_xsts_token(self, xbl_token: str):
        """Gets the XSTS token which is required to authenticate with Minecraft services"""
        json_data = {
            "Properties": {"SandboxId": "RETAIL", "UserTokens": [xbl_token]},
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT",
        }

        resp = self._post(
            "https://xsts.auth.xboxlive.com/xsts/authorize", json=json_data
        )

        if resp.status_code == 401:
            data = resp.json()
            if data["XErr"]:
                if data["XErr"] in _XErrors:
                    raise LoginError(data["XErr"])
                raise HTTPException(resp)

        return resp.json()["Token"]

    def _authenticate_with_minecraft(self, user_hash: str, xsts_token: str):
        json_payload = {
            "identityToken": f"XBL3.0 x={user_hash};{xsts_token}",
            "ensureLegacyEnabled": True,
        }

        resp = self._post(
            f"{BASE_API_URL}/authentication/login_with_xbox",
            json=json_payload,
        )

        return resp.json()

    def _login(self):
        token, url = self._get_oauth2_token_and_url()
        access_token, refresh_token = self._authenticate_with_microsoft(token, url)
        xbl_token, user_hash = self._authenticate_with_xboxlive(access_token)
        xsts_token = self._get_xsts_token(xbl_token)
        data = self._authenticate_with_minecraft(user_hash, xsts_token)

        self.bearer_token = data["access_token"]

        self._set_authorization_header(self.bearer_token)


class Client(MojangAuth):
    def get_profile(self) -> Profile:
        """Get information about the current profile.

        Returns:
            A `Profile` object that contains information about a Minecraft profile

        Example:
            ```py
            profile = client.get_profile()

            print(profile.id)
            print(profile.name)

            for skin in profile.skins:
                print(skin.id)
                print(skin.enabled)
                print(skin.url)
                print(skin.variant)
            ```
        """
        data = self._get(f"{BASE_API_URL}/minecraft/profile").json()

        capes = []
        skins = []

        if data.get("capes"):
            for cape_data in data["capes"]:
                cape = Cape(
                    id=cape_data["id"],
                    enabled=(cape_data["state"] == "ACTIVE"),
                    url=cape_data["url"],
                    alias=cape_data["alias"],
                )
                capes.append(cape)

        if data.get("skins"):
            for skin_data in data["skins"]:
                skin = Skin(
                    id=skin_data["id"],
                    enabled=(skin_data["state"] == "ACTIVE"),
                    url=skin_data["url"],
                    variant=skin_data["variant"],
                    alias=skin_data.get("alias"),
                )
                skins.append(skin)

        return Profile(
            id=data["id"],
            name=data["name"],
            capes=capes,
            skins=skins,
        )

    def get_name_change_info(self) -> Dict[str, Any]:
        """Check if the account's username can be changed.

        Returns:
            A dictionary object that contains information about the account's username. \
                Possible keys are `changed_at`, `created_at`, \
                and `name_change_allowed`.

        Example:
            ```py
            name_obj = client.get_name_change_info()

            if name_obj.name_change_allowed:
                print("A name change is allowed")

            print(name_obj.changed_at)
            print(name_obj.created_at)
            ```
        """
        data = self._get(f"{BASE_API_URL}/minecraft/profile/namechange").json()

        return NameInformation(
            changed_at=data.get("changedAt"),
            created_at=data.get("createdAt"),
            name_change_allowed=data.get("nameChangeAllowed"),
        )

    def is_username_available(self, username: str) -> bool:
        """Check if a username is available.

        Warning: Limitations
            A username must be between 3 and 16 characters and cannot contain invalid characters.
            If any of these constraints are broken, or if a username has already been taken by someone else,
            this function will return `False`.

        Args:
            username: The Minecraft username to check.

        Returns:
            `True` if the username is available; `False` if the username is invalid or already taken

        Example:
            ```py
            if client.is_username_available("Notch"):
                print("The username Notch is available.")
            else:
                print("The username Notch is not available.")
            ```
        """

        resp = self._get(f"{BASE_API_URL}/minecraft/profile/name/{username}/available")

        return bool(resp.json().get("name"))

    def is_username_blocked(self, username: str) -> bool:
        """
        Check if a username is blocked by Mojang's username filter.

        Note:
            This function allows for the checking of usernames that have potentially been blocked.
            Blocking can happen either one of two ways - a username sniper has blocked the name for 24 hours on
            an empty Mojang account, or the username has been blocked by Mojang's inappropriate name filter for
            whatever reason. The reasons names are blocked aren't public, but this endpoint is the best way to
            check if a name is blocked.

        Args:
            username: The Minecraft username to check.

        Returns:
            `True` if the username is blocked; `False` if the username is not blocked
        """
        resp = self._get(f"{BASE_API_URL}/minecraft/profile/name/{username}/available")

        data = resp.json()

        if data.get("status"):
            if data["status"] == "NOT_ALLOWED":
                return True

        return False

    def change_username(self, username: str) -> Dict[str, Any]:
        """Change your Minecraft username.

        Warning: Limitations
            You can only change your username once every 30 days. A username must be
            between 3 and 16 characters and cannot contain invalid characters.

        Args:
            username:  The username you want to change to.

        Returns:
            A dictionary object that contains information about whether the username was claimed. \
                Possible keys are `success` (which contains `True` or `False`) and `error` with an error message \
                (only if the function fails).

        Example:
            ```py
            data = client.change_username("Notch")
            if not data["success"]:
                print(data["error"])
            elif data["success"]:
                print("The username Notch has successfully been claimed.")
            ```
        """

        resp = self._put(f"{BASE_API_URL}/minecraft/profile/name/{username}")

        if resp.ok:
            return dict(success=True)

        data = resp.json()

        if data.get("errorMessage"):
            if data["error"] == "FORBIDDEN":
                return dict(
                    success=False,
                    error="This username is already taken or the account does not have an available name change.",
                )

            error_message = data["errorMessage"].replace(
                "changeProfileName.profileName:", ""
            )
            return dict(success=False, error=error_message)

        raise HTTPException(resp)

    def change_skin(
        self,
        variant: Optional[str] = "classic",
        url: Optional[str] = None,
        image_path: Optional[str] = None,
    ) -> None:
        """Set a new skin for your profile.

        Skin Requirements:
            Image dimensions have to be **64x32**. The max allowed image size is 24576 bytes (24.576 KB). This function
            will raise a `MojangError` if the skin variant, or the provided image path or URL is invalid for some reason.

        Args:
            variant: Set "slim" for the slim model, or "classic" for the default.
            url: A direct image URL to the skin you want to change to.
            image_path: The file name or full file path to the skin image file.

        Raises:
            MojangError: If the skin could not be changed for some reason.

        Example:
            ```py
            # Change your skin via URL
            skin_url = "http://textures.minecraft.net/texture/2ff6d970b1b6243fe5a44c5ac540c320506987a5c55ba99a90f758b00d3e05a1"
            client.change_skin(variant="slim", url=skin_url)

            # Change your skin via file path / image name
            client.change_skin(variant="classic", image_path="skin.png")
            ```
        """
        variant = variant.strip().lower()

        if variant != "slim" and variant != "classic":
            raise ValueError("Skin variant must be set to either slim or classic.")

        if not image_path and not url:
            raise TypeError(
                "Missing required parameters. Please supply a skin URL or a skin image path."
            )

        if url:
            json_payload = {"url": url, "variant": variant}
            resp = self._post(
                f"{BASE_API_URL}/minecraft/profile/skins", json=json_payload
            )
        else:
            files = {
                "file": open(f"{image_path}", "rb"),
                "variant": (None, variant),
            }
            resp = self._post(f"{BASE_API_URL}/minecraft/profile/skins", files=files)

        if not resp.ok:
            error_message = resp.json()["errorMessage"]
            raise MojangError(error_message)

    def copy_skin(
        self,
        username: Optional[str] = None,
        uuid: Optional[str] = None,
    ) -> None:
        """Copy another player's Minecraft skin and skin variant. This will set their skin on your account.

        Pass either the player's username or their UUID - not both.

        Args:
            username: The username of the player whose skin you want to copy.
            uuid: The UUID of the player whose skin you want to copy.

        Raises:
            MojangError: If an invalid username or UUID is supplied.

        Example:
            ```py
            # Copy Notch's skin
            client.copy_skin("Notch")
            ```
        """
        if not username and not uuid:
            raise TypeError("Either a username or a UUID must be supplied")
        if username:
            resp = self._get(
                f"https://api.mojang.com/users/profiles/minecraft/{username}"
            )
            try:
                uuid = resp.json()["id"]
            except json.decoder.JSONDecodeError:
                raise MojangError("Username does not exist")

        resp = self._get(
            f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        )

        try:
            value = resp.json()["properties"][0]["value"]
        except (KeyError, json.decoder.JSONDecodeError):
            raise MojangError("Invalid UUID supplied")

        data = ast.literal_eval(base64.b64decode(value).decode())
        profile = UserProfile(data)

        if not profile.skin_url:
            raise MojangError("User does not have a skin")

        self.change_skin(
            url=profile.skin_url,
            variant=profile.skin_variant,
        )

    def change_skin_variant(self, variant: str) -> None:
        """Change the skin variant for your current Minecraft skin.

        Args:
            variant: Set "slim" for the slim model, or "classic" for the default.

        Example:
            ```py
            # Change your skin model to classic
            client.change_skin_variant("classic")

            # Change your skin model to slim
            client.change_skin_variant("slim")
            ```
        """
        profile = self.get_profile()
        self.change_skin(url=profile.skins[0].url, variant=variant)

    def reset_skin(self) -> None:
        """Reset your Minecraft skin back to the default one"""
        self._delete(f"{BASE_API_URL}/minecraft/profile/skins/active")
