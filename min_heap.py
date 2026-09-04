

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

    def pop(self):
        if self.heap == []:
            return None
        
        min_value = self.heap[0]

        self.heap[0] = self.heap[len(self.heap)-1]
        self.heap.pop()
        self._heapify_down(0)
        return min_value
    
    def _heapify_down(self, index):
        left = 2 * index + 1

        while left < len(self.heap):
            right = 2 * index + 2
            smaller_child = left

            if right < len(self.heap):
                if self.heap[right] < self.heap[left]:
                    smaller_child = right

                else:
                    smaller_child = left

            if self.heap[index] > self.heap[smaller_child]:
                self.heap[index], self.heap[smaller_child] = self.heap[smaller_child], self.heap[index]
                index = smaller_child
                left = 2 * index + 1
                right = 2 * index + 2

            else:
                break


    def remove(self, key):
        current = 0

        while current < len(self.heap):
            if self.heap[current][1] == key:
                self.heap[current] = self.heap[-1]
                self.heap.pop()

                if current == len(self.heap):
                    return

                if current > 0:
                    parent = (current - 1) // 2

                    if self.heap[current] < self.heap[parent]:
                        self._heapify_up(current)

                    else:
                        self._heapify_down(current)

                else:
                    self._heapify_down(current)


                return

            current += 1