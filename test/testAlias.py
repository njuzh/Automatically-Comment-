# def funA():
#     return 'This is funA.'

# funB = funA
# print('run funA:', funA())
# print('run funB:', funB())
# print('name of funA:', funA.__name__)
# print('name of funB:', funB.__name__)
# class ClsA:
#     pass

# ClsB = ClsA

# print('new ClsA:', ClsA())
# print('new ClsB:', ClsB())
# print('name of ClsA:', ClsA.__name__)
# print('name of ClsB:', ClsB.__name__)


class ClsA:
    _cnt = 0
    def __init__(self):
        self.__class__._cnt += 1
        self.idx = self._cnt
ClsB = ClsA
insA = ClsA()
print('new ClsA:', insA)
print('idx of insA:', insA.idx)
insB = ClsB()
print('new ClsB:', insB)
print('idx of insB:', insB.idx)
