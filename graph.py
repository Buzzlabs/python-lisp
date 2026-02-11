import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.zaxis.set_rotate_label(False)

ax.grid(True)

ax.set_xlabel('Time', fontsize=14, fontweight='bold', color='b')
ax.set_ylabel('Moving Parts', fontsize=14, fontweight='bold', color='g')
ax.set_zlabel('Abstraction', fontsize=14, fontweight='bold', color='r', labelpad=10)

ax.set_xticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1], ['Compile Time', '', '', '', '', '', '', '', 'Run Time'])
ax.set_yticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1], ['Few', '', '', '', '', '', '', '', 'Many'])
ax.set_zticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1], ['Bits', '', '', '', '', '', '', '', 'Data Structures'], rotation=0, ha='right')

ax.tick_params(axis='x', pad=20)
ax.tick_params(axis='y', pad=15)
ax.tick_params(axis='z', pad=5)

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)

ax.view_init(elev=-37, azim=-146, roll=-45)

# ('h', 'H', '.', 'P', 'X')

ax.scatter(0.5, 0.5, 0.75, color='blue', s=50, marker='o', label='Metaclasses') 
ax.scatter(0.75, 0.5, 0.75, color='blue', s=50, marker='D', label='Class Decorators')
ax.scatter(0.75, -0.25, 1, color='blue', s=50, marker='d', label='Function/Method Decorators')
ax.scatter(0.75, 0.5, -0.5, color='blue', s=50, marker='v', label='Eval/Exec') 
ax.scatter(-0.5, -0.5, 1, color='blue', s=50, marker='^', label='Procedural Macros') 
ax.scatter(-1, 0, -0.75, color='black', s=50, marker='<', label='Preprocessor') 
ax.scatter(-1, 0, 0, color='black', s=50, marker='>', label='Templates') # TODO: study more
ax.scatter(1, -1, 1, color='black', s=50, marker='8', label='Fexprs') 
ax.scatter(-0.75, -0.5, 0.5, color='black', s=50, marker='s', label='Comptime') 
ax.scatter(-0.75, 0.5, 1, color='black', s=50, marker='p', label='Hygienic Macros') 
ax.scatter(-1, 1, -0.5, color='black', s=50, marker='*', label='Reader Macros') 

ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))

plt.show()
