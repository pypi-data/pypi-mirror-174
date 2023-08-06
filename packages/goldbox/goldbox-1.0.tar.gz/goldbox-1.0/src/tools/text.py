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


def get_lines(filename, collapse_whitespace=True):
    with open(filename, "r") as file:

        if collapse_whitespace:
            return [line.strip() for line in file.readlines() if line != ""]
        else:
            return [line + "\n" for line in file.read().split("\n")]


def replace_text_in_file(filename, old, new):
    lines = get_lines(filename, False)

    with open(filename, "w") as file:
        for line in lines:
            file.write(line.replace(old, new))


def shrink(filename, spaces=4):
    replace_text_in_file(filename, old=(" " * spaces), new="\t")


def grow(filename, spaces=4):
    replace_text_in_file(filename, old="\t", new=(" " * spaces))
