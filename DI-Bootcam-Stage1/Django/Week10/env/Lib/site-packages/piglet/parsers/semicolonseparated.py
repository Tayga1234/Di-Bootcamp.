# Copyright 2021 Oliver Cope
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

from pyparsing import CharsNotIn
from pyparsing import Literal as L
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import QuotedString
from pyparsing import Suppress
from pyparsing import White
from pyparsing import ZeroOrMore

separator = L(";")
single_quote = L("'")
double_quote = L('"')
triple_quote = L('"""') | L("'''")

quoted_string = (
    QuotedString("'", escChar="\\", unquoteResults=False)
    | QuotedString('"', escChar="\\", unquoteResults=False)
    | QuotedString('"""', escChar="\\", unquoteResults=False)
    | QuotedString("'''", escChar="\\", unquoteResults=False)
).setName("quoted string")

text = CharsNotIn("\"';")
value = OneOrMore(text | quoted_string).setResultsName("value").setParseAction("".join)

ssv_parser = (
    value
    + ZeroOrMore(Suppress(Optional(White()) + separator + Optional(White())) + value)
).setParseAction(lambda ts: list(ts))
