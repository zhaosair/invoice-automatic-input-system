#-*- coding:utf-8 -*-

from functools import reduce
from math import acos, pi

# 向量加法：同位置元素直接相加
# 向量减法：同位置元素直接相减
# 标量乘法：向量每个元素乘以同一个数字
# 向量大小：向量所有元素的平方和再开方
# 向量方向：向量所有元素除以向量的大小
# 向量点乘：同位置元素直接相乘，最后加总为一个数
# 向量夹角：两个向量点乘 / 两个向量大小
# 向量平行：向量夹角是0或者180度
# 向量正交：向量点乘为零
# 向量投影：投影大小 * 方向向量


class Vector(object):

    def __init__(self, coordinates):
        self.coordinates = tuple(coordinates)
        self.dimension = len(coordinates)

    def __str__(self):
        return "%dD Vector: %s" % (self.dimension, ', '.join(["%.3f" % round(x, 3) for x in self.coordinates]))

    def __eq__(self, v):
        return self.coordinates is v.coordinates

    def _eq_dim(self, v):
        assert self.dimension is v.dimension, "The dimensions of vectors must be equal!"

    def _zero_vec(self):
        assert self.magnitude() != 0, "Encount with zero vector!"

    def plus(self, v):
        self._eq_dim(v)
        return Vector([x + y for x, y in zip(self.coordinates, v.coordinates)])

    def minus(self, v):
        self._eq_dim(v)
        return Vector([x - y for x, y in zip(self.coordinates, v.coordinates)])

    def scalar_mult(self, m):
        return Vector([x * m for x in self.coordinates])

    def magnitude(self, *args):
        return reduce(lambda x, y: x + y, map(lambda z: z ** 2, self.coordinates)) ** 0.5

    def direction(self, *args):
        self._zero_vec()
        return self.scalar_mult(1 / self.magnitude())

    def dot_product(self, v):
        self._eq_dim(v)
        return reduce(lambda x, y: x + y, [a * b for a, b in zip(self.coordinates, v.coordinates)])

    def angle(self, v, degree=False):
        self._zero_vec()
        v._zero_vec()
        measurement = pi / 180 if degree else 1
        return acos(self.dot_product(v) / (self.magnitude() * v.magnitude())) / measurement

    def parallelism(self, v, threshold=10e-6):
        self._eq_dim(v)
        res = False
        if self.magnitude() < threshold or v.magnitude() < threshold:
            res = True
        else:
            ang = self.angle(v)
            if ang < threshold or (pi - ang) < threshold:
                res = True
        return res

    def orthogonality(self, v, threshold=10e-6):
        return abs(self.dot_product(v)) < threshold

    def projection(self, v):
        _v = v.direction()
        weight = self.dot_product(_v)
        return _v.scalar_mult(weight)

