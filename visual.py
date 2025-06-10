import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def visualize_boyer_moore(text, pattern):
    n = len(text)
    m = len(pattern)
    positions = []
    s = 0

    match_color = '#7FFF00'
    mismatch_color = '#FF4500'
    shift_color = '#1E90FF'
    default_color = '#F0F0F0'

    fig, ax = plt.subplots(figsize=(12, 4))

    text_objects = [ax.text(i, 0, text[i], ha='center', va='center',
                            bbox=dict(facecolor=default_color, edgecolor='black'))
                    for i in range(n)]

    pattern_objects = [ax.text(s + k, -0.5, pattern[k], ha='center', va='center',
                               bbox=dict(facecolor='#FFD700', edgecolor='black'))
                       for k in range(m)]

    arrow = None

    def update(frame):
        nonlocal s, positions, arrow

        if arrow is not None:
            arrow.remove()
            arrow = None

        ax.set_title(f'Шаг: s = {s}', fontsize=14)

        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            text_objects[s + j].set_bbox(dict(facecolor=match_color, edgecolor='black'))
            j -= 1

        if j >= 0:
            text_objects[s + j].set_bbox(dict(facecolor=mismatch_color, edgecolor='black'))

            bad_char_shift = max(1, j - (pattern.rfind(text[s + j]) if text[s + j] in pattern else -1))
            s += bad_char_shift

            arrow = ax.annotate('', xy=(s, -0.2), xytext=(s - bad_char_shift, -0.2),
                                arrowprops=dict(arrowstyle='->', color=shift_color, lw=2))
        else:
            positions.append(s)
            for k in range(m):
                text_objects[s + k].set_bbox(dict(facecolor=match_color, edgecolor='black'))
            s += 1

        for k in range(m):
            pattern_objects[k].set_position((s + k, -0.5))


        if s > n - m:
            return text_objects + pattern_objects

        return text_objects + pattern_objects


    ani = FuncAnimation(fig, update, frames=np.arange(n), interval=1000, blit=True)


    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(np.arange(n), list(text), fontsize=12)
    plt.yticks([])
    plt.xlim(-0.5, n - 0.5)
    plt.show()

    print(f"Найденные позиции: {positions}")


text = "ABACADABRAC"
pattern = "ABAC"
visualize_boyer_moore(text, pattern)