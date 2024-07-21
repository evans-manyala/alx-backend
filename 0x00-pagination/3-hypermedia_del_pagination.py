#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import Dict, List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Retrieves a dictionary of paginated data,
        gracefully handling deletions.
        """

        error = "Invalid index"
        assert index is None or (index >= 0 and
                                 index < len(self.__dataset)), error
        index = index if index is not None else 0

        indexed_dataset = self.indexed_dataset()
        indexed_keys = sorted(indexed_dataset.keys())

        data = []
        pos_index = index
        while len(data) < page_size and pos_index < len(indexed_dataset):
            if pos_index in indexed_dataset:
                data.append(indexed_dataset[pos_index])
            pos_index += 1

        next_index = pos_index if pos_index < len(indexed_dataset) else None

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data,
        }
