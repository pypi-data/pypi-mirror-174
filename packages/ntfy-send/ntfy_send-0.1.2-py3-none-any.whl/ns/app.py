# spdx-license-identifier: gpl-3.0-only
# Copyright (C) 2022 Michał Góral

import sys
import argparse
import logging

from ns.config import read_config, merge_args
from ns.send import send


log = logging.getLogger(__name__)


def prepare_args():
    parser = argparse.ArgumentParser(
        description="Send notifications through ntfy.sh service"
    )

    parser.add_argument("topic", help="subscribed topic")
    parser.add_argument(
        "message",
        nargs="?",
        help="message text or path to file which should be attached",
    )

    msg_group = parser.add_argument_group("message options")
    msg_group.add_argument("-T", "--title", help="message title")
    msg_group.add_argument(
        "-p", "--priority", type=int, choices=(1, 2, 3, 4, 5), help="message priority"
    )
    msg_group.add_argument(
        "-t",
        "--tag",
        dest="tags",
        action="append",
        default=[],
        help="message tags (can be specified many times",
    )
    msg_group.add_argument("-a", "--attach", metavar="URL", help="attach URL")
    msg_group.add_argument("-i", "--icon", metavar="URL", help="message icon")
    msg_group.add_argument(
        "-c", "--click", metavar="URL", help="URL which should open when clicked"
    )
    msg_group.add_argument(
        "-A",
        "--action",
        dest="actions",
        action="append",
        default=[],
        metavar="DEFINITION",
        help="message action buttons. DEFINITION should follows ntfy.sh HTTP header format for actions; can be used many times",
    )
    msg_group.add_argument("--at", help="delay notification by/until a given time")

    srv_group = parser.add_argument_group("server options")
    srv_group.add_argument(
        "-s",
        "--server",
        metavar="URL",
        help="change default ntfy server address",
    )
    srv_group.add_argument(
        "-U", "--username", help="username used to authenticate to the server"
    )
    srv_group.add_argument(
        "-P", "--password", help="password used to authenticate to the server"
    )

    return parser.parse_args()


def main():
    args = prepare_args()
    logging.basicConfig(format="%(message)s", level="INFO")

    config = read_config()
    merge_args(config, args)
    config.exec_commands()

    return not send(args, config)

    # requests.post()


sys.exit(main())
