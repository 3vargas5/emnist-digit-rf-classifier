import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

def get_center(image_matrix):
    rows, cols = image_matrix.shape
    image_area = image_matrix.sum()
    x_center = round(np.sum(np.arange(rows)[:, np.newaxis] * image_matrix) / image_area)
    y_center = round(np.sum(np.arange(cols) * image_matrix) / image_area)
    return (y_center,x_center)

def max_distance_from_center(center,image_matrix, threshold = 5) -> int:
    rows, cols = image_matrix.shape
    y, x = np.indices((rows, cols))
    distances_sq = (x - center[0])**2+(y - center[1])**2
    mask = image_matrix > threshold
    return round(np.sqrt(np.max(distances_sq[mask])))

class ObjectCircleDivider:
    def __init__(self,image_matrix):
        center = get_center(image_matrix)


class ShowCircles:
    def __init__(self,image_matrix):
        x, y = get_center(image_matrix)
        radio = max_distance_from_center((x,y),image_matrix)
        print(radio)
        image = np.asarray(image_matrix).squeeze()
        plt.imshow(image, cmap="gray_r")
        circle1 = plt.Circle((x, y), radio, fill=False, edgecolor='red', linewidth=2)
        circle2 = plt.Circle((x, y), np.ceil(radio/2), fill=False, edgecolor='red', linewidth=2)
        plt.gca().add_artist(circle1)
        plt.gca().add_artist(circle2)
        plt.plot(x, y, 'ro', markersize=5)
        plt.plot([x, x], [y - radio, y + radio], color='red', linewidth=2)
        plt.plot([x - radio, x + radio], [y, y], color='red', linewidth=2)
        self.add_labels(x, y, np.ceil(radio/2), radio)
        plt.show()
    
    def add_labels(self, x, y, radio_inner, radio_outer):
        # Factor para ajustar la posición de las etiquetas dentro de cada cuadrante
        factor_inner = 0.35
        factor_outer = 0.55

        # Posiciones para las etiquetas (en sentido horario desde el cuadrante superior derecho)
        positions = [
            (1, -1), (-1, -1), (-1, 1), (1, 1)
        ]

        for i, (dx, dy) in enumerate(positions, start=1):
            # Etiqueta para el círculo interior
            xi = x + dx * radio_inner * factor_inner
            yi = y + dy * radio_inner * factor_inner
            plt.text(xi, yi, f'C_1{i}', 
                     horizontalalignment='center', 
                     verticalalignment='center',
                     path_effects=[path_effects.Stroke(linewidth=2, foreground='white'), path_effects.Normal()])

            # Etiqueta para el círculo exterior
            xo = x + dx * radio_outer * factor_outer
            yo = y + dy * radio_outer * factor_outer
            plt.text(xo, yo, f'C_2{i}', 
                     horizontalalignment='center', 
                     verticalalignment='center',
                     path_effects=[path_effects.Stroke(linewidth=2, foreground='white'), path_effects.Normal()])
