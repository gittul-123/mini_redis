

class MinHeap:
    def __init__(self):
        self.heap = []

    def size(self):
        return len(self.heap)

    def peek(self):
        if self.heap == []:
            return None

        return self.heap[0]

    def push(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        parent = (index - 1) // 2

        while index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]

            index = parent
            parent = (index - 1) // 2