#!/usr/bin/env python
'''
This example demonstrates a simple use of pycallgraph.
'''
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import numpy as np 

class Banana:

    def eat(self):
        pass


class Person:

    def __init__(self):
        self.no_bananas()

    def no_bananas(self):
        self.bananas = []

    def add_banana(self, banana):
        self.bananas.append(banana)

    def eat_bananas(self):
        [banana.eat() for banana in self.bananas]
        self.no_bananas()

def funA():
    return np.arange(10)
def funB():
    print(eval("1+1"))
def main():
    graphviz = GraphvizOutput()
    graphviz.output_file = 'basic2.png'

    with PyCallGraph(output=graphviz):
        person = Person()
        a = funA()
        funB()
if __name__ == '__main__':
    main()