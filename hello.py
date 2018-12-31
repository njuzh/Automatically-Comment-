from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph.output import GraphvizOutput
import sys
# sys.path.append("../")
from jce2json2 import *
graphviz = GraphvizOutput(output_file=r'trace_detail.png')
with PyCallGraph(output=graphviz):
    jce2json2.lll()
