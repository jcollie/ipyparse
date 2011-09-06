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

import unittest
from ipparse.ipv4 import IPv4
from ipparse.ipv4 import Octet

class TestIPv4(unittest.TestCase):
    def test_octet_1(self):
        result = Octet.parseString('01')
        self.assertEqual(result[0], 1)

    def test_loopback(self):
        result = IPv4.parseString('127.0.0.1')
        self.assertEqual(result[0], 2130706433)

        
