import numpy as np
import matplotlib.pyplot as plt

def get_center(image_matrix):
    image_area = image_matrix.sum()
    x_center = np.rint(np.sum(np.arange(1, 28 + 1)[:, np.newaxis] * image_matrix) / image_area)
    y_center = np.rint(np.sum(np.arange(1, 28 + 1) * image_matrix) / image_area)
    return x_center,y_center

class ObjectCircleDivider:
    def __init__(self,image_matrix):
        get_center(image_matrix)

class ShowCircles:
    def __init__(self,image_matrix):
        x, y = get_center(image_matrix)
        image = np.asarray(image_matrix).squeeze()
        plt.imshow(image, cmap="gray_r")
        plt.plot(x, y, 'ro', markersize=5)
        plt.show()