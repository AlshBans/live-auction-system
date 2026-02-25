class Stack:
    def __init__(self):
        self.stack = []

    def clear(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise IndexError("pop from an empty stack")

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            raise IndexError("peek from an empty stack")

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)


class DualPriorityQueue:
    def __init__(self, primary_weight=1, secondary_weight=1):
        self.heap = []
        self.primary_weight = primary_weight
        self.secondary_weight = secondary_weight

    def clear(self):
        self.heap = []

    def push(self, item, primary_priority, secondary_priority):
        """Push an item onto the priority queue with the given priorities."""
        self.heap.append((primary_priority, secondary_priority, item))
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        """Pop the item with the highest priority from the queue."""
        if not self.is_empty():
            self._swap(0, len(self.heap) - 1)
            item = self.heap.pop()[2]
            self._heapify_down(0)
            return item
        else:
            raise IndexError("pop from an empty priority queue")

    def peek(self):
        """Return the item with the highest priority without removing it."""
        if not self.is_empty():
            return self.heap[0][2]
        else:
            return None

    def is_empty(self):
        """Check if the priority queue is empty."""
        return len(self.heap) == 0

    def size(self):
        """Return the size of the priority queue."""
        return len(self.heap)

    def _heapify_up(self, index):
        """Ensure the heap property is maintained after insertion."""
        parent_index = (index - 1) // 2
        if index > 0 and self._compare(self.heap[index], self.heap[parent_index]) < 0:
            self._swap(index, parent_index)
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        """Ensure the heap property is maintained after removal."""
        smallest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2

        if left_child < len(self.heap) and self._compare(self.heap[left_child], self.heap[smallest]) < 0:
            smallest = left_child

        if right_child < len(self.heap) and self._compare(self.heap[right_child], self.heap[smallest]) < 0:
            smallest = right_child

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _swap(self, i, j):
        """Swap two items in the heap."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _compare(self, item1, item2):
        """Compare two items based on their priorities."""
        primary1, secondary1, _ = item1
        primary2, secondary2, _ = item2
        
        # Calculate weighted values
        weighted_primary1 = primary1 * self.primary_weight
        weighted_primary2 = primary2 * self.primary_weight
        weighted_secondary1 = secondary1 * self.secondary_weight
        weighted_secondary2 = secondary2 * self.secondary_weight

        # Total comparisons (lower values are better)
        total1 = weighted_primary1 + weighted_secondary1
        total2 = weighted_primary2 + weighted_secondary2

        return total1 - total2  # Lower total means higher priority

    def update_priority(self, item, new_primary_priority, new_secondary_priority):
        """Update the priority of an item in the queue."""
        for index, (primary, secondary, i) in enumerate(self.heap):
            if i == item:
                self.heap[index] = (new_primary_priority, new_secondary_priority, item)
                self._heapify_up(index)  # Adjust the position of the updated item
                self._heapify_down(index)  # Ensure the heap property is maintained
                return

    def set_weights(self, primary_weight, secondary_weight):
        """Set new weights for primary and secondary priorities."""
        self.primary_weight = primary_weight
        self.secondary_weight = secondary_weight


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
    def clear(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data):
        if self.head is None:
            return
        if self.head.data == data:
            self.head = self.head.next
            return
        current = self.head
        while current.next is not None and current.next.data != data:
            current = current.next
        if current.next is not None:
            current.next = current.next.next

    def search(self, data):
        current = self.head
        while current is not None:
            if current.data == data:
                return True
            current = current.next
        return False

    def display(self):
        elements = []
        current = self.head
        while current is not None:
            elements.append(current.data)
            current = current.next
        return elements
