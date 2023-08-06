# This file is part of the RIBFIND (https://gitlab.com/topf-lab/ribfind)
# Copyright (c) 2022 RIBFIND Developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
RIBFIND

A python program for finding rigid bodies.
"""
import importlib.metadata

_DISTRIBUTION_METADATA = importlib.metadata.metadata("ribfind")


__author__ = _DISTRIBUTION_METADATA["Author"]
__project__ = _DISTRIBUTION_METADATA["Name"]
__version__ = _DISTRIBUTION_METADATA["Version"]
__credits__ = ""
