import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D


# ── Параметри ──────────────────────────────────────────────────────────────

SCALE      = 0.72   # масштаб дочірніх гілок відносно батьківської
LEFT_SHIFT = 0      # зміщення лівого кута (асиметрія), градуси

node_count   = 0
branch_count = 0
leaf_count   = 0


# ── Кольори ────────────────────────────────────────────────────────────────

TRUNK_COLOR  = (0.545, 0.435, 0.278)   # коричневий
BRANCH_COLOR = (0.290, 0.486, 0.349)   # зелений
LEAF_COLOR   = (0.337, 0.769, 0.412)   # світло-зелений


def depth_color(depth: int, max_depth: int) -> tuple:
    """
    Інтерполює колір між кольором стовбура і кольором гілки
    залежно від глибини рекурсії.

    depth=max_depth  → стовбур (коричневий)
    depth=0          → листок (зелений)
    """
    t = 1.0 - depth / max_depth
    r = TRUNK_COLOR[0] + (BRANCH_COLOR[0] - TRUNK_COLOR[0]) * t
    g = TRUNK_COLOR[1] + (BRANCH_COLOR[1] - TRUNK_COLOR[1]) * t
    b = TRUNK_COLOR[2] + (BRANCH_COLOR[2] - TRUNK_COLOR[2]) * t
    return (r, g, b)


# ── Рекурсивна функція ─────────────────────────────────────────────────────

def draw_tree(ax, x: float, y: float, angle: float,
              length: float, depth: int, max_depth: int,
              branch_angle: float) -> None:
    """
    Рекурсивно будує дерево Піфагора.

    Параметри
    ---------
    ax           : осі matplotlib
    x, y         : початок поточної гілки
    angle        : кут напряму (радіани), 0 = праворуч
    length       : довжина поточної гілки
    depth        : залишкова глибина рекурсії
    max_depth    : початкова глибина (для розрахунку кольору/товщини)
    branch_angle : кут розгалуження (радіани)
    """
    global node_count, branch_count, leaf_count
    node_count += 1

    x_end = x + length * math.cos(angle)
    y_end = y + length * math.sin(angle)

    lw = max(0.4, (depth + 1) * 1.2 * (1.0 if max_depth <= 8 else 0.7))
    color = depth_color(depth, max_depth)

    ax.add_line(Line2D([x, x_end], [y, y_end],
                       color=color, linewidth=lw,
                       solid_capstyle='round'))
    branch_count += 1

    # ── База рекурсії ──
    if depth == 0:
        ax.plot(x_end, y_end, 'o',
                color=LEAF_COLOR, markersize=max(1.5, length * 2.5),
                alpha=0.75, zorder=3)
        leaf_count += 1
        return

    next_len = length * SCALE

    draw_tree(ax, x_end, y_end,
              angle + branch_angle + math.radians(LEFT_SHIFT),
              next_len, depth - 1, max_depth, branch_angle)

    draw_tree(ax, x_end, y_end,
              angle - branch_angle,
              next_len, depth - 1, max_depth, branch_angle)


# ── Допоміжні функції вводу ────────────────────────────────────────────────

def ask_int(prompt: str, default: int, lo: int, hi: int) -> int:
    """Запитує ціле число у діапазоні [lo, hi]. При порожньому вводі — default."""
    while True:
        raw = input(f"{prompt} [{lo}–{hi}, Enter = {default}]: ").strip()
        if raw == "":
            return default
        try:
            val = int(raw)
            if lo <= val <= hi:
                return val
            print(f"  ⚠  Введіть число від {lo} до {hi}.")
        except ValueError:
            print("  ⚠  Потрібне ціле число.")


def ask_float(prompt: str, default: float, lo: float, hi: float) -> float:
    """Запитує дійсне число у діапазоні [lo, hi]. При порожньому вводі — default."""
    while True:
        raw = input(f"{prompt} [{lo}–{hi}, Enter = {default}]: ").strip()
        if raw == "":
            return default
        try:
            val = float(raw)
            if lo <= val <= hi:
                return val
            print(f"  ⚠  Введіть число від {lo} до {hi}.")
        except ValueError:
            print("  ⚠  Потрібне число.")


# ── Головна функція ────────────────────────────────────────────────────────

def main():
    print("=" * 45)
    print("   Дерево Піфагора — генератор фракталу")
    print("=" * 45)
    print()

    max_depth    = ask_int  ("Введіть рівень рекурсії    ", default=8,    lo=1,   hi=14)
    branch_angle = ask_float("Введіть кут розгалуження °  ", default=45.0, lo=10.0, hi=80.0)

    print()
    print(f"Будую дерево: рівень = {max_depth}, кут = {branch_angle}°  …")

    branch_angle_rad = math.radians(branch_angle)

    fig, ax = plt.subplots(figsize=(10, 9))
    fig.patch.set_facecolor('#0b0f0e')
    ax.set_facecolor('#0b0f0e')
    ax.set_aspect('equal')
    ax.axis('off')

    draw_tree(ax, 0.0, 0.0,
              math.pi / 2,
              1.0,
              max_depth, max_depth,
              branch_angle_rad)

    ax.autoscale_view()
    ax.margins(0.05)

    legend_elements = [
        mpatches.Patch(color=TRUNK_COLOR,  label='Стовбур'),
        mpatches.Patch(color=BRANCH_COLOR, label='Гілки'),
        mpatches.Patch(color=LEAF_COLOR,   label='Листки'),
    ]
    ax.legend(handles=legend_elements, loc='lower left',
              facecolor='#111916', edgecolor='#1e2b24',
              labelcolor='#c8ddd1', fontsize=9)

    ax.set_title(
        f"Дерево Піфагора  ·  рівень {max_depth}  ·  кут {branch_angle}°",
        color='#3ddc84', fontsize=12, pad=12
    )

    stats_text = (f"Вузлів: {node_count:,}   "
                  f"Гілок: {branch_count:,}   "
                  f"Листків: {leaf_count:,}")
    fig.text(0.5, 0.01, stats_text,
             ha='center', color='#4a6558', fontsize=8)

    plt.tight_layout()
    out_path = f"pythagorean_tree_d{max_depth}.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())

    print(f"Збережено: {out_path}")
    print(f"Статистика: вузлів = {node_count:,}, "
          f"гілок = {branch_count:,}, листків = {leaf_count:,}")
    plt.show()


if __name__ == "__main__":
    main()
