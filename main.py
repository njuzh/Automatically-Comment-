import ast
from pyecharts import Bar
import numpy as np


class MyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.nodes = list()

    def generic_visit(self, node):
        self.nodes.append(node)
        for x in ast.iter_child_nodes(node):
            self.generic_visit(x)


def to_ast(code: str):
    try:
        return ast.parse(code)
    except:
        return None


def lcs(n1: list, n2: list) -> float:
    len1 = len(n1)
    len2 = len(n2)
    vis1 = [0] * len1
    vis2 = [0] * len2
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    path = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    path[0][0] = (0, 0)
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if dp[i - 1][j] >= dp[i][j - 1]:
                dp[i][j] = dp[i - 1][j]
                path[i][j] = (-1, 0)
            else:
                dp[i][j] = dp[i][j - 1]
                path[i][j] = (0, -1)
            if type(n1[i - 1]) == type(n2[j - 1]):
                dp[i][j] = max(dp[i][j], dp[i - 1][j - 1] + 1)
                path[i][j] = (-1, -1)
    cur_x = len1
    cur_y = len2
    while cur_x != 0 and cur_y != 0:
        if path[cur_x][cur_y] == (-1, -1):
            vis1[cur_x - 1] = True
            vis2[cur_y - 1] = True
        dx, dy = path[cur_x][cur_y]
        cur_x += dx
        cur_y += dy
    draw('LCS', vis1, vis2, 'lcs.html')
    return (2 * dp[len1][len2]) / (len1 + len2)


def gst(n1: list, n2: list) -> float:
    len1 = len(n1)
    len2 = len(n2)
    vis1 = [0] * len1
    vis2 = [0] * len2
    minimum_match_length = 3
    max_match = minimum_match_length + 1
    cnt = 1
    while max_match > minimum_match_length:
        max_match = minimum_match_length
        matches = list()
        for i in range(len1):
            for j in range(len2):
                k = 0
                while i + k < len1 and j + k < len2 and type(n1[i + k]) == type(n2[j + k]) \
                        and not vis1[i + k] and not vis2[j + k]:
                    k += 1
                if k == max_match:
                    matches.append((i, j, k))
                elif k > max_match:
                    matches = [(i, j, k), ]
                    max_match = k
        for match in matches:
            i_st, j_st, kk = match
            for ii in range(i_st, i_st + kk):
                vis1[ii] = cnt
            for ii in range(j_st, j_st + kk):
                vis2[ii] = cnt
        cnt += 1
    draw('GST', vis1, vis2, './gst.html')
    return 2 * sum(np.array(vis1) != 0) / (len1 + len2)


def draw(title: str, vis1: list, vis2: list, path: str) -> None:
    tmp1 = list()
    tmp2 = list()
    p = 0
    ed = 0
    while p < len(vis1):
        while ed < len(vis1) and vis1[ed] == vis1[p]:
            ed += 1
        tmp1.append((vis1[p], ed - p))
        p = ed
    p = 0
    ed = 0
    while p < len(vis2):
        while ed < len(vis2) and vis2[ed] == vis2[p]:
            ed += 1
        tmp2.append((vis2[p], ed - p))
        p = ed
    attr = ['code1', 'code2']
    bar = Bar(title)
    for t1 in tmp1:
        bar.add('Block {}'.format(t1[0]), attr, (t1[1], 0), is_stack=True)
    for t2 in tmp2:
        bar.add('Block {}'.format(t2[0]), attr, (0, t2[1]), is_stack=True)
    bar.render(path)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    #     parser.add_argument("file1")
    #     parser.add_argument("file2")
    args = parser.parse_args()
    args.file1 = "test2.py"
    args.file2 = "test3.py"
    with open(args.file1, 'r', encoding='utf-8') as rf:
        root1 = to_ast(rf.read())
    with open(args.file2, 'r', encoding='utf-8') as rf:
        root2 = to_ast(rf.read())
    visitor1 = MyVisitor()
    visitor2 = MyVisitor()
    visitor1.visit(root1)
    visitor2.visit(root2)
    ns1 = visitor1.nodes
    ns2 = visitor2.nodes
    print('LCS Similarity: {:.3f}'.format(lcs(ns1, ns2)))
    print('GST Similarity: {:.3f}'.format(gst(ns1, ns2)))


if __name__ == '__main__':
    main()
