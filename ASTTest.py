import ast
import warnings

warnings.filterwarnings("ignore")
import re

class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.nodes = []

    def generic_visit(self, node):
        self.nodes.append(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)


def code2nodes(code_str):
    visitor = CodeVisitor()
    visitor.visit(ast.parse(code_str))
    node_str = " ".join(visitor.nodes)
    return node_str


def file2str(file):
    with open(file, encoding="utf-8") as fr:
        code_str = fr.read()
    return code_str


def file2nodes(file):
    with open(file, encoding="utf-8") as fr:
        code_str = fr.read()
    return code2nodes(code_str)



def main():
    code_str1 = file2str("hello.py")
    ast_str1 = code2nodes(code_str1)
    print(ast_str1)
    #code_str2 = file2str("test3.py")
    #print("类型编辑距离:", get_sim(code_str1, code_str2))


if __name__ == "__main__":
    main()
