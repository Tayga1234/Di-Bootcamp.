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
from pyparsing import Empty
from pyparsing import Forward
from pyparsing import Group
from pyparsing import Literal as L
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import QuotedString
from pyparsing import White
from pyparsing import Word
from pyparsing import ZeroOrMore
from pyparsing import alphanums
from pyparsing import alphas
from pyparsing import nums

from piglet import interpolate
from piglet.parsers.text import group_strings


escaped_dollar = L("$$").setParseAction(lambda: "$")
lone_dollar = L("$")


identifier = Word(alphas + "_", alphanums + "_").setName("identifier")

maybe_ws = Optional(White())

index = Word(nums) | "-" + maybe_ws + Word(nums)
maybe_index = Optional(index)
range_ = ":" + maybe_ws + maybe_index
slice_ = (
    (maybe_ws + maybe_index + maybe_ws + Optional(range_) + maybe_ws + Optional(range_))
    | index
    | QuotedString("'\"", escChar="\\")
)


brace_balanced_expr = Forward()
brace_balanced_expr <<= (
    OneOrMore(
        (CharsNotIn("{}") | Empty())
        + "{"
        + brace_balanced_expr
        + "}"
        + (CharsNotIn("{}") | Empty())
    )
    | ("{" + brace_balanced_expr + "}")
    | CharsNotIn("{}")
    | Empty()
)
delimited_expr = "{" + Group(brace_balanced_expr).setResultsName("x") + "}"
delimited_expr.setParseAction(
    lambda ts: "".join(ts.x),
    lambda ts: interpolate.Interpolation("${" + ts[0] + "}", ts[0]),
)

simple_expr = (
    (identifier + ZeroOrMore(("." + identifier) | ("[" + slice_ + "]")))
    .setResultsName("x")
    .setParseAction(
        lambda ts: "".join(ts.x),
        lambda ts: interpolate.Interpolation("$" + ts[0], ts[0]),
    )
)

interpolation = (
    "$" + (simple_expr | delimited_expr).setResultsName("expr")
).setParseAction(lambda ts: ts.expr)

escaped_interpolation = (
    "$!" + (simple_expr | delimited_expr).setResultsName("expr")
).setParseAction(lambda ts: ts.expr[0].noescape())

text_with_interpolations = ZeroOrMore(
    OneOrMore(CharsNotIn("$"))
    | escaped_interpolation
    | interpolation
    | escaped_dollar
    | lone_dollar
).setParseAction(lambda ts: list(group_strings(ts)))

interpolation_parser = text_with_interpolations()
interpolation_parser.leaveWhitespace()
interpolation_parser.parseWithTabs()
interpolation_parser.enablePackrat()
