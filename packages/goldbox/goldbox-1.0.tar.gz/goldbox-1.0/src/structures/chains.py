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

import copy


class Node:

    def __init__(self, value, parent=None, child=None):
        self.value = value
        self.parent = parent
        self.child = child

    def display_value(self):
        return f'"{self.value}"' if isinstance(self.value, str) else str(self.value)

    def __repr__(self):
        return f"Node({self.display_value()})"


class _Chain:

    SEPARATOR = " > "
    PREFIX = ""
    SUFFIX = ""

    MISSING_IADD = Exception("Addition may not be performed on this object.")
    MISSING_ISUB = Exception("Subtraction may not be performed on this object.")

    def __init__(self, iterable=None, reverse=False):

        if iterable:
            self.length = len(iterable)
            current = None

            for i, value in enumerate(reversed(iterable) if reverse else iterable):
                node = Node(value, parent=current)

                if current:
                    current.child = node
                else:
                    self.head = node

                current = node
            self.tail = current

        else:
            self.length = 0
            self.head = None
            self.tail = None

    def copy(self):
        return copy.deepcopy(self)

    def reverse(self):

        current = self.tail
        while current:

            if current == self.tail:
                self.head = current

            temp = current.child
            current.child = current.parent
            current.parent = temp

            if not current.child:
                self.tail = current

            current = current.child

    def display_ends(self):
        print(
            f"{self.head.parent if self.head else None} -> {self.head}",
            "-> ... -> "
            f"{self.tail} -> {self.tail.child if self.tail else None}",
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        if hasattr(self.__class__, "__iadd__"):
            output = self.copy()
            output += other
        else:
            raise self.MISSING_IADD
        return output

    def __sub__(self, other):
        if hasattr(self.__class__, "__isub__"):
            output = self.copy()
            output -= other
        else:
            raise self.MISSING_ISUB
        return output

    def __repr__(self, separator=None, prefix=None, suffix=None):
        sep = self.SEPARATOR if separator is None else separator
        pre = self.PREFIX if prefix is None else prefix
        suf = self.SUFFIX if suffix is None else suffix

        if self.head:
            output = pre

            current = self.head
            while current:
                output += f"{current.display_value()}{sep if current != self.tail else ''}"
                current = current.child

            output += suf
            return output

        else:
            return f"{pre}{sep}{suf}"

    def __len__(self):
        return self.length

    def __reversed__(self):
        c = self.copy()
        c.reverse()
        return c


class LinkedList(_Chain):

    MISSING_VALUE_ERROR = ValueError("Value not contained within linked list.")
    MISSING_INDEX_ERROR = IndexError("Value at index does not exist within linked list.")

    def __init__(self, iterable=None, reverse=False):
        super().__init__(iterable, reverse)
        self._iteration = self.head

    def append(self, value):
        node = Node(value, parent=self.tail)

        if self.tail:
            self.tail.child = node
        else:
            self.head = node

        self.tail = node
        self.length += 1

    def prepend(self, value):
        node = Node(value, child=self.head)

        if self.head:
            self.head.parent = node
        else:
            self.tail = node

        self.head = node
        self.length += 1

    def insert(self, value, index):
        old = self.index(index)
        new = Node(value, child=old)

        if old == self.head:
            self.head = new

        else:
            old.parent.child = new
            new.parent = old.parent

        old.parent = new
        self.length += 1

    def extend(self, iterable, reverse=False, prepend=False):

        if prepend:
            reverse = not reverse  # Prepending each element will naturally reverse the order of the inserted list,
            # requiring a subsequent reversal.
            executed = self.prepend
        else:
            executed = self.append

        if reverse:
            index = len(iterable) - 1
            while index >= 0:
                executed(iterable[index])
                index -= 1

        else:
            for value in iterable:
                executed(value)

    def remove(self, value):
        node = self.search(value)
        self._remove_node(node)

    def remove_all(self, value):
        for node in self:
            if node.value == value:
                self._remove_node(node)

    def pop(self, index=0):
        node = self.index(index)
        self._remove_node(node)

    def search(self, value):

        for node in self:
            if node.value == value:
                return node

        raise self.MISSING_VALUE_ERROR

    def index(self, index):
        count = 0

        for node in self:
            if count == index:
                return node
            count += 1

        raise self.MISSING_INDEX_ERROR

    def values(self):
        for node in self:
            yield node.value

    def _remove_node(self, node):

        if not self.head or not self.tail:
            return

        if node == self.head and node == self.tail:
            self.head = None
            self.tail = None

        elif node == self.head:
            self.head = node.child
            self.head.parent = None

        elif node == self.tail:
            self.tail = node.parent
            self.tail.child = None

        else:
            node.parent.child = node.child
            node.child.parent = node.parent

        self.length -= 1

    def __eq__(self, other):

        if isinstance(other, self.__class__) and len(self) == len(other):
            for local, foreign in zip(self, other):
                if local.value != foreign.value:
                    return False
            return True

        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iadd__(self, other):
        try:
            self.extend(other)
        except TypeError:
            self.append(other)

        return self

    def __isub__(self, other):

        try:
            for item in other:
                self.remove_all(item)
        except TypeError:
            self.remove_all(other)

        return self

    def __contains__(self, item):
        for value in self.values():
            if value == item:
                return True
        return False

    def __iter__(self):
        self._iteration = self.head
        return self

    def __next__(self):

        if not self._iteration:
            self._iteration = self.head
            raise StopIteration()

        iteration_value = self._iteration
        self._iteration = self._iteration.child
        return iteration_value


class Stack(_Chain):

    PREFIX = "| "

    def __init__(self, iterable=None, reverse=False):
        super().__init__(iterable, reverse)

    def push(self, value):
        node = Node(value, parent=self.tail)

        if self.tail:
            self.tail.child = node
        else:
            self.head = node

        self.tail = node
        self.length += 1

    def pull(self):

        if self.tail:
            value = self.tail.value
            self.tail = self.tail.parent

            if self.tail:
                self.tail.child = None
            else:
                self.head = None

            self.length -= 1
            return value

        else:
            return

    def extend(self, iterable, reverse=False):

        if reverse:
            index = len(iterable) - 1
            while index >= 0:
                self.push(iterable[index])
                index -= 1

        else:
            for value in iterable:
                self.push(value)

    def __iadd__(self, other):
        self.push(other)
        return self

    def __repr__(self, separator=None, prefix=None, suffix=None):
        sep = self.SEPARATOR if separator is None else separator
        pre = self.PREFIX if prefix is None else prefix
        suf = self.SUFFIX if suffix is None else suffix
        return super().__repr__(sep, pre, suf)

    def __iter__(self):
        return self

    def __next__(self):

        if not self.tail:
            raise StopIteration()

        return self.pull()


class Queue(_Chain):

    PREFIX = "> "
    SUFFIX = " >"

    def __init__(self, iterable=None, reverse=False):
        super().__init__(iterable, reverse)

    def push(self, value):
        node = Node(value, child=self.head)

        if self.head:
            self.head.parent = node
        else:
            self.tail = node

        self.head = node
        self.length += 1

    def pull(self):

        if self.tail:
            value = self.tail.value
            self.tail = self.tail.parent

            if self.tail:
                self.tail.child = None
            else:
                self.head = None

            self.length -= 1
            return value

        else:
            return

    def extend(self, iterable, reverse=False):

        if reverse:
            index = len(iterable) - 1
            while index >= 0:
                self.push(iterable[index])
                index -= 1

        else:
            for value in iterable:
                self.push(value)

    def __iadd__(self, other):
        self.push(other)
        return self

    def __repr__(self, separator=None, prefix=None, suffix=None):
        sep = self.SEPARATOR if separator is None else separator
        pre = self.PREFIX if prefix is None else prefix
        suf = self.SUFFIX if suffix is None else suffix
        return super().__repr__(sep, pre, suf)

    def __iter__(self):
        return self

    def __next__(self):

        if not self.tail:
            raise StopIteration()

        return self.pull()


class Deque(Queue):

    SEPARATOR = " | "
    PREFIX = "< "
    SUFFIX = " >"

    def __init__(self, iterable=None, reverse=False):
        super().__init__(iterable, reverse)

    def push(self, value, to_back=True):
        push = self._push_back if to_back else self._push_front
        push(value)

    def _push_back(self, value):
        super().push(value)

    def _push_front(self, value):
        node = Node(value, parent=self.tail)

        if self.tail:
            self.tail.child = node
        else:
            self.head = node

        self.tail = node
        self.length += 1

    def pull(self, from_front=True):
        pull = self._pull_front if from_front else self._pull_back
        pull()

    def _pull_back(self):
        if self.head:
            value = self.head.value
            self.head = self.head.child

            if self.head:
                self.head.parent = None
            else:
                self.tail = None

            self.length -= 1
            return value

        else:
            return

    def _pull_front(self):
        return super().pull()	

    def extend(self, iterable, reverse=False, prepend=True):
        reverse = not reverse if prepend else reverse

        if reverse:
            index = len(iterable) - 1
            while index >= 0:
                self.push(iterable[index], prepend)
                index -= 1

        else:
            for value in iterable:
                self.push(value, prepend)

    def __iadd__(self, other):
        self.push(other)
        return self

    def __repr__(self, separator=None, prefix=None, suffix=None):
        sep = self.SEPARATOR if separator is None else separator
        pre = self.PREFIX if prefix is None else prefix
        suf = self.SUFFIX if suffix is None else suffix
        return super().__repr__(sep, pre, suf)
