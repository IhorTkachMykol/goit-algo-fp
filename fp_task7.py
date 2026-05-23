import random
import matplotlib.pyplot as plt


# -------------------------------------------------
# Кількість симуляцій
# -------------------------------------------------
NUM_ROLLS = 100000


# -------------------------------------------------
# Словник для підрахунку сум
# -------------------------------------------------
results = {sum_value: 0 for sum_value in range(2, 13)}


# -------------------------------------------------
# Симуляція кидків
# -------------------------------------------------
for _ in range(NUM_ROLLS):

    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)

    total = die1 + die2

    results[total] += 1


# -------------------------------------------------
# Обчислення ймовірностей
# -------------------------------------------------
monte_carlo_probabilities = {}

for total, count in results.items():

    probability = count / NUM_ROLLS

    monte_carlo_probabilities[total] = probability


# -------------------------------------------------
# Аналітичні ймовірності
# -------------------------------------------------
analytical_probabilities = {
    2: 1 / 36,
    3: 2 / 36,
    4: 3 / 36,
    5: 4 / 36,
    6: 5 / 36,
    7: 6 / 36,
    8: 5 / 36,
    9: 4 / 36,
    10: 3 / 36,
    11: 2 / 36,
    12: 1 / 36
}


# -------------------------------------------------
# Виведення таблиці
# -------------------------------------------------
print(f"{'Сума':^10} {'Монте-Карло':^20} {'Аналітична':^20}")

for total in range(2, 13):

    mc = monte_carlo_probabilities[total] * 100
    analytical = analytical_probabilities[total] * 100

    print(f"{total:^10} {mc:^19.2f}% {analytical:^19.2f}%")


# -------------------------------------------------
# Побудова графіка
# -------------------------------------------------
x = list(range(2, 13))

mc_values = [
    monte_carlo_probabilities[i] * 100
    for i in x
]

analytical_values = [
    analytical_probabilities[i] * 100
    for i in x
]

plt.figure(figsize=(10, 6))

plt.plot(
    x,
    mc_values,
    marker='o',
    label='Monte Carlo'
)

plt.plot(
    x,
    analytical_values,
    marker='s',
    linestyle='--',
    label='Analytical'
)

plt.title("Ймовірності сум при киданні двох кубиків")

plt.xlabel("Сума")

plt.ylabel("Ймовірність (%)")

plt.xticks(x)

plt.grid(True)

plt.legend()

plt.show()
