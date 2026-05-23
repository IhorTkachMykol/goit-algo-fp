import heapq

# Граф у вигляді списку суміжності
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('E', 2), ('F', 6)],
    'E': [('C', 10), ('D', 2), ('F', 3)],
    'F': [('D', 6), ('E', 3)]
}

def dijkstra(graph, start):
    # Відстані до всіх вершин
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0

    # Бінарна купа
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Якщо знайдено коротший шлях
        if current_distance > distances[current_vertex]:
            continue

        # Перевірка сусідів
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight

            # Оновлення найкоротшого шляху
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# Запуск алгоритму
start_vertex = 'A'
shortest_paths = dijkstra(graph, start_vertex)

# Виведення результату
print(f"Найкоротші шляхи від вершини {start_vertex}:")
for vertex, distance in shortest_paths.items():
    print(f"{vertex}: {distance}")
