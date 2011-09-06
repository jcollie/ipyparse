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

from distutils.core import setup

setup(name = 'ipyparse',
      version = '0.1',

      author = 'Jeffrey C. Ollie',
      author_email = 'jeff@ocjtech.us',
      url = 'https://github.com/jcollie/ipyparse',
      license = 'LGPLv3+',

      classifiers = ['License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                     'Development Status :: 3 - Alpha',
                     'Intended Audience :: Developers',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2.7',
                     'Topic :: Software Development :: Libraries :: Python Modules'],

      packages = ['ipyparse', 'ipyparse.test'],
      package_dir = {'': 'src'},
      requires = ['pyparsing'] )
