Mochi
====
Mochi is a dynamically typed programming language for functional programming and actor-style programming.

Its interpreter is written in Python3. The interpreter translates a program written in Mochi to Python3's AST / bytecode.

## Features
- Python-like syntax
- Tail recursion optimization (self tail recursion only), and no loop syntax
- Re-assignments are not allowed in function definition.
- Basic collection type is a persistent data structure. (using Pyrsistent)
- Pattern matching / Data types, like algebraic data types
- Pipeline operator
- Syntax sugar of anonymous function definition
- Actor, like the actor of Erlang (using Eventlet)
- Macro, like the traditional macro of Lisp
- Builtin functions includes functions exported by itertools module, recipes, functools module and operator module

