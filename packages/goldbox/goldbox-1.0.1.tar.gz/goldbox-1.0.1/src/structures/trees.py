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

import chains
import copy
import math


class BinaryNode:

    def __init__(self, value, left=None, right=None, parent=None):
        self.value = value
        self.left, self.right = left, right
        self.parent = parent
        self.children = (0 if left is None else 1) + (0 if right is None else 1)

    def set_child(self, value, is_left=True):
        node = BinaryNode(value, parent=self)
        if is_left:
            self.children += 1 if self.left is None else 0
            self.left = node
        else:
            self.children += 1 if self.right is None else 0
            self.right = node

    def get_child(self, is_left=True):
        return self.left if is_left else self.right

    def pop_child(self, node):
        if node is not None:
            if node is self.left:
                self.left = None
                self.children -= 1
            elif node is self.right:
                self.right = None
                self.children -= 1

    def reverse_children(self):
        temp = self.left
        self.left = self.right
        self.right = temp

    def get_display_value(self):
        return f'"{self.value}"' if isinstance(self.value, str) else str(self.value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.value == self.value
        return False

    def __repr__(self):
        return f"BinaryNode({self.get_display_value()})"


class _Tree:

    SEPARATOR = ", "
    PREFIX = "Tree("
    SUFFIX = ")"

    MISSING_IADD = Exception("Addition may not be performed on this object.")
    MISSING_ISUB = Exception("Subtraction may not be performed on this object.")

    def __init__(self):
        self.root = None
        self.size = 0
        self._nodes = []
        self._iteration = 0

    def values(self):
        for node in self:
            yield node.value

    def copy(self):
        return copy.deepcopy(self)

    def _pre(self, node, func, args, get_value):
        if node is None:
            return
        func(node.value if get_value else node, *args)
        self._pre(node.left, func, args, get_value)
        self._pre(node.right, func, args, get_value)

    def _in(self, node, func, args, get_value):
        if node is None:
            return
        self._in(node.left, func, args, get_value)
        func(node.value if get_value else node, *args)
        self._in(node.right, func, args, get_value)

    def _post(self, node, func, args, get_value):
        if node is None:
            return
        self._post(node.left, func, args, get_value)
        self._post(node.right, func, args, get_value)
        func(node.value if get_value else node, *args)

    def _level(self, func, args=(), get_value=True):
        queue = chains.Queue()
        if self.root:
            queue.push(self.root)

        while queue.head is not None:
            node = queue.pull()
            if node.left is not None:
                queue.push(node.left)
            if node.right is not None:
                queue.push(node.right)
            func(node.value if get_value else node, *args)

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

    def __radd__(self, other):
        return self.__add__(other)

    def __repr__(self, separator=None, prefix=None, suffix=None):
        sep = self.SEPARATOR if separator is None else separator
        suf = self.SUFFIX if suffix is None else suffix
        output = self.PREFIX if prefix is None else prefix

        remaining = self.size
        for node in self:
            output += node.get_display_value()
            remaining -= 1
            output += "" if remaining == 0 else sep

        output += suf
        return output

    def __len__(self):
        return self.size

    def __iter__(self):
        nodes = []
        self._level(nodes.append, get_value=False)
        self._nodes = nodes
        self._iteration = 0
        return self

    def __next__(self):
        try:
            returned = self._nodes[self._iteration]
            self._iteration += 1
            return returned
        except IndexError:
            raise StopIteration


class BinaryTree(_Tree):

    PREFIX = "BinaryTree("

    INDEX_ERROR = IndexError("Invalid index within binary tree; impossible to reach position.")

    def __init__(self, values=()):
        super().__init__()
        if values:
            for index in range(len(values)):
                self.insert(values[index], index)

    def insert(self, value, index):
        if self.root is None:
            self.root = BinaryNode(value)
            self.size += 1
        elif index == 0:
            self.root.value = value
        else:
            parent = self.index((index - 1) // 2)
            is_left = bool(index % 2)
            child = parent.get_child(is_left)
            if child:
                child.value = value
            else:
                parent.set_child(value, is_left=is_left)
                self.size += 1

    def pop(self, index):
        removed = self.index(index)
        if removed is self.root:
            del self.root
            self.root = None
        else:
            removed.parent.pop_child(removed)
        self.size -= 1

    def index(self, index):
        try:
            node = self._get_node_at_index(index)
        except AttributeError:
            raise self.INDEX_ERROR
        else:
            if node is None:
                raise self.INDEX_ERROR
            return node

    def values(self):
        for node in self:
            yield node.value

    def pre_order(self, func, args=(), get_value=True):
        self._pre(self.root, func, args, get_value)

    def in_order(self, func, args=(), get_value=True):
        self._in(self.root, func, args, get_value)

    def post_order(self, func, args=(), get_value=True):
        self._post(self.root, func, args, get_value)

    def level_order(self, func, args=(), get_value=True):
        self._level(func, args, get_value)

    def invert(self):
        self._level(BinaryNode.reverse_children, get_value=False)

    def _get_node_at_index(self, index):
        current = self.root
        if index > 0:
            n = index + 1
            power = 2 ** math.floor(math.log(n, 2))
            base = power // 2
            total = n - power
            while base > 0:
                quotient = total // base
                current = current.right if quotient else current.left
                total -= quotient * base
                base //= 2
        return current

    def __repr__(self, separator=None, prefix=None, suffix=None):
        sep = self.SEPARATOR if separator is None else separator
        pre = self.PREFIX if prefix is None else prefix
        suf = self.SUFFIX if suffix is None else suffix
        return super().__repr__(sep, pre, suf)

    def __contains__(self, item):
        for value in self.values():
            if value == item:
                return True
        return False

    def __reversed__(self):
        c = self.copy()
        c.invert()
        return c


class BinarySearchTree(_Tree):

    PREFIX = "BinarySearchTree("

    def __init__(self, values=(), reverse=False):
        super().__init__()
        self._maximum = None
        self._minimum = None
        self._values = set()
        if values:
            self.extend(values, reverse)

    def extend(self, values, reverse=False):
        step = -1 if reverse else 1
        for value in values[::step]:
            self.push(value)

    def push(self, value):
        if value not in self._values:
            parent = self._get_parent_of_value(value)
            if parent:
                is_left = value < parent.value
                parent.set_child(value, is_left=is_left)
                node = parent.get_child(is_left)
            else:
                self.root = BinaryNode(value)
                node = self.root
            self._update_max_and_min(node)
            self._values.add(value)
            self.size += 1

    def reduce(self, values):
        for value in values:
            self.pull(value)

    def pull(self, value):
        if value in self._values:
            node = self._get_node_of_value(value)
            self._delete_node(node)
            self.size -= 1
            self._values.remove(value)
            return value

    def traverse(self, func, args=(), get_value=True):
        self._in(self.root, func, args, get_value)

    def get_nearest_value(self, value, round_up=True):
        if value in self._values:
            return value
        current = self._get_parent_of_value(value)
        if round_up:
            while current.value < value and current is not self._maximum:
                current = self._get_next_highest_node(current)
        else:
            while current.value > value and current is not self._minimum:
                current = self._get_next_lowest_node(current)
        return current.value

    def get_maximum_value(self):
        return self._maximum.value

    def get_minimum_value(self):
        return self._minimum.value

    def _get_parent_of_value(self, value):
        parent = None
        current = self.root
        while current:
            parent = current
            current = parent.right if value > parent.value else parent.left
        return parent

    def _update_max_and_min(self, node):
        if self._maximum is None or node.value > self._maximum.value:
            self._maximum = node
        if self._minimum is None or node.value < self._minimum.value:
            self._minimum = node

    def _get_node_of_value(self, value):
        current = self.root
        while current and current.value != value:
            current = current.left if value < current.value else current.right
        return current

    def _delete_node(self, node):
        parent = node.parent

        self._pass_max_and_min(node)
        if parent is None:
            self._delete_root()
        elif node.children == 0:
            self._delete_leaf_node(node, parent)
        elif node.children == 1:
            self._delete_one_child_node(node, parent)
        else:
            self._delete_two_child_node(node)

    def _pass_max_and_min(self, node):
        if node is self._maximum:
            self._maximum = self._get_next_lowest_node(self._maximum)
        elif node is self._minimum:
            self._minimum = self._get_next_highest_node(self._minimum)

    def _delete_root(self):
        root = self.root

        if root.children == 0:
            self.root = None
        elif root.children == 1:
            child = root.right if root.left is None else root.left
            child.parent = None
            self.root = child
        else:
            replacement = self._get_next_highest_node(root)
            self.root.value = replacement.value
            self._delete_node(replacement)

    @staticmethod
    def _delete_leaf_node(node, parent):
        parent.pop_child(node)

    @staticmethod
    def _delete_one_child_node(node, parent):
        child = node.right if node.left is None else node.left
        child.parent = parent
        if node is parent.left:
            parent.left = child
        else:
            parent.right = child

    def _delete_two_child_node(self, node):
        replacement = self._get_next_highest_node(node) if node.value <= self.root.value \
            else self._get_next_lowest_node(node)
        node.value = replacement.value
        self._delete_node(replacement)

    def _get_next_highest_node(self, node):
        child = None
        while node.right is child or node.right is None:
            parent = node.parent
            if parent is None or node is self._maximum:
                return node
            elif node is parent.left:
                return parent
            else:
                child = node
                node = parent

        else:
            current = node.right
            while current.left:
                current = current.left
            return current

    def _get_next_lowest_node(self, node):
        child = None
        while node.left is child or node.left is None:
            parent = node.parent
            if parent is None or node is self._minimum:
                return node
            elif node is parent.right:
                return parent
            else:
                child = node
                node = parent

        else:
            current = node.left
            while current.right:
                current = current.right
            return current

    def __iadd__(self, other):
        try:
            self.extend(other)
        except TypeError:
            self.push(other)

        return self

    def __isub__(self, other):
        try:
            self.reduce(other)
        except TypeError:
            self.pull(other)

        return self

    def __repr__(self, separator=None, prefix=None, suffix=None):
        sep = self.SEPARATOR if separator is None else separator
        pre = self.PREFIX if prefix is None else prefix
        suf = self.SUFFIX if suffix is None else suffix
        return super().__repr__(sep, pre, suf)

    def __contains__(self, item):
        return item in self._values

    def __iter__(self):
        nodes = []
        self.traverse(nodes.append, get_value=False)
        self._nodes = nodes
        self._iteration = 0
        return self


class _Heap:

    SEPARATOR = ", "
    PREFIX = "Heap("
    SUFFIX = ")"

    INCOMPLETE_METHOD_ERROR = Exception("Incomplete method called; class hierarchy violated.")

    def __init__(self, values=()):
        self.items = []
        self.size = 0
        self.extend(values)
        self._iteration = 0

    def extend(self, values):
        for value in values:
            self.push(value)

    def push(self, value):
        self.items.append(value)
        self._bubble_up(self.size)
        self.size += 1

    def pull(self):
        if self.size > 0:
            self.size -= 1
            old = self.items[0]
            if self.size > 0:
                self.items[0] = self.items[self.size]
                self._bubble_down(0)
            self.items.pop()
            return old

    def copy(self):
        return copy.deepcopy(self)

    def _swap(self, i1, i2):
        temp = self.items[i1]
        self.items[i1] = self.items[i2]
        self.items[i2] = temp

    def _bubble_up(self, index):
        raise self.INCOMPLETE_METHOD_ERROR

    def _bubble_down(self, index):
        current_index = index
        child_index = self._get_child_index(index)
        while child_index:
            self._swap(current_index, child_index)
            current_index = child_index
            child_index = self._get_child_index(current_index)

    def _get_child_index(self, index):
        raise self.INCOMPLETE_METHOD_ERROR

    @staticmethod
    def get_parent_index(index):
        return (index - 1) // 2

    @staticmethod
    def get_left_index(index):
        return (index * 2) + 1

    @staticmethod
    def get_right_index(index):
        return (index * 2) + 2

    @staticmethod
    def _get_item_display_value(item):
        return f'"{item}"' if isinstance(item, str) else str(item)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.items == other.items
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        c = self.copy()
        c += other
        return c

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        try:
            self.extend(other)
        except TypeError:
            self.push(other)
        return self

    def __repr__(self, separator=None, prefix=None, suffix=None):
        sep = self.SEPARATOR if separator is None else separator
        suf = self.SUFFIX if suffix is None else suffix
        output = self.PREFIX if prefix is None else prefix

        remaining = self.size
        for item in self.items:
            output += self._get_item_display_value(item)
            remaining -= 1
            output += "" if remaining == 0 else sep

        output += suf
        return output

    def __contains__(self, item):
        return item in self.items

    def __len__(self):
        return self.size

    def __iter__(self):
        self._iteration = self.size
        return self

    def __next__(self):
        if self._iteration <= 0:
            raise StopIteration()
        self._iteration -= 1
        return self.pull()


class MinHeap(_Heap):

    PREFIX = "MinHeap("

    def _bubble_up(self, index):
        value = self.items[index]
        current_index = index
        parent_index = self.get_parent_index(index)
        while parent_index >= 0 and value < self.items[parent_index]:
            self._swap(current_index, parent_index)
            current_index = parent_index
            parent_index = self.get_parent_index(current_index)

    def _get_child_index(self, index):
        output = None
        value = self.items[index]
        left = self.get_left_index(index)
        right = self.get_right_index(index)
        if left < self.size and self.items[left] < value:
            output = left
            value = self.items[left]
        if right < self.size and self.items[right] < value:
            output = right
        return output

    def __repr__(self, separator=None, prefix=None, suffix=None):
        sep = self.SEPARATOR if separator is None else separator
        pre = self.PREFIX if prefix is None else prefix
        suf = self.SUFFIX if suffix is None else suffix
        return super().__repr__(sep, pre, suf)

    def __reversed__(self):
        return MaxHeap(self.items)


class MaxHeap(_Heap):

    PREFIX = "MaxHeap("

    def _bubble_up(self, index):
        value = self.items[index]
        current_index = index
        parent_index = self.get_parent_index(index)
        while parent_index >= 0 and value > self.items[parent_index]:
            self._swap(current_index, parent_index)
            current_index = parent_index
            parent_index = self.get_parent_index(current_index)

    def _get_child_index(self, index):
        output = None
        value = self.items[index]
        left = self.get_left_index(index)
        right = self.get_right_index(index)
        if left < self.size and self.items[left] > value:
            output = left
            value = self.items[left]
        if right < self.size and self.items[right] > value:
            output = right
        return output

    def __repr__(self, separator=None, prefix=None, suffix=None):
        sep = self.SEPARATOR if separator is None else separator
        pre = self.PREFIX if prefix is None else prefix
        suf = self.SUFFIX if suffix is None else suffix
        return super().__repr__(sep, pre, suf)

    def __reversed__(self):
        return MinHeap(self.items)
