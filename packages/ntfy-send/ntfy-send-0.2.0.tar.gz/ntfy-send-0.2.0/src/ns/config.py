# spdx-license-identifier: gpl-3.0-only
# Copyright (C) 2022 Michał Góral

from typing import Optional

import os
import sys
import subprocess
import logging
from dataclasses import dataclass
from argparse import Namespace

import tomlkit


log = logging.getLogger(__name__)


def _run_cmd(cmd: str) -> Optional[str]:
    try:
        cp = subprocess.run(cmd, text=True, capture_output=True, check=True, shell=True)
    except subprocess.CalledProcessError:
        log.error("Command failed: %s", cmd)
        return None
    return cp.stdout


@dataclass
class Config:
    server: str = ""
    username: Optional[str] = None
    password: Optional[str] = None

    def exec_commands(self):
        for name in self.__dataclass_fields__:
            val = getattr(self, name, None)
            if isinstance(val, str):
                val = val.strip()
                if len(val) > 2 and val[0] == "`" and val[-1] == "`":
                    new_val = _run_cmd(val[1:-1])
                    if new_val is None:
                        sys.exit(1)
                    setattr(self, name, new_val)


def merge_args(config: Config, args: Namespace):
    for name in config.__dataclass_fields__:
        attr_val = getattr(args, name, None)
        if attr_val is not None:
            setattr(config, name, attr_val)


def read_config() -> Config:
    home = os.path.expanduser("~")
    config_home = os.getenv("XDG_CONFIG_HOME", os.path.join(home, ".config"))
    path = os.path.join(config_home, "ntfy-send", "config.tomla")

    if not os.path.exists(path):
        path = os.path.join("/etc", "ntfy-send", "config.toml")

    try:
        with open(path, encoding="utf-8") as cfgf:
            doc = tomlkit.parse(cfgf.read())
    except FileNotFoundError:
        doc = {}

    return Config(**doc)
