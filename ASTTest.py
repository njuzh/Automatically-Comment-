import ast
import warnings

warnings.filterwarnings("ignore")
import re
#import Levenshtein


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


# def get_sim(file1, file2):
#     with open(file1, encoding="utf-8") as fr:
#         code_str1 = fr.read()
#     with open(file2, encoding="utf-8") as fr:
#         code_str2 = fr.read()
#     node_str1 = code2nodes(code_str1)
#     node_str2 = code2nodes(code_str2)
#     return Levenshtein.distance(node_str1, node_str2)


# def get_code_str_sim(code_str1, code_str2):
#     node_str1 = code2nodes(code_str1)
#     node_str2 = code2nodes(code_str2)
#     return Levenshtein.distance(node_str1, node_str2)


# def get_sim(code_str1, code_str2):
#     node_str1 = code2nodes(code_str1)
#     node_str2 = code2nodes(code_str2)
#     return Levenshtein.distance(node_str1, node_str2)


# def get_node_sim(node1, node2):
#     return Levenshtein.distance(node1, node2)


def file2str(file):
    with open(file, encoding="utf-8") as fr:
        code_str = fr.read()
    return code_str


def file2nodes(file):
    with open(file, encoding="utf-8") as fr:
        code_str = fr.read()
    return code2nodes(code_str)


# def get_sim(code_str1, code_str2):
#     node_str1 = code2nodes(code_str1)
#     node_str2 = code2nodes(code_str2)
#     return Levenshtein.distance(node_str1.lower(), node_str2.lower())


def main():
    code_str1 = file2str("test2.py")
    ast_str1 = code2nodes(code_str1)
    print(ast_str1)
    #code_str2 = file2str("test3.py")
    #print("类型编辑距离:", get_sim(code_str1, code_str2))


if __name__ == "__main__":
    main()
