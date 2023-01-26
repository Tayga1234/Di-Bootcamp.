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
from pyparsing import Regex
from pyparsing import SkipTo
from pyparsing import White
from pyparsing import Word
from pyparsing import ZeroOrMore
from pyparsing import alphanums
from pyparsing import alphas
from pyparsing import hexnums
from pyparsing import nums

from piglet import parse

# https://infra.spec.whatwg.org/#noncharacter
html5_non_chars = (
    "\U0000fdd0"
    "\U0000fdd1"
    "\U0000fdd2"
    "\U0000fdd3"
    "\U0000fdd4"
    "\U0000fdd5"
    "\U0000fdd6"
    "\U0000fdd7"
    "\U0000fdd8"
    "\U0000fdd9"
    "\U0000fdda"
    "\U0000fddb"
    "\U0000fddc"
    "\U0000fddd"
    "\U0000fdde"
    "\U0000fddf"
    "\U0000fffe"
    "\U0000ffff"
    "\U0001fffe"
    "\U0001ffff"
    "\U0002fffe"
    "\U0002ffff"
    "\U0003fffe"
    "\U0003ffff"
    "\U0004fffe"
    "\U0004ffff"
    "\U0005fffe"
    "\U0005ffff"
    "\U0006fffe"
    "\U0006ffff"
    "\U0007fffe"
    "\U0007ffff"
    "\U0008fffe"
    "\U0008ffff"
    "\U0009fffe"
    "\U0009ffff"
    "\U000afffe"
    "\U000affff"
    "\U000bfffe"
    "\U000bffff"
    "\U000cfffe"
    "\U000cffff"
    "\U000dfffe"
    "\U000dffff"
    "\U000efffe"
    "\U000effff"
    "\U000ffffe"
    "\U000fffff"
    "\U0010fffe"
    "\U0010ffff"
)

# https://html.spec.whatwg.org/multipage/syntax.html#attributes-2
attribute_name = Regex(f"[^ \"'>/=\u0000-\u001f\u007F-\u009F{html5_non_chars}]+")
# Spec does not specify which characters are valid in tag names, other than
# to say that 'HTML elements all have names that only use ASCII alphanumerics'
tag_name = Word(alphanums, alphanums + "-")
qname = (
    (ZeroOrMore(tag_name + ":") + tag_name)
    .setName("qname")
    .setResultsName("qname")
    .setParseAction("".join)
)

quoted_string = (
    L('"').setResultsName("qsquote") + SkipTo('"').setResultsName("qscontent") + '"'
) | (L("'").setResultsName("qsquote") + SkipTo("'").setResultsName("qscontent") + "'")

attribute = (
    attribute_name().setResultsName("name")
    + Optional(White()).setResultsName("space1")
    + Optional("=" + Optional(White()).setResultsName("space2") + quoted_string())
    + Optional(White()).setResultsName("space3")
).setParseAction(
    lambda ts: (
        ts.name,
        parse.Attribute(
            name=ts.name,
            quote=ts.qsquote,
            value=ts.get("qscontent"),
            space1=ts.space1,
            space2=ts.space2,
            space3=ts.space3,
        ),
    )
)

open_tag = (
    "<"
    + qname
    + Optional(
        White().setResultsName("space") + ZeroOrMore(attribute).setResultsName("attrs")
    )
    + ">"
).setParseAction(
    lambda ts: parse.OpenTag(qname=ts.qname, space=ts.space, attrs=list(ts.attrs))
)

close_tag = "</" + qname + ">"
close_tag.setParseAction(lambda ts: parse.CloseTag(qname=ts.qname))

text = OneOrMore(CharsNotIn("<&"))
text.setParseAction(lambda ts: parse.Text(content=ts[0]))

cdata_open_tag = (
    "<"
    + (L("script") | L("style")).setResultsName("tagname")
    + Optional(
        White().setResultsName("space") + ZeroOrMore(attribute).setResultsName("attrs")
    )
    + ">"
).setParseAction(
    lambda ts: parse.OpenTag(qname=ts.tagname, space=ts.space, attrs=list(ts.attrs))
)

cdata_close_tag = (
    "</" + (L("script") | L("style")).setResultsName("tagname") + ">"
).setParseAction(lambda ts: parse.CloseTag(qname=ts.tagname))

open_close_tag = (
    L("<")
    + qname().setResultsName("qname")
    + Optional(White()).setResultsName("space")
    + ZeroOrMore(attribute).setResultsName("attrs")
    + "/>"
).setParseAction(
    lambda ts: parse.OpenCloseTag(qname=ts.qname, space=ts.space, attrs=list(ts.attrs))
)

implicit_cdata = (
    cdata_open_tag().setResultsName("opentag")
    + SkipTo(cdata_close_tag).setResultsName("content")
    + cdata_close_tag().setResultsName("closetag")
).setParseAction(
    lambda ts: [ts.opentag, parse.Text(content=ts.content, cdata=True), ts.closetag]
)

alpha_entity = (L("&") + Word(alphas) + L(";")).setParseAction("".join)
numeric_entity = (L("&#") + Word(nums) + L(";")).setParseAction("".join)
hex_entity = (L("&#x") + Word(hexnums) + L(";")).setParseAction("".join)
entity = (
    (alpha_entity | hex_entity | numeric_entity)
    .setParseAction("".join)
    .setResultsName("reference")
    .setParseAction(lambda ts: parse.Entity(reference="".join(ts.reference)))
)

comment = (
    L("<!--") + SkipTo("-->").setResultsName("content") + L("-->")
).setParseAction(lambda ts: parse.Comment(**ts))

cdata = (
    L("<![CDATA[") + SkipTo("]]>").setResultsName("content") + L("]]>")
).setParseAction(lambda ts: parse.CDATA(**ts))

declaration = (L("<!") + SkipTo(">").setResultsName("content") + L(">")).setParseAction(
    lambda ts: parse.Declaration(**ts)
)

processing_instruction = (
    L("<?")
    + Word(alphanums).setResultsName("target")
    + (White() + SkipTo("?>")).setResultsName("content").setParseAction("".join)
    + L("?>")
).setParseAction(lambda ts: parse.PI(**ts))

html = ZeroOrMore(
    text
    | implicit_cdata
    | open_tag
    | close_tag
    | open_close_tag
    | entity
    | comment
    | cdata
    | declaration
    | processing_instruction
)
html_template_parser = html()
html_template_parser.leaveWhitespace()
html_template_parser.parseWithTabs()
html_template_parser.enablePackrat()
