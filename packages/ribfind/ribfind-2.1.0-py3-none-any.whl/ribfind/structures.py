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
class RNAObject:
    """Builder of master RNA objects, mostly a container for a
    'chains' list containing ChainObjects.

    """

    def __init__(self):
        self.chains = []


class ChainObject:
    """Builder of chain objects, containing:

    chain_id: Integer (counting from 1 upwards, as per RNAML
      standards) identifying the chain.

    length: Integer defining the chain's length.

    struct_list: List of StructObjects defining the SSEs present in
      the chain.
    """

    def __init__(self, chain_id, length, numbering_map):
        self.chain_id = chain_id
        self.length = length
        self.struct_list = []
        self.numbering_map = numbering_map


class StructObject:
    """Builder of SSE objects, with parameters: title: String naming
    the object, primarily for display purposes, shared between the two
    objects that form a helix.  is_helix: Boolean identifying the
    object's nature, TRUE for helix, FALSE for loop.  start_pos:
    Integer identifying the first nucleotide (5'-3' direction) of the
    structure.  end_pos: Integer identifying the last nucleotide
    (5'-3' direction) of the structure.

    """

    def __init__(self, title, is_helix, start_pos, end_pos):
        self.title = title
        self.is_helix = is_helix
        self.start_pos = start_pos
        self.end_pos = end_pos
