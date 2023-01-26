# Copyright 2016 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from copy import copy

import attr
import pyparsing

from piglet.exceptions import PigletParseError
from piglet import parsers


@attr.s
class Interpolation(object):
    source = attr.ib()
    value = attr.ib()

    autoescape = True

    def noescape(self):
        ob = copy(self)
        ob.autoescape = False
        return ob


def parse_interpolations(source):
    try:
        parse_result = parsers.interpolation_parser.parseString(source)
    except pyparsing.ParseException as e:
        raise PigletParseError() from e
    return list(parse_result)
