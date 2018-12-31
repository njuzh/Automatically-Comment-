import ast


class CodeVisitor(ast.NodeVisitor):

    def visit_Assign(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)


class CodeVisitor(ast.NodeVisitor):

    def visit_Assign(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)


class CodeVisitor(ast.NodeVisitor):

    def visit_Assign(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)



import ast

if __name__ == '__main__':
    pass
