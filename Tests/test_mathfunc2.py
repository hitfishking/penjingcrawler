# coding: utf-8
import unittest
from mathfunc import *   # 测试用例必须引入待测试的源程序；

class TestMathFunc(unittest.TestCase):   # 测试用例只是构建自己的TestCase继承类，其实例由controller/runner负责构建；这是框架的效果；
    """Test mathfuc.py"""

    def test_add(self):
        """Test method add(a, b)"""
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))

    def test_minus(self):
        """Test method minus(a, b)"""
        self.assertEqual(1, minus(3, 2))

    def test_multi(self):
        """Test method multi(a, b)"""
        self.assertEqual(6, multi(2, 3))

    def test_divide(self):
        """Test method divide(a, b)"""
        self.assertEqual(2, divide(6, 3))
        self.assertEqual(2.5, divide(5, 2))

if __name__ == '__main__':
    unittest.main(verbosity=1)
