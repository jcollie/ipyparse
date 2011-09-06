# -*- mode: python; coding: utf-8 -*-

# Copyright © 2011
#
# This file is part of IPyParse.
#
# IPyParse is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IPyParse is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with IPyParse.  If not, see <http://www.gnu.org/licenses/>.

from pyparsing import Group
from pyparsing import Literal
from pyparsing import ParserElement
from pyparsing import StringEnd
from pyparsing import StringStart
from pyparsing import Word

from ipparse.ipv4 import IPv4_in_IPv6

dwspc = ParserElement.DEFAULT_WHITE_CHARS
ParserElement.setDefaultWhitespaceChars('')

def convert_short(s, loc, toks):
    """
    Convert part of an IPv6 address to a short integer.

    @param s: The original string
    @type s: str
    
    @param loc: The location in the string that the match occurred
    @type loc: int

    @param toks: The tokens that make up the IPv6 address part.
    @type toks: L{pyparsing.ParseResult}

    @return: The IPv6 address part expressed as a 16-bit integer.
    @rtype: int
    """
    return [ int(toks[0], 16) ]

def convert_ipv6(s, loc, toks):
    """
    Convert tokens that the parser has matched as an IPv6 address to a 128-bit number.

    @param s: The original string
    @type s: str
    
    @param loc: The location in the string that the match occurred
    @type loc: int

    @param toks: The tokens that make up the IPv6 address.  Individual
    parts of the address should already have been converted to
    integers, except for the DoubleColon token which is handled
    specially.
    @type toks: L{pyparsing.ParseResult}

    @return: The IPv6 address expressed as a 128-bit integer.
    @rtype: int
    """
    # convert toks to a read list or we get some wierd exceptions
    toks = toks[:]

    try:
        index = toks.index('::')
        toks = toks[:index] + [0] * (8 - len(toks) + 1) + toks[index+1:]
    except ValueError:
        pass

    if len(toks) != 8:
        raise ValueError('There has to be 8!')

    result = 0
    for tok in toks:
        result = (result << 16) + tok

    return [ result ]

G = Word('0123456789abcdefABCDEF', min = 1, max = 4).setParseAction(convert_short)

Colon = Literal(':').suppress()
DoubleColon = Literal('::')

IPv6 = (((G + Colon) * 7 + G) ^
         ((G + Colon) * 6 + IPv4_in_IPv6) ^
         (G + (Colon + G) * (0, 6) + DoubleColon) ^
         (G + (Colon + G) * (0, 5) + DoubleColon + G) ^
         (G + (Colon + G) * (0, 4) + DoubleColon + IPv4_in_IPv6) ^
         (G + (Colon + G) * (0, 4) + DoubleColon + (G + Colon) + G) ^
         (G + (Colon + G) * (0, 3) + DoubleColon + (G + Colon) + IPv4_in_IPv6) ^
         (G + (Colon + G) * (0, 3) + DoubleColon + (G + Colon) * 2 + G) ^
         (G + (Colon + G) * (0, 2) + DoubleColon + (G + Colon) * 2 + IPv4_in_IPv6) ^
         (G + (Colon + G) * (0, 2) + DoubleColon + (G + Colon) * 3 + G) ^
         (G + (Colon + G) * (0, 1) + DoubleColon + (G + Colon) * 3 + IPv4_in_IPv6) ^
         (G + (Colon + G) * (0, 1) + DoubleColon + (G + Colon) * 4 + G) ^
         (G                        + DoubleColon + (G + Colon) * 5 + G) ^
         (DoubleColon + (G + Colon) * (0, 6) + (G ^ IPv4_in_IPv6))).setParseAction(convert_ipv6)

IPv6_WholeString = StringStart() + IPv6 + StringEnd()

ParserElement.setDefaultWhitespaceChars(dwspc)
