class Stack():
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)
        if len(self.items) >10:
            self.items.pop(0)

    def pop(self):
        if self.is_empty():
            return None
        else:
            return self.items.pop()
    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.items[len(self.items) - 1]



