import os
import ast
import csv
def dispatch(node):
    if not node:
        return None
    node_type = type(node)
    if node_type is ast.Name:
        return node.id
    elif node_type is ast.NameConstant:
        return str(node.value)
    elif node_type is ast.Ellipsis:
        return '...'
    elif node_type is ast.Subscript:
        return '%s[%s]' % (dispatch(node.value), dispatch(node.slice))
    elif node_type is ast.Index:
        return dispatch(node.value)
    elif node_type is ast.Tuple:
        ret = '('
        if node.elts == 1:
            (elt, ) = node.elts
            ret += dispatch(elt)
            ret += ','
        else:
            # print([type(e) for e in node.elts])
            ret += ','.join([dispatch(e) for e in node.elts])
        ret += ')'
        return ret
    elif node_type is ast.List:
        ret = '['
        if node.elts == 1:
            (elt,) = node.elts
            ret += dispatch(elt)
            ret += ','
        else:
            ret += ','.join([dispatch(e) for e in node.elts])
        ret += ']'
        return ret


class ClassVisitor(ast.NodeVisitor):

    def __init__(self, file):
        self.file = file
        self.func_docs = []

    def visit_ClassDef(self, node):
        cls_name = node.name
        tmp_func_docs = extract_func_docstring(self.file, node, cls_name)
        self.func_docs.extend(tmp_func_docs)


def extract_func_docstring(file, node, cls_name=None):
    func_docs = []
    for b in node.body:
        if isinstance(b, ast.FunctionDef):
            func_name = b.name
            arguments = b.args
            if arguments:
                args = arguments.args
                kwonlyargs = arguments.kwonlyargs
                args_type = []
                kwonlyargs_type = []
                for arg in args:
                    args_type.append(dispatch(arg.annotation))
                for arg in kwonlyargs:
                    kwonlyargs_type.append(dispatch(arg.annotation))
            for bi in b.body:
                if isinstance(bi, ast.Expr) and isinstance(bi.value, ast.Str):
                    func_docs.append(
                        (file,
                         cls_name,
                         func_name,
                         bi.value.s,
                         list(zip([arg.arg for arg in args], args_type)),
                         list(zip([arg.arg for arg in kwonlyargs], kwonlyargs_type)))
                    )
    return func_docs


def extract_docstring_from_file(file):
    with open(file, 'r', encoding='utf-8') as rf:
        content = rf.read()
    root = ast.parse(content)
    result = extract_func_docstring(file, root)
    cls_visitor = ClassVisitor(file)
    cls_visitor.visit(root)
    result.extend(cls_visitor.func_docs)
    return result


def dfs(cur_dir):

    def dfs_dir(cur_dir):
        if not os.path.isdir(cur_dir):
            print("not dir")
            return
        files = os.listdir(cur_dir)
        for file in files:
            new_path = os.path.join(cur_dir, file)
            if os.path.isdir(new_path):
                dfs_dir(new_path)
            elif file.endswith('.py'):
                result.extend(extract_docstring_from_file(new_path))

    result = []
    dfs_dir(cur_dir)
    return result

def main():
    #datasets = ["home-assistant","flask","pytorch","keras"]
    #datasets = ["flask","django","requests","spaCy","keras"]
    datasets = ['flask']
    total_comment_num = 0
    for dataset in datasets:
        index = 0
        pardir = os.path.abspath(os.path.dirname(os.getcwd()))
        result = dfs(os.path.join(pardir,"dataset",dataset))
        with open(os.path.join(pardir,"results",dataset + ".csv"),"w", newline='', encoding='utf8') as csvfile:
            print(dataset)
            writer = csv.writer(csvfile)
            writer.writerow(["index","project","file","func_name","func_doc"])
            for r in result:
                index += 1
                total_comment_num += 1
                file = r[0]
                cls = r[1]
                func_name = r[2]
                doc = r[3]
                #path = file[:-3].split('\\')[1:]
                #if path[0] == 'sh':
                #    path = path[1:]
                #module = '.'.join(path)
                #qualname = '%s%s' % (cls + '.' if cls else '', func_name)
                #print(qualname)
                list1 = [index,dataset,file,func_name,doc]
                
                #print (list1)
                writer.writerows([list1])
    #print ("the total number of comment is"+ str(total_comment_num))
            

if __name__=='__main__':
    main()