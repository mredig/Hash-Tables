class DynamicArray():
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.count = 0
        self.storage = [None] * capacity

    def insert(self, value, index):
        if self.count == self.capacity:
            self.double_size()
        
        if index > self.count or index < 0:
            print("Out of bounds error")
            return
        
        self.storage[index] = value

    def append(self, value):
        self.insert(value, self.count)

    def double_size(self):
        self.capacity *= 2
        newStorage = [None] * self.capacity
        
        for i in range(self.count):
            newStorage[i] = self.storage[i]

        self.storage = newStorage
