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
from pyparsing import ParseException
from ipparse.ipv6 import IPv6_WholeString

good = [(0, '::127.0.0.1', 2130706433),
        (1, '::1', 1),
        (2, '2001:0db8:85a3:0000:0000:8a2e:0370:7334', 42540766452641154071740215577757643572),
        (3, '2001:db8:85a3:0:0:8a2e:370:7334', 42540766452641154071740215577757643572),
        (4, '2001:db8:85a3::8a2e:370:7334', 42540766452641154071740215577757643572),
        (5, '2001:0db8:0000:0000:0000:0000:1428:57ab', 42540766411282592856903984951992014763),
        (6, '2001:0db8:0000:0000:0000::1428:57ab', 42540766411282592856903984951992014763),
        (7, '2001:0db8:0:0:0:0:1428:57ab', 42540766411282592856903984951992014763),
        (8, '2001:0db8:0:0::1428:57ab', 42540766411282592856903984951992014763),
        (9, '2001:0db8::1428:57ab', 42540766411282592856903984951992014763),
        (10, '2001:db8::1428:57ab', 42540766411282592856903984951992014763),
        (11, '::ffff:12.34.56.78', 281470885312590),
        (12, '::ffff:0c22:384e', 281470885312590),
        (13, '2001:0db8:1234:ffff:ffff:ffff:ffff:ffff', 42540766416917396102127771534959312895),
        (14, '2001:0db8:1234:0000:0000:0000:0000:0000', 42540766416916187176308156905784606720),
        (15, '2001:db8:a::123', 42540766411294682115100131243400888611),
        (16, 'fc00::', 334965454937798799971759379190646833152),
        (17, '::ffff:0:0', 281470681743360),
        (18, '2001::', 42540488161975842760550356425300246528),
        (19, '2001:10::', 42540489429626442988779757922003451904),
        (20, '2001:db8::', 42540766411282592856903984951653826560),
        (21, '2001:0000:1234:0000:0000:C1C0:ABCD:0876', 42540488167609437079954741412691249270),
        (22, '3ffe:0b00:0000:0000:0001:0000:0000:000a', 85060430243023186378961535760024469514),
        (23, 'FF02:0000:0000:0000:0000:0000:0000:0001', 338963523518870617245727861364146307073),
        (24, '0000:0000:0000:0000:0000:0000:0000:0001', 1),
        (25, '0000:0000:0000:0000:0000:0000:0000:0000', 0),
        (26, '::ffff:192.168.1.26', 281473913979162),
        (27, '2::10', 10384593717069655257060992658440208),
        (28, 'ff02::1', 338963523518870617245727861364146307073),
        (29, 'fe80::', 338288524927261089654018896841347694592),
        (30, '2002::', 42545680458834377588178886921629466624),
        (31, '2001:db8::', 42540766411282592856903984951653826560),
        (32, '2001:0db8:1234::', 42540766416916187176308156905784606720),
        (33, '::ffff:0:0', 281470681743360),
        (34, '::1', 1),
        (35, '::ffff:192.168.1.1', 281473913979137),
        (36, '1:2:3:4:5:6:7:8', 5192455318486707404433266433261576),
        (37, '1:2:3:4:5:6::8', 5192455318486707404433266432802824),
        (38, '1:2:3:4:5::8', 5192455318486707404433240662999048),
        (39, '1:2:3:4::8', 5192455318486707403025865779445768),
        (40, '1:2:3::8', 5192455318486633616049570941239304),
        (41, '1:2::8', 5192455314859856157205683417120776),
        (42, '1::8', 5192296858534827628530496329220104),
        (43, '1::2:3:4:5:6:7', 5192296860952734609117897189359623),
        (44, '1::2:3:4:5:6', 5192296858534864522863085858652166),
        (45, '1::2:3:4:5', 5192296858534827629093459167805445),
        (46, '1::2:3:4', 5192296858534827628530504919351300),
        (47, '1::2:3', 5192296858534827628530496329351171),
        (48, '1::8', 5192296858534827628530496329220104),
        (49, '::2:3:4:5:6:7:8', 158459951879775902770104041480),
        (50, '::2:3:4:5:6:7', 2417906980587400860139527),
        (51, '::2:3:4:5:6', 36894332589529432070),
        (52, '::2:3:4:5', 562962838585349),
        (53, '::2:3:4', 8590131204),
        (54, '::2:3', 131075),
        (55, '::8', 8),
        (56, '1:2:3:4:5:6::', 5192455318486707404433266432802816),
        (57, '1:2:3:4:5::', 5192455318486707404433240662999040),
        (58, '1:2:3:4::', 5192455318486707403025865779445760),
        (59, '1:2:3::', 5192455318486633616049570941239296),
        (60, '1:2::', 5192455314859856157205683417120768),
        (61, '1::', 5192296858534827628530496329220096),
        (62, '1:2:3:4:5::7:8', 5192455318486707404433240663457800),
        (63, '2001:0000:1234:0000:0000:C1C0:ABCD:0876', 42540488167609437079954741412691249270),
        (64, '1:2:3:4::7:8', 5192455318486707403025865779904520),
        (65, '1:2:3::7:8', 5192455318486633616049570941698056),
        (66, '1:2::7:8', 5192455314859856157205683417579528),
        (67, '1::7:8', 5192296858534827628530496329678856),
        (68, '1:2:3:4:5:6:1.2.3.4', 5192455318486707404433266449711876),
        (69, '1:2:3:4:5::1.2.3.4', 5192455318486707404433240679908100),
        (70, '1:2:3:4::1.2.3.4', 5192455318486707403025865796354820),
        (71, '1:2:3::1.2.3.4', 5192455318486633616049570958148356),
        (72, '1:2::1.2.3.4', 5192455314859856157205683434029828),
        (73, '1::1.2.3.4', 5192296858534827628530496346129156),
        (74, '1:2:3:4::5:1.2.3.4', 5192455318486707403025887271191300),
        (75, '1:2:3::5:1.2.3.4', 5192455318486633616049592432984836),
        (76, '1:2::5:1.2.3.4', 5192455314859856157205704908866308),
        (77, '1::5:1.2.3.4', 5192296858534827628530517820965636),
        (78, '1::5:11.22.33.44', 5192296858534827628530517990056236),
        (79, 'fe80::217:f2ff:254.7.237.98', 338288524927261089654169753135180410210),
        (80, 'fe80::217:f2ff:fe07:ed62', 338288524927261089654169753135180410210),
        (81, '2001:DB8:0:0:8:800:200C:417A', 42540766411282592856906245548098208122),
        (82, 'FF01:0:0:0:0:0:0:101', 338958331222012082418099330867817087233),
        (83, '0:0:0:0:0:0:0:1', 1),
        (84, '0:0:0:0:0:0:0:0', 0),
        (85, '2001:DB8::8:800:200C:417A', 42540766411282592856906245548098208122),
        (86, 'FF01::101', 338958331222012082418099330867817087233),
        (87, '::1', 1),
        (88, '0:0:0:0:0:0:13.1.68.3', 218186755),
        (89, '0:0:0:0:0:FFFF:129.144.52.38', 281472855454758),
        (90, '::13.1.68.3', 218186755),
        (91, '::FFFF:129.144.52.38', 281472855454758),
        (92, 'fe80:0000:0000:0000:0204:61ff:fe9d:f156', 338288524927261089654164245681446711638),
        (93, 'fe80:0:0:0:204:61ff:fe9d:f156', 338288524927261089654164245681446711638),
        (94, 'fe80::204:61ff:fe9d:f156', 338288524927261089654164245681446711638),
        (95, 'fe80:0:0:0:204:61ff:254.157.241.86', 338288524927261089654164245681446711638),
        (96, 'fe80::204:61ff:254.157.241.86', 338288524927261089654164245681446711638),
        (97, 'fe80::', 338288524927261089654018896841347694592),
        (98, 'fe80::1', 338288524927261089654018896841347694593),
        (99, '0000:0000:0000:0000:0000:0000:0000:0001', 1),
        (100, '::ffff:192.0.2.128', 281473902969472),
        (101, '::ffff:c000:280', 281473902969472)]
"""
A list of "good" test cases - valid IPv6 addresses and the corresponding 128-bit integer.
"""

bad = [(0, '127.0.0.1'),
       (1, '::'),
       (2, ':'),
       (3, '2001:0000:1234:0000:0000:C1C0:ABCD:0876 0'),
       (4, '2001:0000:1234: 0000:0000:C1C0:ABCD:0876'),
       (5, '02001:0000:1234:0000:0000:C1C0:ABCD:0876'),
       (6, '2001:0000:1234:0000:00001:C1C0:ABCD:0876'),
       (7, '3ffe:0b00:0000:0001:0000:0000:000a'),
       (8, 'FF02:0000:0000:0000:0000:0000:0000:0000:0001'),
       (9, '3ffe:b00::1::a'),
       (10, '::1111:2222:3333:4444:5555:6666::'),
       (11, '1:2:3::4:5::7:8'),
       (12, '12345::6:7:8'),
       (13, '1::5:400.2.3.4'),
       (14, '1::5:260.2.3.4'),
       (15, '1::5:256.2.3.4'),
       (16, '1::5:1.256.3.4'),
       (17, '1::5:1.2.256.4'),
       (18, '1::5:1.2.3.256'),
       (19, '1::5:300.2.3.4'),
       (20, '1::5:1.300.3.4'),
       (21, '1::5:1.2.300.4'),
       (22, '1::5:1.2.3.300'),
       (23, '1::5:900.2.3.4'),
       (24, '1::5:1.900.3.4'),
       (25, '1::5:1.2.900.4'),
       (26, '1::5:1.2.3.900'),
       (27, '1::5:300.300.300.300'),
       (28, '1::5:3000.30.30.30'),
       (29, '1::400.2.3.4'),
       (30, '1::260.2.3.4'),
       (31, '1::256.2.3.4'),
       (32, '1::1.256.3.4'),
       (33, '1::1.2.256.4'),
       (34, '1::1.2.3.256'),
       (35, '1::300.2.3.4'),
       (36, '1::1.300.3.4'),
       (37, '1::1.2.300.4'),
       (38, '1::1.2.3.300'),
       (39, '1::900.2.3.4'),
       (40, '1::1.900.3.4'),
       (41, '1::1.2.900.4'),
       (42, '1::1.2.3.900'),
       (43, '1::300.300.300.300'),
       (44, '1::3000.30.30.30'),
       (45, '::400.2.3.4'),
       (46, '::260.2.3.4'),
       (47, '::256.2.3.4'),
       (48, '::1.256.3.4'),
       (49, '::1.2.256.4'),
       (50, '::1.2.3.256'),
       (51, '::300.2.3.4'),
       (52, '::1.300.3.4'),
       (53, '::1.2.300.4'),
       (54, '::1.2.3.300'),
       (55, '::900.2.3.4'),
       (56, '::1.900.3.4'),
       (57, '::1.2.900.4'),
       (58, '::1.2.3.900'),
       (59, '::300.300.300.300'),
       (60, '::3000.30.30.30'),
       (61, '2001:DB8:0:0:8:800:200C:417A:221FF01::101::2'),
       (62, '1111:2222:3333:4444::5555:'),
       (63, '1111:2222:3333::5555:'),
       (64, '1111:2222::5555:'),
       (65, '1111::5555:'),
       (66, '::5555:'),
       (67, ':::'),
       (68, '1111:'),
       (69, ':'),
       (70, ':1111:2222:3333:4444::5555'),
       (71, ':1111:2222:3333::5555'),
       (72, ':1111:2222::5555'),
       (73, ':1111::5555'),
       (74, ':::5555'),
       (75, ':::'),
       (76, '1.2.3.4:1111:2222:3333:4444::5555'),
       (77, '1.2.3.4:1111:2222:3333::5555'),
       (78, '1.2.3.4:1111:2222::5555'),
       (79, '1.2.3.4:1111::5555'),
       (80, '1.2.3.4::5555'),
       (81, '1.2.3.4::'),
       (82, '123'),
       (83, 'ldkfj'),
       (84, '2001::FFD3::57ab'),
       (85, '2001:db8:85a3::8a2e:37023:7334'),
       (86, '2001:db8:85a3::8a2e:370k:7334'),
       (87, '1:2:3:4:5:6:7:8:9'),
       (88, '1::2::3'),
       (89, '1:::3:4:5'),
       (90, '1:2:3::4:5:6:7:8:9'),
       (91, '::ffff:2.3.4'),
       (92, '::ffff:257.1.2.3'),
       (93, '1.2.3.4')]
"""
A list of "bad" test cases - invalid IPv6 addresses.
"""

class TestIPv6(unittest.TestCase):
    pass

def create_good_test_case(address, expected):
    def test_case(self, address = address, expected = expected):
        result = IPv6_WholeString.parseString(address)
        self.assertEquals(result[0],
                          expected,
                          '{} does not convert to {} but instead we get {}'.format(address,
                                                                                   expected,
                                                                                   result[0]))
    return test_case

for counter, address, expected in good:
    setattr(TestIPv6,
            'test_good_{}'.format(counter),
            create_good_test_case(address, expected))

def create_bad_test_case(address):
    def test_case(self, address = address):
        self.assertRaises(ParseException, IPv6_WholeString.parseString, address)
    return test_case

for counter, address in bad:
    setattr(TestIPv6,
            'test_bad_{}'.format(counter),
            create_bad_test_case(address))
