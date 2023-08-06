# This file is part of the project mb-netmgmt
#
# (C) 2022 Deutsche Telekom AG
#
# Deutsche Telekom AG and all other contributors / copyright
# owners license this file to you under the terms of the GPL-2.0:
#
# mb-netmgmt is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# mb-netmgmt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mb-netmgmt. If not, see <https://www.gnu.org/licenses/

"""Network Management Protocols for Mountebank"""
__version__ = "0.0.49"

import os
import subprocess
import time
from contextlib import contextmanager

import requests
import yaml


@contextmanager
def mb(imposters, loglevel="info"):
    with start_mb(loglevel) as mb:
        try:
            put_imposters("localhost", imposters)
            yield mb
        finally:
            mb.terminate()


def start_mb(loglevel="info"):
    return subprocess.Popen(
        ["mb", "--loglevel", loglevel, "--pidfile", "/tmp/mb.pid"],
        cwd=os.path.dirname(__file__),
    )


def put_imposters(host, imposters, port=2525):
    while True:
        try:
            response = requests.put(
                f"http://{host}:{port}/imposters",
                json={"imposters": imposters},
            )
            break
        except requests.ConnectionError:
            time.sleep(1)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(e.response.json()["errors"])


def dump_imposters(host, name):
    imposters = get_imposters(host)

    def str_presenter(dumper, data):
        style = "|" if len(data.splitlines()) > 1 else None
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)

    yaml.representer.SafeRepresenter.add_representer(str, str_presenter)
    yaml.safe_dump(imposters, open(f"{name}.yaml", "w"), width=None)


def get_imposters(host):
    response = requests.get(
        f"http://{host}:2525/imposters",
        {"replayable": True, "removeProxies": True},
    )
    return response.json()


def load_imposters(host, name):
    put_imposters(host, read_imposters(name))


def read_imposters(name):
    return yaml.safe_load(open(f"{name}.yaml").read())["imposters"]


def proxy_imposters(to, snmp_port=161, telnet_port=23, netconf_port=830):
    return [
        proxy_imposter(snmp_port, "snmp", to, "oids"),
        proxy_imposter(telnet_port, "telnet", to, "command"),
        proxy_imposter(
            netconf_port,
            "netconf",
            f"netconf://{os.environ['NETCONF_USERNAME']}:{os.environ['NETCONF_PASSWORD']}@{to}",
            "rpc",
        ),
    ]


def proxy_imposter(port, protocol, to, predicate_generator):
    return {
        "port": port,
        "protocol": protocol,
        "stubs": proxy_stubs(to, predicate_generator),
    }


def proxy_stubs(to, predicate_generator):
    return [
        {
            "responses": [
                {
                    "proxy": {
                        "mode": "proxyAlways",
                        "predicateGenerators": [
                            {"matches": {predicate_generator: True}}
                        ],
                        "to": to,
                    }
                }
            ]
        }
    ]
