# spdx-license-identifier: gpl-3.0-only
# Copyright (C) 2022 Michał Góral

from typing import Any, Optional, Dict, Union

import os
import base64
import logging
from urllib.parse import urljoin
from argparse import Namespace

import requests

from ns.config import Config


log = logging.getLogger(__name__)


def get_auth(username: str, password: str) -> bytes:
    if username or password:
        creds = f"{username}:{password}"
        return base64.b64encode(creds.encode("utf-8"))
    return None


def set_header(name: str, headers: Dict[str, Union[str, bytes]], val: Optional[Any]):
    if val is not None:
        headers[name] = val


def send(args: Namespace, c: Config) -> bool:
    url = urljoin(c.server, args.topic)

    headers = {}
    auth = get_auth(c.username, c.password)
    if auth:
        headers["Authorization"] = "Basic ".encode("utf-8") + auth

    if args.priority:
        headers["Priority"] = str(args.priority)

    if args.tags:
        headers["Tags"] = ",".join(args.tags)

    if args.attach:
        headers["Attach"] = args.attach

    if args.icon:
        headers["Icon"] = args.icon

    if args.click:
        headers["Click"] = args.click

    if args.at:
        headers["At"] = args.at

    if args.actions:
        headers["Actions"] = ";".join(args.actions)

    # message is a local path and should be treated as attachment
    if args.message and os.path.exists(args.message):
        with open(args.message, "rb") as mf:
            headers["Filename"] = os.path.basename(args.message)
            args.message = mf.read()

    kw = {"headers": headers}
    if args.message:
        kw["data"] = args.message
    resp = requests.post(url, **kw)

    if resp.text:
        log.info(resp.text.strip())

    if not resp.ok:
        log.error("Sending notification failed")
        return False

    return True
