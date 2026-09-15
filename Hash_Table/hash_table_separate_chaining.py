from Hash_Table.abstract_hash_table import HashTable, V
from referential_array import ArrayR
from List.linked_list import LinkedList
from typing import Tuple

class HashTableSeparateChaining(HashTable[str, V]):
    """
    Separate Chaining Hash Table Implementation using a Linked List.
    It currently rehashes the primary cluster to handle deletion.

    constants:
        DEFAULT_TABLE_SIZE: default table size used in the __init__
        DEFAULT_HASH_TABLE: default hash base used for the hash function

    attributes:
        _table: used to represent our internal array
        _length: number of elements in the hash table

    Complexity notation:
        N: number of key-value pairs stored in the hash table
        S: table size / number of buckets
        K: length of the key
        alpha: load factor, N / S
    """

    DEFAULT_TABLE_SIZE = 17
    DEFAULT_HASH_BASE = 31


    def __init__(self, table_size: int = DEFAULT_TABLE_SIZE) -> None:
        """
        :complexity: O(S) where S is the table size.
        """
        if table_size <= 0:
            raise ValueError("Table size should be larger than 0.")

        HashTable.__init__(self)
        self._table: ArrayR[LinkedList[Tuple[str, V]] | None] = ArrayR(table_size)
        self._length = 0

    def hash(self, key: str) -> int:
        """
        Universal Hash function
        :returns: a valid position (0 <= value < table_size) in the hash table
        :complexity: O(K) where K is the length of the key
        """
        if len(self._table) == 1:
            return 0

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % len(self._table)
            a = (a * HashTableSeparateChaining.DEFAULT_HASH_BASE % (len(self._table) - 1)) + 1
        return value

    @property
    def table_size(self) -> int:
        return len(self._table)

    def items(self) -> ArrayR[Tuple[str, V]]:
        """
        Returns all key-value pairs in the hash table.
        :complexity: O(N + S), where N is the number of stored pairs and S is
            the table size. If S is treated as a fixed constant, this can be
            simplified to O(N).
        :auxiliary space: O(N) for the returned array.
        """
        res = ArrayR(self._length)
        i = 0
        for list in self._table:
            if list is not None:
                for item in list:
                    res[i] = item
                    i += 1
        return res
    
    def is_empty(self) -> bool:
        """
        Returns whether the hash table is empty
        :complexity: O(1)
        """
        return self._length == 0

    def is_full(self) -> bool:
        """
        Returns whether the hash table is full
        :complexity: O(1)
        """
        return False

    def __delitem__(self, key: str) -> None:
        """
        Deletes an item from our hash table
        :raises KeyError: when the key doesn't exist
        :complexity:
            Best: O(K) when the target chain is empty or the key is found immediately.
            Average: O(K + alpha) under uniform hashing.
            Worst: O(K + N) when all items collide into one chain.
        """
        position = self.hash(key)
        if self._table[position] is None:
            raise KeyError(key)

        for index, item in enumerate(self._table[position]):
            if item[0] == key:
                if len(self._table[position]) <= 1:
                    self._table[position] = None
                else:
                    self._table[position].delete_at_index(index)

                self._length -= 1
                return

        raise KeyError(key)

    def __getitem__(self, key: str) -> V:
        """
        Get the data associated with a key
        :raises KeyError: when the key doesn't exist
        :complexity:
            Best: O(K) when the key is found immediately or the target chain is empty.
            Average: O(K + alpha) under uniform hashing.
            Worst: O(K + N) when all items collide into one chain.
        """
        position = self.hash(key)
        if self._table[position] is None:
            raise KeyError(key)
        for item in self._table[position]:
            if item[0] == key:
                return item[1]

        raise KeyError(key)

    def __setitem__(self, key: str, data: V) -> None:
        """
        Set a (key, data) pair in our hash table
        :complexity:
            Best: O(K) when the target chain is empty.
            Average: O(K + alpha) under uniform hashing.
            Worst: O(K + N) when all items collide into one chain.
        """
        position = self.hash(key)
        if self._table[position] is None:
            self._table[position] = LinkedList()

        # Attempt to find the key in our linked list
        if len(self._table[position]) > 0:
            for index, item in enumerate(self._table[position]):
                if item[0] == key:
                    # If found update the data
                    self._table[position][index] = (key, data)
                    return

        # Insert at the beginning for better time complexity
        self._table[position].insert(0, (key, data))
        self._length += 1

    def __iter__(self):
        """
        Returns an iterator for the hash table
        :complexity:
            Creating the iterator is O(1).
            Iterating over all values is O(N + S), because every bucket may be
            checked and every stored item is yielded once.
        """
        for list in self._table:
            if list is not None:
                for item in list:
                    yield item[1]

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        :complexity: O(1)
        """
        return self._length

    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular order)
        :complexity: O(N + S), because it first calls items().
        """
        items = self.items()
        items = '\n'.join(map(lambda x: f"({x[0]}, {x[1]})", items))
        return f"<HashTableSeparateChaining\n{items}\n>"
