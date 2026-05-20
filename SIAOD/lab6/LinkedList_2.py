class Node:
   def __init__(self, data=None, next_node=None):
       self.data = data
       self.next = next_node

class LinkedList:
   def __init__(self):
       self.head = None

   def add_first(self, value):
       new_node = Node(value)
       new_node.next = self.head
       self.head = new_node

   def add_last(self, value):
       new_node = Node(value)
       if self.head is None:
           self.head = new_node
           return
       current = self.head
       while current.next is not None:
           current = current.next
       current.next = new_node

   def delete_first(self):
       if self.head is None:
           return
       self.head = self.head.next

   def delete_last(self):
       if self.head is None:
           return
       if self.head.next is None:
           self.head = None
           return
       current = self.head
       while current.next.next is not None:
           current = current.next
       current.next = None

   def get_by_index(self, index):
       current = self.head
       count = 0
       while current is not None:
           if count == index:
               return current.data
           count += 1
           current = current.next
       raise IndexError("Индекс вне диапазона")

   def get_size(self):
       length = 0
       current = self.head
       while current is not None:
           length += 1
           current = current.next
       return length

   def __str__(self):
       result = []
       current = self.head
       while current:
           result.append(str(current.data))
           current = current.next
       return " -> ".join(result)

ll = LinkedList()
for val in [5, 3, 5, 20]:
   ll.add_last(val)

ll.add_last(7)
ll.delete_first()
ll.delete_last()

print(f"Итоговая последовательность: {ll}")