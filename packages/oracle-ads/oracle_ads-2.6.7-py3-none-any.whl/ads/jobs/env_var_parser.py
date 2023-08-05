#!/usr/bin/env python
# -*- coding: utf-8; -*-

# Copyright (c) 2021, 2022 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/
from typing import Union, List, Dict
from configparser import ConfigParser, ExtendedInterpolation
from configparser import (
    InterpolationSyntaxError,
    InterpolationDepthError,
    InterpolationMissingOptionError,
)
from configparser import NoSectionError, NoOptionError, MAX_INTERPOLATION_DEPTH


class EnvVarInterpolation(ExtendedInterpolation):
    def before_set(self, parser, section: str, option: str, value: str) -> str:
        return value

    def _interpolate_some(self, parser, option, accum, rest, section, map, depth):
        rawval = parser.get(section, option, raw=True, fallback=rest)
        if depth > MAX_INTERPOLATION_DEPTH:
            raise InterpolationDepthError(option, section, rawval)
        while rest:
            p = rest.find("$")
            if p < 0:
                accum.append(rest)
                return
            if p > 0:
                accum.append(rest[:p])
                rest = rest[p:]
            # p is no longer used
            c = rest[1:2]
            if c == "$":
                accum.append("$")
                rest = rest[2:]
            elif c == "{":
                m = self._KEYCRE.match(rest)
                if m is None:
                    raise InterpolationSyntaxError(
                        option,
                        section,
                        "Bad interpolation variable reference %r" % rest,
                    )
                path = m.group(1).split(":")
                rest = rest[m.end() :]
                sect = section
                opt = option
                try:
                    if len(path) == 1:
                        opt = parser.optionxform(path[0])
                        v = map[opt]
                    elif len(path) == 2:
                        sect = path[0]
                        opt = parser.optionxform(path[1])
                        v = parser.get(sect, opt, raw=True)
                    else:
                        raise InterpolationSyntaxError(
                            option, section, "More than one ':' found: %r" % (rest,)
                        )
                except (KeyError, NoSectionError, NoOptionError):
                    accum.append(rawval)
                    return
                if "$" in v:
                    self._interpolate_some(
                        parser,
                        opt,
                        accum,
                        v,
                        sect,
                        dict(parser.items(sect, raw=True)),
                        depth + 1,
                    )
                else:
                    accum.append(v)
            else:
                accum.append("$")
                rest = rest[1:]


def parse(env_var: Union[Dict, List[dict]]) -> dict:
    """Parse the environment variables and perform substitutions.
    This will also converts kubernetes style environment variables from a list to a dictionary.

    Parameters
    ----------
    env_var : dict or list
        Environment variables specified as a list or a dictionary.
        If evn_var is a list, it should be in the format of:
            "[{"name": "ENV_NAME_1", "value": "ENV_VALUE_1"}, {"name": "ENV_NAME_2", "value": "ENV_VALUE_2"}]

    Returns
    -------
    dict
        Environment variable as a dictionary.
    """
    # Convert kubernetes style env to dict
    if isinstance(env_var, list):
        env_var = {ev["name"]: ev["value"] for ev in env_var}
    config = ConfigParser(interpolation=EnvVarInterpolation())
    config.optionxform = str
    config["envs"] = env_var
    return {k: config["envs"].get(k) for k in env_var.keys()}


def escape(s: str) -> str:
    return s.replace("$", "$$")
