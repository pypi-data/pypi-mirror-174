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
"""Weighted undirected graph data structure

Defines a graph where nodes are model_ids and edges model interaction
strength.

"""


class _Edge:
    def __init__(self, this_model_id, that_model_id):
        self.this = this_model_id
        self.that = that_model_id
        self.interaction_strength = 0


class Graph:
    """A Graph"""

    def __init__(self):
        self.edges = {}

    def add_edge(self, this_model, that_model, interaction_strength):
        """Add and edge to the graph"""
        edge = self.get_edge(this_model.model_id, that_model.model_id)
        edge.interaction_strength = interaction_strength

    def get_edges(self):
        """Returns a list of edges sorted by interaction strength"""
        edges = list(self.edges.values())
        edges.sort(key=lambda x: x.interaction_strength)
        return edges

    def get_weights(self):
        """Returns a sorted list of unique edge weights"""
        weights = list(set(e.interaction_strength for e in self.edges.values()))
        weights.sort()
        return weights

    def get_edge(self, this_model_id, that_model_id):
        """Returns the edge between two contigs."""
        this = min(this_model_id, that_model_id)
        that = max(this_model_id, that_model_id)
        if self.edges.get((this, that)) is None:
            self.edges[(this, that)] = _Edge(this, that)
        return self.edges[(this, that)]
