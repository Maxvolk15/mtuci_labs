from LinkedList_2 import LinkedList

class Stack:
   def __init__(self):
       self.list = LinkedList()

   def push(self, value):
       self.list.add_first(value)

   def pop(self):
       if self.list.head is None:
           raise IndexError("Попытка удаления из пустого стека")
       value = self.list.head.data
       self.list.delete_first()
       return value

   def peek(self):
       if self.list.head is None:
           raise IndexError("Стек пуст")
       return self.list.head.data

   def size(self):
       return self.list.get_size()

stack = Stack()
for val in [5, 0, 1, 7, 9]:
   stack.push(val)

print(f"Верхний элемент (без удаления): {stack.peek()}")
stack.pop()
stack.pop()
print(f"Верхний элемент после удаления двух: {stack.peek()}")
print(f"Итоговый размер стека: {stack.size()}")