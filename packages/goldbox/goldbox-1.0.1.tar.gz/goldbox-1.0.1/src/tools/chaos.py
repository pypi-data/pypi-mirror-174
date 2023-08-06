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

import secrets
import random


def get_random_int(start, end, inclusive=False, truly_random=False):
    if inclusive:
        end += 1

    if truly_random:
        return secrets.randbelow(end - start) + start

    else:
        return random.randrange(start, end)


def get_random_float(start, end, inclusive=False, truly_random=False):
    base = get_random_int(start * 100, end * 100, inclusive, truly_random)
    return base / 100
