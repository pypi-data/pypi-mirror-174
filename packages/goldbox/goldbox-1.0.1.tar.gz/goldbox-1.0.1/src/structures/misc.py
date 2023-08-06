# goldbox - A package of simple Python utilities and data structures.
# Copyright (C) 2022 Xavier Mercerweiss
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# The author may be contacted for inquiry at: <xavifmw@gmail.com>

import trees
import copy


### RangeDict ###

class RangeDict:
    ADD_INPUT_ERROR = TypeError("RangeDict addition operand must be of type 'Tuple.'")

    def __init__(self, round_up_keys=True):
        self.dictionary = {None: None}
        self.keys = trees.BinarySearchTree()
        self.round_up = round_up_keys

    def add(self, key, value):
        self.dictionary[key] = value
        self.keys.push(key)

    def remove(self, key):
        self.dictionary.pop(key)
        self.keys.pull(key)

    def get(self, key):
        if key in self.keys:
            true_key = key
        else:
            true_key = self.keys.get_nearest_value(key, self.round_up)

        return self.dictionary[true_key]

    def copy(self):
        return copy.deepcopy(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.dictionary == other.dictionary
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iadd__(self, other):
        if isinstance(other, tuple) and len(other) >= 2:
            self.add(other[0], other[1])
            return self
        else:
            raise self.ADD_INPUT_ERROR

    def __add__(self, other):
        c = self.copy()
        c += other
        return c

    def __radd__(self, other):
        return self.__add__(other)

    def __repr__(self):
        output = "RangeDict{"
        for key, value in self.dictionary.items():
            if key is not None:
                output += f"{key}: {value}, "
        output += "}"

        return output
