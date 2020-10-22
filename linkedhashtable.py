"""
file: linkedhashtable.py
description: a linked hashtable that stores entries in a hashtable while keeps
the order of entries insertion
language: python3
author: Dongyu Wu, Chenghui Zhu
"""

from entry import ChainNode
from set import SetType
from collections.abc import Iterable, Iterator

class Linkedhashtable(SetType, Iterable):
    """
    The Linkedhashtable class using a list as the hashtable to hold the key
    object, it uses direct chaining to handle collision, and rehash to keep
    the size in limit
    """
    __slots__ = "_list", "_capacity", "_limit", "_size", "_front", "_back"

    def __init__(self, capacity=100, limit=0.75):
        """
        Initialize an empty hashtable, the default capcity is 1000 and the
        threshold rate (limit) is 0.75
        :param capacity: the initial length of hashtable
        :param limit: the initial threshold rate of hashtable
        """
        self._list = [None] * capacity
        self._capacity = capacity
        self._limit = limit
        self._size = 0
        self._front = None
        self._back = None

    def __iter__(self):
        """
        Initialize an iterator inside hashtable, it will iterate entries
        by the order of insertion
        :return: an iterator
        """
        return Linkedhashtable.Iterator(self)

    class Iterator:
        """
        The internal iterator class
        """
        __slots__ = "i"

        def __init__(self, data):
            """
            Initialize the iterator before the first entry in linkedhashtable
            :param data: the linkedhashtable class
            """
            self.i = ChainNode("")
            self.i.setLink(data._front)

        def __iter__(self):
            """
            Define the iterator itself
            :return: the iterator itself
            """
            return self

        def __next__(self):
            """
            Get the next entry in the linkedhashtable class till the last entry
            :return: the next entry
            """
            if not self.i.hasLink():
                raise StopIteration()
            self.i = self.i.getLink()
            return self.i

    def add(self, entry):
        """
        Adding an entry into the linkedhashtable
        :param entry: the entry being added
        """
        # if the hashtable is empty, the enrty is the first to be added
        if self._size == 0:
            self._list[entry.getKey(len(self._list))] = entry
            self._front = entry
        # if the hashtable is not empty, check if the next entry will cause
        # over threshold and perform a rehash if necessary
        else:
            if self.sizeOver():
                self.rehash()
            self._back.setLink(entry)
            entry.setPrevious(self._back)
            self._add(entry)
        self._size += 1
        self._back = entry


    def _add(self, entry):
        """
        The internal add method for updating hashtable and direct chaining
        :param entry: the entry being added
        """
        if self._list[entry.getKey(len(self._list))] is None:
            self._list[entry.getKey(len(self._list))] = entry
        else:
            temp = self._list[entry.getKey(len(self._list))]
            while not temp.getChain() is None:
                temp = temp.getChain()
            temp.setChain(entry)

    def contains(self, obj):
        """
        Check if an entry(obj) is in hashtable
        :param obj: the entry being checked
        :return: true if this entry is found
        """
        toSearch = ChainNode(obj)
        key = toSearch.getKey(self._capacity)
        temp = self._list[key]
        if self._list[key] is None:
            return False
        elif str(temp) == obj:
            return True
        else:
            while not temp.getChain() is None:
                temp = temp.getChain()
                if str(temp) == obj:
                    return True
        return False

    # def _find(self, obj):
    #     toSearch = Entry(obj)
    #     key = toSearch.getKey(self._capacity)
    #     temp = self._list[key]
    #     if str(temp) == obj:
    #         return temp
    #     else:
    #         while not temp.getChain() is None:
    #             temp = temp.getChain()
    #             if str(temp) == obj:
    #                 return temp
    #     return None

    def remove(self, obj):
        """
        Remove a spcific entry(obj) form the hashtable
        :param obj: the entry being removed
        :return: the removed entry
        """
        if self.contains(obj):
            if self.sizeOff():
                self.rehash()
            toRemoved = ChainNode(obj)
            key = toRemoved.getKey(self._capacity)
            temp = self._list[key]
            temp_back = temp
            # if the entry to be removed is the first item in this linked list
            if str(temp) == obj:
                self._list[key] = self._list[key].getChain()
                temp.setChain(None)
            # else the entry to be removed is in other position than the first
            else:
                while not temp.getChain() is None:
                    temp = temp.getChain()
                    if str(temp) == obj:
                        temp_back.setChain(temp.getChain())
                        temp.setChain(None)
                        break
                    temp_back = temp_back.getChain()

            # if the entry to be removed is the only one left in hashtable
            if temp.getPrevious() is None and temp.getLink() is None:
                self._front = None
                self._back = None
            # if the entry to be removed is front
            elif temp.getPrevious() is None:
                self._front = temp.getLink()
                temp.getLink().setPrevious(None)
                temp.setLink(None)
            # if the entry to be removed is back
            elif temp.getLink() is None:
                self._back = temp.getPrevious()
                temp.getPrevious().setLink(None)
                temp.setPrevious(None)
            # if the entry to be removed is in the middle
            else:
                temp.getPrevious().setLink(temp.getLink())
                temp.getLink().setPrevious(temp.getPrevious())
                temp.setPrevious(None)
                temp.setLink(None)
            self._size -= 1
            return temp

    def _remove(self):
        """
        The internal (directly) remove method, always remove the front entry.
        It will only be called in rehash function, only happened in removing
        from the front to the back
        :return: the removed entry
        """
        temp = self._front
        if self._front == self._back:
            self._list[self._front.getKey(self._capacity)] = None
            self._front = None
            self._back = None
        else:
            self._list[self._front.getKey(self._capacity)] = \
                self._list[self._front.getKey(self._capacity)].getChain()
            self._front.setChain(None)
            self._front = self._front.getLink()
            self._front.setPrevious(None)
            temp.setLink(None)
        self._size -= 1
        return temp

    def sizeOver(self):
        """
        Check if the size of hashtable is over threshold
        :return: true if size is higher than threshold
        """
        return (self._size+1) >= self._capacity * self._limit

    def sizeOff(self):
        """
        Check if the size of hashtable is off limit
        :return: true if size is lower then low limit
        """
        return (self._size-1) < self._capacity * (1 - self._limit) \
               and (self._size-1) > 0

    def rehash(self):
        """
        The rehash function that can either double or halve the capacity of
        hashtable and rearrange all existing entries by its insertion order
        """
        if self.sizeOver():
            self._list = self._list + [None] * self._capacity
            temp_front = self._front.getLink()
            orig_back = self._back
            while not temp_front.getPrevious() is orig_back:
                self.add(self.remove(str(temp_front.getPrevious())))
                temp_front = temp_front.getLink()
            self.add(self.remove(str(temp_front.getPrevious())))
            self._capacity *= 2
        elif self.sizeOff() and self._size > 0:
            temp_list = []
            new_capacity = self._capacity // 2
            while not self._front is None:
                temp_list.append(self._remove())
            for _ in range(new_capacity, self._capacity):
                self._list.pop()
            for item in temp_list:
                self.add(item)
            self._capacity = new_capacity

    # def lookline(self, key):
    #     """
    #     The method for testing the direct chaining at a spcific position(key)
    #     :param key: the location of hashtable
    #     :return: a string contains all entries within the key
    #     """
    #     if self._list[key] is None:
    #         return str(key) + ": " + "None"
    #     else:
    #         temp = self._list[key]
    #         result = str(key) + ": " + str(temp)
    #         while not temp.getChain() is None:
    #             temp = temp.getChain()
    #             result += " -> " + str(temp)
    #         return result

    def __str__(self):
        result = "front -> "
        for item in self:
            result += str(item) + " "
        result += "<- back"
        return result






if __name__ == '__main__':
    # e1 = Entry("batman")
    # e2 = Entry("has")
    # e3 = Entry("lots")
    # e4 = Entry("of")
    # e5 = Entry("gizmos")
    # e6 = Entry("in")
    # e7 = Entry("his")
    # e8 = Entry("belt")
    # l = Linkedhashtable(6, 2)
    # l.add(e1)
    # l.add(e2)
    # l.add(e3)
    # l.add(e4)
    # l.add(e5)
    # l.add(e6)
    # l.add(e7)
    # l.add(e8)

    e1 = ChainNode("lost")
    e2 = ChainNode("christmas")
    e3 = ChainNode("aoi")
    e4 = ChainNode("shigure")
    e5 = ChainNode("sena")
    e6 = ChainNode("jelly")
    e7 = ChainNode("fish")
    e8 = ChainNode("code")
    e9 = ChainNode("geass")
    e10 = ChainNode("gebera")
    e11 = ChainNode("cc")
    e12 = ChainNode("blue")
    l = Linkedhashtable(6, 0.8)
    l.add(e1)
    l.add(e2)
    l.add(e3)
    l.add(e4)
    l.add(e5)
    l.add(e6)
    l.add(e7)
    l.add(e8)
    l.add(e9)
    l.add(e10)
    l.add(e11)
    l.add(e12)

    for item in l:
        print(item)


    print(l._size)
    print(l._capacity)

    print(l._front)
    print(l._back)
    # for i in range(l._capacity):
    #     print(l.lookline(i))

    print(l.contains("aoi"))
    print(l.contains("lost"))
    print(l.contains("blue"))
    print(l.contains("cc"))
    print(l.contains("aaaaa"))

    # print("start remove--------------------")
    # l.remove("cc")
    # l.remove("fish")
    # l.remove("geass")
    # l.remove("lost")
    # l.remove("blue")
    # l.remove("christmas")
    # l.remove("gebera")
    # l.remove("shigure")
    # l.remove("aoi")
    # l.remove("sena")
    # l.remove("code")
    # l.remove("jelly")
    #
    # for item in l:
    #     print(item)
    # print("\n")
    #
    # print("size: " + str(l._size))
    # print("capacity: " + str(l._capacity))
    #
    # print(l._front)
    # print(l._back)
    # for i in range(l._capacity):
    #     print(l.lookline(i))