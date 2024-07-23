#!/usr/bin/env python3
"""
LIFOCache module
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache class inherits from BaseCaching
    and implements LIFO caching.
    """

    def __init__(self):
        """
        Initialize the LIFOCache object.
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Assign to the dictionary self.cache_data
        the item value for the key key.
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                del self.order[self.order.index(key)]
            self.cache_data[key] = item
            self.order.append(key)
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                discarded_key = self.order.pop()
                del self.cache_data[discarded_key]
                print("DISCARD:", discarded_key)

    def get(self, key):
        """
        Return the value in self.cache_data linked to key.
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
