# -------------------------------------------------
# Дані про їжу
# -------------------------------------------------
items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}


# -------------------------------------------------
# Жадібний алгоритм
# -------------------------------------------------
def greedy_algorithm(items, budget):

    # Обчислення співвідношення калорій до вартості
    sorted_items = sorted(
        items.items(),
        key=lambda item:
        item[1]["calories"] / item[1]["cost"],
        reverse=True
    )

    selected_items = []

    total_cost = 0
    total_calories = 0

    # Вибір страв
    for name, info in sorted_items:

        cost = info["cost"]
        calories = info["calories"]

        if total_cost + cost <= budget:

            selected_items.append(name)

            total_cost += cost
            total_calories += calories

    return {
        "items": selected_items,
        "total_cost": total_cost,
        "total_calories": total_calories
    }


# -------------------------------------------------
# Динамічне програмування
# -------------------------------------------------
def dynamic_programming(items, budget):

    item_list = list(items.items())
    n = len(item_list)

    # Таблиця DP
    dp = [[0 for _ in range(budget + 1)]
          for _ in range(n + 1)]

    # Заповнення таблиці
    for i in range(1, n + 1):

        name, info = item_list[i - 1]

        cost = info["cost"]
        calories = info["calories"]

        for b in range(budget + 1):

            if cost <= b:

                dp[i][b] = max(
                    dp[i - 1][b],
                    dp[i - 1][b - cost] + calories
                )

            else:
                dp[i][b] = dp[i - 1][b]

    # Відновлення вибраних страв
    selected_items = []

    b = budget

    for i in range(n, 0, -1):

        if dp[i][b] != dp[i - 1][b]:

            name, info = item_list[i - 1]

            selected_items.append(name)

            b -= info["cost"]

    selected_items.reverse()

    total_cost = sum(
        items[item]["cost"]
        for item in selected_items
    )

    total_calories = sum(
        items[item]["calories"]
        for item in selected_items
    )

    return {
        "items": selected_items,
        "total_cost": total_cost,
        "total_calories": total_calories
    }


# -------------------------------------------------
# Тестування
# -------------------------------------------------
budget = 100

print("Бюджет:", budget)

print("\nЖадібний алгоритм:")
greedy_result = greedy_algorithm(items, budget)

print(greedy_result)

print("\nДинамічне програмування:")
dp_result = dynamic_programming(items, budget)

print(dp_result)
