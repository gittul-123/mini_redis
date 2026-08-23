class Node:
    """이중 연결 리스트의 노드."""

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    """이중 연결 리스트."""

    def __init__(self):
        self.head = None
        self.tail = None
    
    def insert_front(self, data):
        node = Node(data)

        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        
        return node


    def insert_back(self, data):
        node = Node(data)

        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        
        return node

    def remove_front(self):
        if self.head is None:
            return

        if self.head is self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

    def remove_back(self):
        if self.head is None:
            return

        elif self.head is self.tail: 
            self.head = None
            self.tail = None
        else:
            self.tail=self.tail.prev
            self.tail.next=None

    def remove_node(self, node):
        if self.head is self.tail:
            self.head = None
            self.tail = None

        elif node is self.head:
            self.head = node.next
            self.head.prev = None

        elif node is self.tail:
            self.tail = node.prev
            self.tail.next = None

        else:
            node.prev.next = node.next
            node.next.prev = node.prev

    def move_to_front(self, node):
        if node is self.head:
            return

        if node is self.tail:
            self.tail = node.prev
            self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        node.next = self.head
        node.prev = None
        self.head.prev = node
        self.head = node


