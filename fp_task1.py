class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def print_list(self):
        elements = []
        cur = self.head
        while cur:
            elements.append(str(cur.data))
            cur = cur.next
        print(" → ".join(elements) if elements else "Список порожній")

    # ── Завдання 1: Реверсування списку ─────────────────────────────────

    def reverse(self):
        """
        Реверсує однозв'язний список, змінюючи посилання між вузлами.

        Алгоритм (ітеративний, три вказівники):
          prev = None
          cur  = head
        """
        prev = None
        cur = self.head
        while cur:
            next_node = cur.next   # зберігаємо наступний
            cur.next = prev        # перевертаємо посилання
            prev = cur             # зсуваємо prev
            cur = next_node        # зсуваємо cur
        self.head = prev

    # ── Завдання 2: Сортування вставками ────────────────────────────────

    def insertion_sort(self):
        """
        Сортує список методом вставок (Insertion Sort).

        Алгоритм:
          sorted_head = None  — голова відсортованої частини
          cur = self.head     — поточний вузол невідсортованої частини
        """
        sorted_head = None
        cur = self.head

        while cur:
            next_node = cur.next   # зберігаємо наступний перед вставкою

            # Визначаємо місце для cur у відсортованій частині
            if sorted_head is None or cur.data < sorted_head.data:
                # Вставка на початок відсортованої частини
                cur.next = sorted_head
                sorted_head = cur
            else:
                # Шукаємо правильну позицію
                search = sorted_head
                while search.next and search.next.data < cur.data:
                    search = search.next
                # Вставляємо cur після search
                cur.next = search.next
                search.next = cur

            cur = next_node   # переходимо до наступного невідсортованого

        self.head = sorted_head

    # ── Завдання 3: Злиття двох відсортованих списків ───────────────────

    @staticmethod
    def merge_sorted(list1: "LinkedList", list2: "LinkedList") -> "LinkedList":
        """
        Об'єднує два відсортовані однозв'язні списки в один відсортований.
        Алгоритм (ітеративний з фіктивним вузлом-заглушкою):
          dummy → вузол-заглушка, спрощує обробку голови результату
          tail  → завжди вказує на останній вузол результату
        """
        dummy = Node(0)       # фіктивний вузол — спрощує логіку голови
        tail = dummy

        a = list1.head
        b = list2.head

        while a and b:
            if a.data <= b.data:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next

        # Приєднуємо залишок невичерпаного списку
        tail.next = a if a else b

        result = LinkedList()
        result.head = dummy.next   # пропускаємо фіктивний вузол
        return result


# ── Демонстрація роботи ──────────────────────────────────────────────────

if __name__ == "__main__":

    # --- Завдання 1: Реверсування ---
    print("=" * 50)
    print("Завдання 1: Реверсування списку")
    print("=" * 50)

    lst = LinkedList()
    for val in [1, 2, 3, 4, 5]:
        lst.insert_at_end(val)

    print("До реверсування:   ", end=""); lst.print_list()
    lst.reverse()
    print("Після реверсування:", end=""); lst.print_list()

    # --- Завдання 2: Сортування вставками ---
    print()
    print("=" * 50)
    print("Завдання 2: Сортування вставками")
    print("=" * 50)

    lst2 = LinkedList()
    for val in [64, 25, 12, 22, 11]:
        lst2.insert_at_end(val)

    print("До сортування:   ", end=""); lst2.print_list()
    lst2.insertion_sort()
    print("Після сортування:", end=""); lst2.print_list()

    # --- Завдання 3: Злиття двох відсортованих списків ---
    print()
    print("=" * 50)
    print("Завдання 3: Злиття відсортованих списків")
    print("=" * 50)

    sorted_a = LinkedList()
    for val in [1, 3, 5, 7]:
        sorted_a.insert_at_end(val)

    sorted_b = LinkedList()
    for val in [2, 4, 6, 8]:
        sorted_b.insert_at_end(val)

    print("Список A:", end=" "); sorted_a.print_list()
    print("Список B:", end=" "); sorted_b.print_list()

    merged = LinkedList.merge_sorted(sorted_a, sorted_b)
    print("Злитий: ", end=" "); merged.print_list()
