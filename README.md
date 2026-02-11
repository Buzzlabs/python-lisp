# Python Lisp

A repository to help explain how Python's metaprogramming strategies compare among other approaches.
Currently, we use [hylang](https://hylang.org/) to acquire [procedural macros](https://en.wikipedia.org/wiki/Macro_(computer_science)#Procedural_macros) from the Lisp world without having to give up Python's ecosystem.

## Goal 
In here, it is more interesting to make a comparison between them based on important 
criteria (time, moving parts, and abstractions being used) rather than making a judgment of which 
metaprogramming strategy is better. Which metaprogramming strategy is "better" depends
on several factors, including familiarity, so it is not productive to attempt an evaluation in those terms.

By providing this criteria, the programmer should be able to settle expectations when using the metaprogramming
strategy available in the tool of choice. Understanding how to position a strategy in those terms helps gathering
intuition and future proof your solutions based on the trade offs you are aware of already.

## Motivating Example

Our main motivation example is the use of [gRPC](https://grpc.io) in combination with Python. In particular, 
[this example](https://grpc.io/docs/languages/python/quickstart/). We aim to solve this problem of multiple steps
and interaction with generated Python code using metaprogramming.

Hy's solution uses procedural macros to solve this problem. The Python solution comprises both metaclasses and
classes' decorators. 
