from doubly_linked_list import DoublyLinkedList

class HashMap:
    def __init__(self):
        self.buckets = [None, None, None, None, None]
        self.size = 0

    def put(self, key, value):
        index = self._hash(key)

        
        if self.buckets[index] is None:
            bucket = DoublyLinkedList()
            self.buckets[index] = bucket
            bucket.insert_front((key, value))
            self.size += 1

        else:
            found = False
            current = self.buckets[index].head

            while current is not None:
                if current.data[0] == key:
                    current.data = (key, value)
                    found = True
                    break

                current = current.next

            if found == False:
                self.buckets[index].insert_front((key,value))
                self.size += 1


        if self.size / len(self.buckets) > 0.75:
            self.resize()



    def get(self, key):
        index = self._hash(key)

        bucket = self.buckets[index]
        
        if bucket is None:
            return None
        
        else:
            current = bucket.head

            while current is not None:
                if current.data[0] == key:
                    return current.data[1]
                
                current = current.next
            
            return None

    def remove(self, key):
        index = self._hash(key)

        bucket = self.buckets[index]

        if bucket is None:
            return  # 삭제할 게 없다는 처리를 해야 함

        current = bucket.head

        while current is not None:
            if current.data[0] == key:
                bucket.remove_node(current)
                self.size -= 1
                break

            current = current.next

    def contains(self, key):
        return self.get(key) is not None

    def keys(self):
        keys = []
        for bucket in self.buckets:
            if bucket is not None:
                current = bucket.head
                while current is not None:
                    keys.append(current.data[0])
                    current = current.next
        return keys


    def resize(self):
        new_buckets = [None] * (len(self.buckets) * 2)

        for bucket in self.buckets:
            if bucket is not None:
                current = bucket.head
                while current is not None:
                    next_node = current.next
                    index = self._hash(current.data[0], len(new_buckets))

                    if new_buckets[index] is None:
                        new_bucket = DoublyLinkedList()
                        new_buckets[index] = new_bucket
                        new_bucket.insert_front(current.data)
                    else:
                        new_buckets[index].insert_front(current.data)

                    current = next_node            
        self.buckets = new_buckets


    def _hash(self, key, bucket_count=None):
        if bucket_count is None:
            bucket_count = len(self.buckets)
        

        hash_value = 0

        for char in key:
            hash_value = hash_value * 31 + ord(char)

        return hash_value % bucket_count


