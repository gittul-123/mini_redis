from doubly_linked_list import DoublyLinkedList

class HashMap:
    def __init__(self):
        self.buckets = [None, None, None, None, None]
        self.size = 0

    def put(self, key, value):
        index = hash(key) % len(self.buckets)

        
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
        index = hash(key) % len(self.buckets)

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
        index = hash(key) % len(self.buckets)

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
                    index = hash(current.data[0]) % len(new_buckets)

                    if new_buckets[index] is None:
                        new_bucket = DoublyLinkedList()
                        new_buckets[index] = new_bucket
                        new_bucket.insert_front(current.data)
                    else:
                        new_buckets[index].insert_front(current.data)

                    current = next_node            
        self.buckets = new_buckets


