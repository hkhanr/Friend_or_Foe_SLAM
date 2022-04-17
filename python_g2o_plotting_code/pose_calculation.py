import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R


input_file = 'poses_LC_Keyframes.txt'
output_file = 'nstp_poses.g2o'
f = open(input_file, "r")
text = f.read()
poses_text = text.split(':\n')
pose_arrays = []
for i, pose_text in enumerate(poses_text):
    if i == 0:
        continue
    pose_text = pose_text.split('\n\n')[0]
    pose_text = pose_text[1:]
    pose_text = pose_text[:-1]
    temp_array = np.zeros((4,4))
    print(pose_text)
    rows = pose_text.split(';\n')
    for i,row in enumerate(rows):
        elements = row.split(',')
        for j,element in enumerate(elements):
            element = float(element)
            temp_array[i,j] = element
            print(element)
    pose_arrays.append(temp_array)
print(text)

vertices_df = pd.DataFrame()
vertices_df = vertices_df.append([['VERTEX_SE3:QUAT', '0', '0', '0', '0', '0', '0', '0', '1']],ignore_index=True)
print(vertices_df)
for i,pose_array in enumerate(pose_arrays):
    vertex_text = 'VERTEX_SE3:QUAT'
    vertex_number = str(i+1)
    T = pose_array[0:3, 3]
    x = str(T[0])
    y = str(T[1])
    z = str(T[2])
    R_matrix = pose_array[0:3, 0:3]
    r = R.from_matrix(R_matrix)
    r = r.as_quat()
    qx = str(r[0])
    qy = str(r[1])
    qz = str(r[2])
    qw = str(r[3])
    vertices_df = vertices_df.append([[vertex_text, vertex_number, x, y, z, qx, qy, qz, qw]], ignore_index=True)

vertices_df = vertices_df.apply(" ".join, 1)

print(vertices_df)

edges_df = pd.DataFrame()
inf_matrix = '1 0 0 0 0 0 1 0 0 0 0 1 0 0 0 4.00073 -0.000375887 0.0691425 3.9997 -8.5017e-05 4.00118'

edge_text = 'EDGE_SE3:QUAT'
pose_array = pose_arrays[0]
T = pose_array[0:3, 3]
x = str(T[0])
y = str(T[1])
z = str(T[2])
R_matrix = pose_array[0:3, 0:3]
r = R.from_matrix(R_matrix)
r = r.as_quat()
qx = str(r[0])
qy = str(r[1])
qz = str(r[2])
qw = str(r[3])
edges_df = edges_df.append([[edge_text, '0', '1', x, y, z, qx, qy, qz, qw, inf_matrix]])

for i in range(0, len(pose_arrays)-1):
    index_first = str(i+1)
    index_last = str(i+2)
    pose_A = pose_arrays[i]
    pose_B = pose_arrays[i+1]
    T_A = pose_A[0:3, 3]
    T_B = pose_B[0:3, 3]
    R_A = pose_A[0:3, 0:3]
    R_B = pose_B[0:3, 0:3]
    inv_R_A = np.linalg.inv(R_A)
    inv_T_A = np.matmul(-inv_R_A,T_A)
    inv_M_A = np.zeros((4,4))
    inv_M_A[0:3, 0:3] = inv_R_A
    inv_M_A[0:3, 3] = inv_T_A
    inv_M_A[3,3] = 1

    M_B = pose_B
    pose_AB = np.matmul(inv_M_A,M_B)
    print(pose_AB)
    T = pose_AB[0:3, 3]
    x = str(T[0])
    y = str(T[1])
    z = str(T[2])
    R_matrix = pose_AB[0:3, 0:3]
    r = R.from_matrix(R_matrix)
    r = r.as_quat()
    qx = str(r[0])
    qy = str(r[1])
    qz = str(r[2])
    qw = str(r[3])
    edges_df = edges_df.append([[edge_text, index_first, index_last, x, y, z, qx, qy, qz, qw, inf_matrix]])


edges_df = edges_df.apply(" ".join, 1)
new_g2o = pd.concat([vertices_df, edges_df])
new_g2o.to_csv(output_file, index=None, header=None)
print(edges_df)



