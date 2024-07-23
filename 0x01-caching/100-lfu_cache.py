#!/usr/bin/env python3
"""
LFUCache module
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache class inherits from BaseCaching
    and implements LFU caching.
    """

    def __init__(self):
        """
        Initialize the LFUCache object.
        """
        super().__init__()
        self.freq = {}
        self.min_freq = 0
        self.freq_keys = {}

    def put(self, key, item):
        """
        Assign to the dictionary self.cache_data
        the item value for the key key.
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.get(key)
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:

            min_freq_keys = self.freq_keys[self.min_freq]
            victim = min_freq_keys.pop(0)
            if not min_freq_keys:
                del self.freq_keys[self.min_freq]
            del self.cache_data[victim]
            del self.freq[victim]
            print("DISCARD:", victim)

        self.cache_data[key] = item
        self.freq[key] = 1
        if 1 not in self.freq_keys:
            self.freq_keys[1] = []
        self.freq_keys[1].append(key)
        self.min_freq = 1

    def get(self, key):
        """
        Return the value in self.cache_data linked to key.
        If key is None or if the key doesn’t exist
        in self.cache_data, return None.
        """
        if key is None or key not in self.cache_data:
            return None

        freq = self.freq[key]
        self.freq_keys[freq].remove(key)
        if not self.freq_keys[freq]:
            del self.freq_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        self.freq[key] += 1
        new_freq = self.freq[key]
        if new_freq not in self.freq_keys:
            self.freq_keys[new_freq] = []
        self.freq_keys[new_freq].append(key)

        return self.cache_data[key]
