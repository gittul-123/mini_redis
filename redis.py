import time
from hashmap import HashMap
from doubly_linked_list import DoublyLinkedList
from min_heap import MinHeap


class Redis:
    def __init__(self):
        self.store = HashMap()
        self.lru = DoublyLinkedList()
        self.ttl_heap = MinHeap()

        self.maxmemory = 0
        self.used_memory = 0
        self.evicted_keys = 0

    def set(self, key, value):
        self._remove_expired()

        old_value = self.store.get(key)

        new_memory = self._calculate_memory(key, value)

        if old_value is not None:
            old_memory = self._calculate_memory(key, old_value)

            current = self.lru.head

            while current is not None:                          
                if current.data[0] == key:
                    self.lru.remove_node(current)
                    break

                current = current.next

            self.ttl_heap.remove(key)

        else:
            old_memory = 0

        new_used_memory = self.used_memory - old_memory + new_memory

        if self.maxmemory > 0 and new_memory > self.maxmemory:
            return "(error) OOM"


        while self.maxmemory > 0 and new_used_memory > self.maxmemory:
            lru_node = self.lru.tail
            evict_key, evict_value = lru_node.data
            self.store.remove(evict_key)
            self.lru.remove_node(lru_node)
            new_used_memory -= self._calculate_memory(evict_key, evict_value)
            self.evicted_keys += 1

        self.store.put(key,value)
        self.used_memory = new_used_memory

        found = False

        current = self.lru.head

        while current is not None:
            if current.data[0] == key:
                self.lru.remove_node(current)
                self.lru.insert_front((key, value))
                found = True
                break

            current = current.next

        if found == False:
            self.lru.insert_front((key, value))

    def get(self, key):
        self._remove_expired()
        value = self.store.get(key)

        if value is None:
            return None

        current = self.lru.head

        while current is not None:
            if current.data[0] == key:
                data = current.data
                self.lru.remove_node(current)
                self.lru.insert_front(data)
                break

            current = current.next

        return value
    
    def delete(self, key):
        self._remove_expired()


        value = self.store.get(key)

        if value is None:
            return 0

        self.store.remove(key)
        self.ttl_heap.remove(key)

        self.used_memory -= self._calculate_memory(key, value) 

        current = self.lru.head

        while current is not None:
            if current.data[0] == key:
                self.lru.remove_node(current)
                break

            current = current.next
        
        return 1

    def expire(self, key, seconds):
        self._remove_expired()

        if not self.store.contains(key):
            return 0

        expire_at = time.time() + seconds

        self.ttl_heap.remove(key)
        self.ttl_heap.push((expire_at, key))

        return 1

    def ttl(self, key):
        self._remove_expired()

        if not self.store.contains(key):
            return -2
        current = 0

        while current < len(self.ttl_heap.heap):
            if self.ttl_heap.heap[current][1] == key:
                expire_at = self.ttl_heap.heap[current][0]
                remaining = expire_at - time.time()
                return int(remaining)

            current += 1

        return -1


    def _remove_expired(self):
        while self.ttl_heap.size() > 0:
            expire_at, key = self.ttl_heap.peek()

            if expire_at > time.time():
                break

            self.ttl_heap.pop()

            value = self.store.get(key)

            if value is None:
                continue

            self.store.remove(key)

            self.used_memory -= self._calculate_memory(key, value)

            current = self.lru.head

            while current is not None:
                if current.data[0] == key:
                    self.lru.remove_node(current)
                    break

                current = current.next

    def exists(self, key):
        self._remove_expired()
        if self.store.contains(key):
            return 1

        return 0


    def keys(self):
        self._remove_expired()
        return self.store.keys()


    def dbsize(self):
        self._remove_expired()
        return self.store.size


    def _calculate_memory(self, key, value):
        return len(key.encode("utf-8")) + len(value.encode("utf-8"))


    def config(self, maxmemory):
        try:
            maxmemory = int(maxmemory)
        except ValueError:
            return "(error) ERR value is not an integer or out of range"

        if maxmemory < 0:
            return "(error) ERR value is not an interger or out of range"

        self.maxmemory = maxmemory

        return "OK"


    def info(self):
        self._remove_expired()
        
        return(
            f"used_memory:{self.used_memory}\n"
            f"maxmemory:{self.maxmemory}\n"
            f"evicted_keys:{self.evicted_keys}"
        )