"""
file: test.py
description: the unit test file to test functions in Linkedhashtable class
language: python3
author: Dongyu Wu, Chenghui Zhu
"""

import unittest

from entry import ChainNode
from linkedhashtable import Linkedhashtable

class Test(unittest.TestCase):
    """
    Test is the unit test class for testing Linkedhashtable
    """

    def test_add(self):
        """
        Test the add and _add function
        """
        e1 = ChainNode("we")
        e2 = ChainNode("are")
        e3 = ChainNode("the")
        e4 = ChainNode("light")
        e5 = ChainNode("miwa")
        table = Linkedhashtable()
        self.assertEqual(str(table), "front -> <- back")
        table.add(e1)
        table.add(e2)
        table.add(e3)
        table.add(e4)
        table.add(e5)
        self.assertEqual(str(table), "front -> we are the light miwa <- back")

    def test_iterator(self):
        """
        Test the iterator class
        """
        e1 = ChainNode("we")
        e2 = ChainNode("are")
        e3 = ChainNode("the")
        e4 = ChainNode("light")
        e5 = ChainNode("miwa")
        table = Linkedhashtable()
        table.add(e1)
        table.add(e2)
        table.add(e3)
        table.add(e4)
        table.add(e5)
        temp = table.__iter__()
        self.assertEqual(str(temp.__next__()), "we")
        self.assertEqual(str(temp.__next__()), "are")
        self.assertEqual(str(temp.__next__()), "the")
        self.assertEqual(str(temp.__next__()), "light")
        self.assertEqual(str(temp.__next__()), "miwa")

    def test_contains(self):
        """
        Test the contains function
        """
        e1 = ChainNode("we")
        e2 = ChainNode("are")
        e3 = ChainNode("the")
        e4 = ChainNode("light")
        e5 = ChainNode("miwa")
        table = Linkedhashtable()
        table.add(e1)
        table.add(e2)
        table.add(e3)
        table.add(e4)
        table.add(e5)
        self.assertTrue(table.contains("we"))
        self.assertTrue(table.contains("the"))
        self.assertTrue(table.contains("miwa"))
        self.assertFalse(table.contains("you"))
        self.assertFalse(table.contains("wee"))

    def test_remove(self):
        """
        Test the remove function
        """
        e1 = ChainNode("we")
        e2 = ChainNode("are")
        e3 = ChainNode("the")
        e4 = ChainNode("light")
        e5 = ChainNode("miwa")
        table = Linkedhashtable()
        table.add(e1)
        table.add(e2)
        table.add(e3)
        table.add(e4)
        table.add(e5)
        self.assertEqual(str(table), "front -> we are the light miwa <- back")
        table.remove("we")
        self.assertEqual(str(table), "front -> are the light miwa <- back")
        table.remove("miwa")
        self.assertEqual(str(table), "front -> are the light <- back")
        table.remove("the")
        self.assertEqual(str(table), "front -> are light <- back")

    def test_rehash(self):
        """
        Test the rehash, sizeOver, sizeOff, and _remove functions
        """
        e1 = ChainNode("rise")
        e2 = ChainNode("on")
        e3 = ChainNode("up")
        e4 = ChainNode("till")
        e5 = ChainNode("ya")
        e6 = ChainNode("touching")
        e7 = ChainNode("moon")
        e8 = ChainNode("we")
        e9 = ChainNode("are")
        e10 = ChainNode("the")
        e11 = ChainNode("light")
        e12 = ChainNode("miwa")
        table = Linkedhashtable(6, 0.8)
        self.assertEqual(table._size, 0)
        self.assertEqual(table._capacity, 6)
        self.assertEqual(len(table._list), 6)
        table.add(e1)
        table.add(e2)
        table.add(e3)
        table.add(e4)
        table.add(e5)
        table.add(e6)
        table.add(e7)
        table.add(e8)
        table.add(e9)
        table.add(e10)
        table.add(e11)
        table.add(e12)
        self.assertEqual(table._size, 12)
        self.assertEqual(table._capacity, 24)
        self.assertEqual(len(table._list), 24)
        self.assertEqual(str(table),"front -> rise on up till ya touching moon"
                                     " we are the light miwa <- back")
        table.remove("ya")
        table.remove("up")
        table.remove("are")
        table.remove("on")
        table.remove("miwa")
        table.remove("moon")
        table.remove("rise")
        table.remove("the")
        self.assertEqual(table._size, 4)
        self.assertEqual(table._capacity, 12)
        self.assertEqual(len(table._list), 12)
        self.assertEqual(str(table), "front -> till touching we light <- back")
        table.remove("we")
        self.assertEqual(table._size, 3)
        self.assertEqual(table._capacity, 12)
        self.assertEqual(len(table._list), 12)
        self.assertEqual(str(table), "front -> till touching light <- back")
        table.remove("till")
        self.assertEqual(table._size, 2)
        self.assertEqual(table._capacity, 6)
        self.assertEqual(len(table._list), 6)
        self.assertEqual(str(table), "front -> touching light <- back")
        table.remove("light")
        self.assertEqual(table._size, 1)
        self.assertEqual(table._capacity, 3)
        self.assertEqual(len(table._list), 3)
        self.assertEqual(str(table), "front -> touching <- back")
        table.remove("touching")
        self.assertEqual(table._size, 0)
        self.assertEqual(table._capacity, 3)
        self.assertEqual(len(table._list), 3)
        self.assertEqual(str(table), "front -> <- back")


if __name__ == "__main__":
    unittest.main()
