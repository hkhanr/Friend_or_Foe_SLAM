import pandas as pd
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

## g2o file path
g2o_file = '/home/haris/usb_dataaa/g2o_final_solved/intel/intel_solved_false.g2o'

g2o_data = pd.read_csv(g2o_file, header=None)

vertices = []
edges = []
for line in g2o_data[0]:
    if "VERTEX_SE2" in line:
        line = line.split()
        vertices.append(line)
        # print(vertices)
    elif "EDGE_SE2" in line:
        line = line.split()
        edges.append(line)
vertices = np.array(vertices).astype(object)
edges = np.array(edges).astype(object)
# print(vertices)
# ax = plt.axes(projection='3d')
for idx, edge in enumerate(edges):
    if idx == 0:
        continue
    vertex1 = vertices[int(edge[1])]
    vertex2 = vertices[int(edge[2])]
    # if int(vertex2[1]) - int(vertex1[1]) > 1:
        # continue
    vertex1 = [float(vertex1[2]), float(vertex1[3])]
    vertex2 = [float(vertex2[2]), float(vertex2[3])]
    x_points = np.array([vertex1[0], vertex2[0]])
    y_points = np.array([vertex1[1], vertex2[1]])
    # print(vertex1)
    # print(vertex2)
    plt.plot(x_points, y_points, 'r')
    # print('yes')

x_points = (vertices[1:, 2]).astype(float)
y_points = (vertices[1:, 3]).astype(float)
text = np.arange(1, len(vertices))
plt.plot(x_points, y_points, 'o', color = 'blue', markersize = 2)
# for i,txt in enumerate(text):
#     plt.annotate(str(txt), (x_points[i],y_points[i]), size=7)
plt.show()

total_lc = 0
false_lc = 0
true_lc = 0
for idx, edge in enumerate(edges):
    if idx == 0:
        continue
    if int(edge[2]) - int(edge[1]) == 1:
        continue
    total_lc = total_lc + 1
    if (float(edge[3]) == 0) & (float(edge[4]) == 0) & (float(edge[5]) == 0):
        false_lc = false_lc + 1
    else:
        true_lc = true_lc + 1
print('Detected')
print('total_lc  = ', total_lc)
print('true_lc  = ', true_lc)
print('false_lc  = ', false_lc)

actual_total_lc = 13
actual_true_lc = 5
actual_false_lc = 8
print('actual_total_lc  = ', actual_total_lc)
print('actual_true_lc  = ', actual_true_lc)
print('actual_false_lc  = ', actual_false_lc)

TP = true_lc
FP = false_lc
TN = actual_false_lc - false_lc
FN = actual_true_lc - true_lc
print('True_positives = ', TP)
print('True_negatives = ', TN)
print('False_positives = ', FP)
print('False_negatives = ', FN)
print('Precision = ', TP/(TP+FP))
print('Recall = ', TP/(TP+FN))