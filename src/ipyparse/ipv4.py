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

from pyparsing import Combine
from pyparsing import Group
from pyparsing import Literal
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import ParserElement
from pyparsing import Word

dwspc = ParserElement.DEFAULT_WHITE_CHARS
ParserElement.setDefaultWhitespaceChars('')

def convert_octet(s, l, t):
    """
    Convert an octet to an 8-bit integer.

    @param s: The original string
    @type s: str
    
    @param loc: The location in the string that the match occurred
    @type loc: int

    @param toks: The tokens that make up octet.
    @type toks: L{pyparsing.ParseResult}

    @return: The octet expressed as a 8-bit integer.
    @rtype: int
    """
    return [ int(t[0]) ]

def convert_ipv4_in_ipv6(s, l, t):
    """
    Convert an IPv4 address to two 16 bit integers

    @param s: The original string
    @type s: str
    
    @param loc: The location in the string that the match occurred
    @type loc: int

    @param toks: The tokens that make up IPv4 address.
    @type toks: L{pyparsing.ParseResult}

    @return: The IPv4 address expressed as two 16 bit integers.
    @rtype: int
    """
    r = [ (t[0][0] << 8) + 
          (t[0][1]),
          (t[0][2] << 8) +
          (t[0][3]) ]
    return r

def convert_ipv4(s, l, t):
    """
    Convert an IPv4 address to a 32-bit integer.

    @param s: The original string
    @type s: str
    
    @param loc: The location in the string that the match occurred
    @type loc: int

    @param toks: The tokens that make up the IPv4 address.
    @type toks: L{pyparsing.ParseResult}

    @return: The IPv4 address expressed as a 32-bit integer.
    @rtype: int
    """
    r = [ (t[0][0] << 24) + 
          (t[0][1] << 16) +
          (t[0][2] << 8) +
          (t[0][3]) ]
    return r

LeadingZeros = Optional(Literal('0')).suppress()

Octet = Combine((OneOrMore(Literal('0'))) ^
                (LeadingZeros + Word('123456789', exact = 1)) ^
                (LeadingZeros + Word('123456789', '0123456789', exact = 2)) ^
                (LeadingZeros + '1' + Word('0123456789', exact = 2)) ^
                (LeadingZeros + '2' + Word('01234', '0123456789', exact = 2)) ^
                (LeadingZeros + '25' + Word('012345', exact = 1))).setParseAction(convert_octet)

Dot = Literal('.').suppress()

_IPv4 = Octet + (Dot + Octet) * 3
IPv4 = Group(_IPv4).setParseAction(convert_ipv4)
IPv4_in_IPv6 = Group(_IPv4).setParseAction(convert_ipv4_in_ipv6)

ParserElement.setDefaultWhitespaceChars(dwspc)
