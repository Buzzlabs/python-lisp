import matplotlib.pyplot as plt
import numpy as np

points = [
    (0.5, 0.5, 1, 'blue', 'o', 'Metaclasses'),
    (0.75, 0.5, 1, 'blue', 'D', 'Class Decorators'),
    (0.75, -0.25, 1, 'blue', 'd', 'Function/Method Decorators'),
    (0.75, 0.5, -0.5, 'blue', 'v', 'Eval/Exec'),
    (-0.75, -0.5, 1, 'blue', '^', 'Procedural Macros'),
    (-1, 0, -0.75, 'black', '<', 'Preprocessor'),
    (-0.75, 0.5, 1, 'black', '>', 'Templates'),
    (1, -1, 1, 'brown', '8', 'Fexprs'),
    (-0.75, -0.75, 0.75, 'black', 's', 'Comptime'),
    (-0.75, 0.75, 1, 'black', 'p', 'Hygienic Macros'),
    (-1, 1, -0.5, 'deeppink', '*', 'Reader Macros'),
]

fig, axes = plt.subplots(1, 3, figsize=(24, 8))
grid_ticks = np.arange(-1.25, 1.25, 0.25)

def style_axes(ax, xlabel, ylabel, facecolor, x_labels, y_labels):
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)

    ax.set_aspect('equal', adjustable='box')

    ax.set_xlabel(xlabel, fontsize=14, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=14, fontweight='bold')

    # Apply full grid ticks
    ax.set_xticks(grid_ticks)
    ax.set_yticks(grid_ticks)

    # Hide tick labels (keep grid only)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Grid styling
    ax.grid(True, linewidth=0.8, alpha=0.6)

    # Background tint
    ax.set_facecolor(facecolor)

    # ---- Extreme labels ----
    ax.text(-1, -1.75, x_labels[0], ha='center', va='top', fontsize=11)
    ax.text(1, -1.75, x_labels[1], ha='center', va='top', fontsize=11)

    ax.text(-1.75, -1, y_labels[0], ha='right', va='center', fontsize=11)
    ax.text(-1.75, 1, y_labels[1], ha='right', va='center', fontsize=11)


# ---------------- XY ----------------
ax = axes[0]
for x, y, z, color, marker, label in points:
    ax.scatter(x, y, color=color, marker=marker, s=80, label=label)

style_axes(
    ax,
    "Time",
    "Moving Parts",
    (1.0, 1.0, 0.6, 0.3),
    ("Compile Time", "Run Time"),
    ("Few", "Many")
)

ax.set_title("Time / Moving Parts", fontsize=16)

handles, labels = ax.get_legend_handles_labels()
unique = dict(zip(labels, handles))
ax.legend(unique.values(), unique.keys(),
          loc='center left', bbox_to_anchor=(1.05, 0.5))


# ---------------- XZ ----------------
ax = axes[1]
for x, y, z, color, marker, label in points:
    ax.scatter(x, z, color=color, marker=marker, s=80, label=label)

style_axes(
    ax,
    "Time",
    "Abstraction",
    (0.8, 1.0, 0.8, 0.3),
    ("Compile Time", "Run Time"),
    ("Bits", "Data Structures")
)

ax.set_title("Time / Abstraction", fontsize=16)

handles, labels = ax.get_legend_handles_labels()
unique = dict(zip(labels, handles))
ax.legend(unique.values(), unique.keys(),
          loc='center left', bbox_to_anchor=(1.05, 0.5))


# ---------------- YZ ----------------
ax = axes[2]
for x, y, z, color, marker, label in points:
    ax.scatter(y, z, color=color, marker=marker, s=80, label=label)

style_axes(
    ax,
    "Moving Parts",
    "Abstraction",
    (1.0, 0.8, 0.8, 0.3),
    ("Few", "Many"),
    ("Bits", "Data Structures")
)

ax.set_title("Moving Parts / Abstraction", fontsize=16)

handles, labels = ax.get_legend_handles_labels()
unique = dict(zip(labels, handles))

ax.legend(unique.values(), unique.keys(),
          loc='center left', bbox_to_anchor=(1.05, 0.5))

plt.tight_layout()
plt.show()
