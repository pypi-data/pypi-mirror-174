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
Used for calculating contact distances.
"""

import re
import numpy as np
from ribfind.model import Residue


class CentroidContact:
    """An object for checking contact distance between residues."""

    def __init__(self, dist_cutoff):
        self.id_to_centroid = {}
        self.dist_cutoff = dist_cutoff

    def has_centroid(self, residue):
        return self.id_to_centroid.get(residue) is not None

    def in_contact(self, res_a: Residue, res_b: Residue):
        """Returns true if res_a and res_b are with in the contact distance"""
        try:
            center_a = self.id_to_centroid[res_a]
            center_b = self.id_to_centroid[res_b]
            dist = np.linalg.norm(center_a - center_b)
            if dist < self.dist_cutoff:
                return True
            return False
        except KeyError:
            return False

    def checker(self, residues):
        contact_map = ContactMap(self)
        for residue in residues:
            contact_map.map_residue(residue, residue)
        return contact_map

    def add_residue(self, res, coords):
        """Given a residue and a list of coordinates saves the
        centroid for the residue.
        """
        if len(coords) == 0:
            return
        total = sum(coord for coord in coords)
        self.id_to_centroid[res] = total / float(len(coords))


def make_protein_contacts(structure, dist_cutoff=6.5):
    """Create contact checking object with the following rules.

    - Residues are in contact if their centroids are with in
      'dist_cutoff' of one another.

    - Centroids are calculated as the average position of non-backbone
      atoms in the residue, with the exception of glycine which uses the
      C-alpha atom.
    """
    backbone_atom_names = ["CA", "N", "O", "C"]

    centroids = CentroidContact(
        dist_cutoff,
    )

    for chain in structure[0]:
        for residue in chain:
            _, res_num, _ = residue.get_id()
            if residue.get_resname() == "GLY":
                coords = [
                    np.array(list(a.get_vector()))
                    for a in residue.get_list()
                    if a.get_id() == "CA"
                ]
            else:
                coords = [
                    np.array(list(a.get_vector()))
                    for a in residue.get_list()
                    if a.get_id() not in backbone_atom_names
                ]
            centroids.add_residue(Residue(chain.get_id(), res_num), coords)

    return centroids


def make_rna_contacts(structure, dist_cutoff=7.5):
    """Create contact checking object with the following rules:

    - Residues are in contact if their centroids are with in
      'dist_cutoff' of each over.

    - Centroids are calculated as the average position of atoms in the
      residues, which do not contain `P` or `'` in there element
      names.
    """
    centroids = CentroidContact(dist_cutoff)
    for chain in structure[0]:
        for residue in chain:
            _, res_num, _ = residue.get_id()
            coords = [
                np.array(list(a.get_vector()))
                for a in residue.get_list()
                if not (re.search(r"P", a.get_name()) or re.search(r"'", a.get_name()))
            ]
            centroids.add_residue(Residue(chain.get_id(), res_num), coords)
    return centroids


class ContactMap:
    def __init__(self, contacts):
        self._contacts = contacts
        self.cells = {}
        self.cell_size = self._contacts.dist_cutoff

    def to_cell_id(self, residue):
        center = self._contacts.id_to_centroid.get(residue)
        cell_id = (
            int(center[0] / self.cell_size),
            int(center[1] / self.cell_size),
            int(center[2] / self.cell_size),
        )
        return cell_id

    def to_cell(self, residue):
        cell_id = self.to_cell_id(residue)
        cell = self.cells.get(cell_id)
        if cell is None:
            cell = set()
            self.cells[cell_id] = cell
        return cell

    def map_residue(self, residue, value):
        self.to_cell(residue).add(value)

    def neighbour_ids(self, residue):
        cell_id = self.to_cell_id(residue)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                for k in [-1, 0, 1]:
                    yield (cell_id[0] + i, cell_id[1] + j, cell_id[2] + k)

    def neighbours(self, residue):
        for ncell_id in self.neighbour_ids(residue):
            cell = self.cells.get(ncell_id)
            if cell is not None:
                for nresidue in cell:
                    yield nresidue

    def in_contact(self, residue):
        for other_residue in self.neighbours(residue):
            if self._contacts.in_contact(residue, other_residue):
                return True
        return False
