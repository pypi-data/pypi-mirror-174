# goldbox
A library of data structures and utilities used for Python programming. 
Copyright Xavier Mercerweiss, 2022. Licensed under GPLv3.

## Contents
### ***structures***
A variety of data structures.
#### chains
- Node : An object which holds a given value, a reference to a parent, and a reference to a child.
- \_Chain : A basic linked list; used as an abstract class on which full other implementations may build.
- LinkedList : An implementation of a doubly linked list data structure.
- Stack : An implementation of the stack data structure.
- Queue : An implementation of the queue data structure.
- Deque : An implementation of the deque data structure. Inherits from Queue.

#### trees
- BinaryNode : An object which holds a given value, a reference to a parent, a reference to a left child, and a reference to a right child.
- \_Tree : A basic binary tree; used as an abstract class on which other implementations may build.
- BinaryTree : An implementation of the binary tree data structure.
- BinarySearchTree : An implementation of the binary search tree data structure.
- \_Heap : Acts as an abstract class on which heap implementations may build.
- MinHeap : An implementation of the heap data structure, with lower numbers granted greater precedence.
- MaxHeap : An implementation of the heap data structure, with high numbers granted greater precedence.


#### misc
- RangeDict : An extension of the dict class which utilizes a BinarySearchTree to store keys. If passed a key which it does not contain, the value of the nearest key is returned. May only store keys of comparable data types. Missing keys may be rounded either up or down.

### ***tools***
Several basic utilities.
#### chaos
- get_random_int : Generates a random integer within a specific range. 
- get_random_float : Generates a random floatinf point number within a speicfic range.

#### text
- get_lines : Returns the individual lines of a file, with or without whitespace collapsed.
- replace_text_in_file : Replaces all instances of a given string within a file with a specified string.
- shrink : Replaces all instances of a specified number of spaces within a file with a tab character.
- grow : Replaces all instaces of tab characters within a file with a specified number of spaces.

#### misc
- time_it : A function decorator which prints the number of milliseconds it takes a function to execute.

### ***values***
A collection of constant values.
#### text
- LOWER : A string containing all lowercase letters used in English.
- UPPER : A string containing all uppercase letters used in English.
- DIGITS : A string containing digits 0 through 9.
- SPECIALS : ?!@#$%^&\*()[]{}<>-\_+=|/',.
- CHARS : A combination of all strings listed above.


## Changelog
### Version 1.0
- Released project.
