# '''
# Linked List hash table key/value pair
# '''


class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def delete(self):
        if self.next:
            self.value = self.next.value
            self.key = self.next.key
            self.next.delete()
        else:
            self = None

    def deleteKey(self, key):
        if self.key == key:
            self.delete()
            return key
        elif self.next:
            return self.next.deleteKey(key)
        else:
            return None

    def setValueForKey(self, value, key):
        if self.key == key:
            self.value = value
        elif self.next:
            self.next.setValueForKey(value, key)
        else:
            self.next = LinkedPair(key, value)

    def getValueForKey(self, key):
        if self.key == key:
            return self.value
        elif self.next:
            return self.next.getValueForKey(key)
        else:
            return None

    def __repr__(self):
        return f"<{self.key}, {self.value} -> {self.next}>"


class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''

    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity
        self.count = 0

    def _loadCapacity(self):
        return self.count / self.capacity

    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        # return hash(key)
        return self._hash_djb2(key)

    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        hashValue = 5381
        chars = [ord(letter) for letter in key]
        for letter in chars:
            hashValue = (hashValue << 5) + hashValue + letter
        return hashValue & 0xFFFFFFFF

    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash(key) % self.capacity

    def _keyExists(self, key):
        index = self._hash_mod(key)
        node = self.storage[index]
        while node is not None:
            if node.key == key:
                return True
        return False

    def _indexForKey(self, key):
        index = self._hash_mod(key)
        if self.storage[index] is not None:
            return index
        else:
            return None

    def insert(self, key, value):
        '''
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Fill this in.
        '''
        index = self._hash_mod(key)
        newNode = LinkedPair(key, value)
        if self.storage[index] is None:
            self.storage[index] = newNode
            self.count += 1
            self.resizeUp()
        else:
            self.storage[index].setValueForKey(value, key)

    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        index = self._indexForKey(key)
        if index is not None:
            baseNode = self.storage[index]
            if baseNode.key == key:
                self.storage[index] = baseNode.next
                self.count -= 1
                self.resizeDown()
                return key
            else:
                currentNode = baseNode
                nextNode = currentNode.next
                while nextNode is not None:
                    if nextNode.key == key:
                        currentNode.next = nextNode.next
                        self.count -= 1
                        self.resizeDown()
                        return key
                    else:
                        currentNode = nextNode
                        nextNode = currentNode.next
                print("key not found")
                return None
        else:
            print("key not found")
            return None

    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        index = self._indexForKey(key)
        if index is not None:
            return self.storage[index].getValueForKey(key)
        else:
            return None

    def resizeUp(self):
        if self._loadCapacity() < 0.7:
            return
        newHash = HashTable(self.capacity * 2)
        for node in self.storage:
            currentNode = node
            while currentNode is not None:
                newHash.insert(currentNode.key, currentNode.value)
                currentNode = currentNode.next
        self.capacity = newHash.capacity
        self.storage = newHash.storage

    def resizeDown(self):
        if self.capacity < 4:
            return
        if self._loadCapacity() > 0.2:
            return
        newHash = HashTable(self.capacity // 2)
        for node in self.storage:
            currentNode = node
            while currentNode is not None:
                newHash.insert(currentNode.key, currentNode.value)
                currentNode = currentNode.next

        self.capacity = newHash.capacity
        self.storage = newHash.storage
        self.count = newHash.count

if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
