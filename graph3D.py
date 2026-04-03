import matplotlib.pyplot as plt

def project_point(ax, x, y, z, color, marker, label):
    ax.scatter(x, y, z, color=color, s=50, marker=marker, label=label)
    ax.plot([x, 1], [y, y], [z, z], color=color, linestyle='dashed', alpha=0.3)
    ax.scatter(1, y, z, color=color, marker=marker, alpha=0.3, s=40)

fig = plt.figure()
ax = plt.axes(projection='3d', proj_type='ortho')
ax.set_aspect('equal')

ax.zaxis.set_rotate_label(False)

ax.grid(True, linewidth=0.8, alpha=0.6)

ax.set_xlabel('Time', fontsize=14, fontweight='bold', color='black')
ax.set_ylabel('Moving Parts', fontsize=14, fontweight='bold', color='black')
ax.set_zlabel('Abstraction', fontsize=14, fontweight='bold', color='black', labelpad=10)

ax.xaxis.pane.set_facecolor((1.0, 0.8, 0.8, 0.3))  # YZ plane (red tint)
ax.yaxis.pane.set_facecolor((0.8, 1.0, 0.8, 0.3))  # XZ plane (green tint)
ax.zaxis.pane.set_facecolor((1.0, 1.0, 0.6, 0.3))  # XY plane (yellow tint)

ax.set_xticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1], ['Compile Time', '', '', '', '', '', '', '', 'Run Time'])
ax.set_yticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1], ['Few', '', '', '', '', '', '', '', 'Many'])
ax.set_zticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1], ['Bits', '', '', '', '', '', '', '', 'Data Structures'], rotation=0, ha='right')

ax.tick_params(axis='x', pad=20)
ax.tick_params(axis='y', pad=15)
ax.tick_params(axis='z', pad=5)

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)

ax.view_init(elev=-40, azim=-136, roll=-56)

project_point(ax, 0.5, 0.5, 1, 'blue', 'o', 'Metaclasses') 
project_point(ax, 0.75, 0.5, 1, 'blue', 'D', 'Class Decorators')
project_point(ax, 0.75, -0.25, 1, 'blue', 'd', 'Function/Method Decorators')
project_point(ax, 0.75, 0.5, -0.5, 'blue', 'v', 'Eval/Exec') 
project_point(ax, -0.75, -0.5, 1, 'blue', '^', 'Procedural Macros') 
project_point(ax, -1, 0, -0.75, 'black', '<', 'Preprocessor') 
project_point(ax, -0.75, 0.5, 1, 'black', '>', 'Templates')
project_point(ax, 1, -1, 1, 'brown', '8', 'Fexprs') 
project_point(ax, -0.75, -0.75, 0.75, 'black', 's', 'Comptime') 
project_point(ax, -0.75, 0.75, 1, 'black', 'p', 'Hygienic Macros') 
project_point(ax, -1, 1, -0.5, 'deeppink', '*', 'Reader Macros') 

ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))

plt.show()
