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
from pyparsing import Group
from pyparsing import Literal as L
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import QuotedString
from pyparsing import White
from pyparsing import ZeroOrMore

from piglet import compilett
from piglet import parse

quote = L('"') | L("'")

quoted_string = (
    QuotedString(
        "'", escChar="\\", convertWhitespaceEscapes=False, multiline=True
    ).setParseAction(lambda ts: compilett.QuotedString(quote="'", content="".join(ts)))
    | QuotedString(
        '"', escChar="\\", convertWhitespaceEscapes=False, multiline=True
    ).setParseAction(lambda ts: compilett.QuotedString(quote='"', content="".join(ts)))
).setParseAction(lambda ts: ts[0])

directive_name = (
    L("for")
    | L("if")
    | L("extends")
    | L("block")
    | L("def")
    | L("import")
    | L("include")
    | L("with")
    | L("choose")
    | L("when")
    | L("else")
    | L("transname")
    | L("trans")
)

ws_control = L("-") | L("+")

maybe_ws = Optional(White())


def group_strings(ts):
    cur = []
    for t in ts:
        if isinstance(t, str):
            cur.append(t)
        else:
            if cur:
                yield "".join(cur)
                cur = []
            yield t
    if cur:
        yield "".join(cur)


args = ZeroOrMore(
    OneOrMore(CharsNotIn("'\"-+%"))
    | quoted_string
    | (ws_control + ~L("%}"))
    | (L("%") + ~L("}"))
).setParseAction(group_strings)


end_directive_name = ((L("end") + directive_name) | L("end")).setParseAction("".join)

open_directive = (
    L("{%")
    + Optional(ws_control).setResultsName("ws_before")
    + maybe_ws().setResultsName("space1")
    + directive_name().setResultsName("name")
    + maybe_ws().setResultsName("space2")
    + (Group(args).setResultsName("args"))
    + Optional(ws_control()).setResultsName("ws_after")
    + L("%}")
).setParseAction(lambda ts: compilett.Statement(**ts))

close_directive = (
    L("{%")
    + Optional(ws_control).setResultsName("ws_before")
    + maybe_ws().setResultsName("space1")
    + end_directive_name.setResultsName("name")
    + maybe_ws().setResultsName("space2")
    + Optional(ws_control()).setResultsName("ws_after")
    + L("%}")
).setParseAction(lambda ts: compilett.Statement(**ts))

directive = open_directive | close_directive

text = OneOrMore(OneOrMore(CharsNotIn("{")) | (L("{") + ~L("%"))).setParseAction(
    lambda ts: parse.Text(cdata=True, content="".join(ts))
)

text_template = ZeroOrMore(text | directive)

text_template_parser = text_template()
text_template_parser.leaveWhitespace()
text_template_parser.parseWithTabs()
text_template_parser.enablePackrat()
