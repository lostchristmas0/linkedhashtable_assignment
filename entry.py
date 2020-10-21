"""
file: entry.py
description: the entry(node) used for the linked hashtable
language: python3
author: Dongyu Wu, Chenghui Zhu
"""

class ChainNode:
    """
    The ChainNode class represents each single entry containing its obj and
    links to other entries
    """
    __slots__ = "_obj", "_prev", "_link", "_chain"

    def __init__(self, obj):
        """
        Initialize a new chainNode with a string as its obj
        :param obj: the representing string of itself
        """
        self._obj = obj
        self._prev = None
        self._link = None
        self._chain = None

    def getKey(self, capacity):
        """
        Get the key as the hash code for insertion, calculate the key by the
        capacity of any specific hashtable
        :param capacity: the capacity of the hashtable to be added into
        :return: the calculated hash code(key)
        """
        return (ord(self._obj[0]) - ord("a")) % capacity

    def setPrevious(self, entry):
        """
        Setter to set the previous entry
        :param entry: the previous entry
        """
        self._prev = entry

    def setLink(self, entry):
        """
        Setter to set the next entry
        :param entry: the next entry
        """
        self._link = entry

    def setChain(self, entry):
        """
        Setter to set the forward(chain) entry
        :param entry: the forward(chain) entry
        """
        self._chain = entry

    def getPrevious(self):
        """
        Getter to get the previous entry
        :return: the previous entry
        """
        return self._prev

    def getLink(self):
        """
        Getter to get the next entry
        :return: the next entry
        """
        return self._link

    def getChain(self):
        """
        Getter to get the forward(chain) entry
        :return: the forward(chain) entry
        """
        return self._chain

    def hasLink(self):
        """
        Determine if the entry's next is None
        :return: true if the entry's next is not None
        """
        return not self.getLink() is None

    def __str__(self):
        """
        Return a string of its obj
        :return: the obj of itself
        """
        return self._obj
