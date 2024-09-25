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
    def __init__(self, image_matrix):
        x, y = get_center(image_matrix)
        radio = max_distance_from_center((x,y), image_matrix)
        print(radio)
        image = np.asarray(image_matrix).squeeze()
        plt.figure(figsize=(6, 6))
        plt.imshow(image, cmap="gray_r")
        circle1 = plt.Circle((x, y), radio, fill=False, edgecolor='red', linewidth=2)
        circle2 = plt.Circle((x, y), np.ceil(radio/2), fill=False, edgecolor='red', linewidth=2)
        plt.gca().add_artist(circle1)
        plt.gca().add_artist(circle2)
        plt.plot(x, y, 'ro', markersize=5)
        
        # Dibujar líneas divisorias
        self.draw_dividing_lines(x, y, radio)
        
        self.add_labels(x, y, np.ceil(radio/2), radio)
        plt.axis('equal')
        plt.show()
    
    def draw_dividing_lines(self, x, y, radio):
        angles = np.linspace(0, 2*np.pi, 9)[:-1]  # 8 ángulos equidistantes
        for angle in angles:
            dx = radio * np.cos(angle)
            dy = radio * np.sin(angle)
            plt.plot([x, x + dx], [y, y + dy], color='red', linewidth=2)

    def add_labels(self, x, y, radio_inner, radio_outer):
        factor_inner = 0.7
        factor_outer = 0.85
        
        # Ángulos para cada sección (en radianes)
        angles = np.linspace(0, 2*np.pi, 9)[:-1]
        
        # Ajuste para colocar las etiquetas en el centro de cada sección
        label_angles = angles + np.pi/8
        
        # Orden de las etiquetas en sentido antihorario
        label_order = [8,7,6,5,4,3,2,1]
        
        for i, angle in enumerate(label_angles):
            # Etiqueta para el círculo interior
            xi = x + np.cos(angle) * radio_inner * factor_inner
            yi = y + np.sin(angle) * radio_inner * factor_inner
            plt.text(xi, yi, f'C_1{label_order[i]}', 
                     horizontalalignment='center', 
                     verticalalignment='center',
                     path_effects=[path_effects.Stroke(linewidth=2, foreground='white'), path_effects.Normal()])

            # Etiqueta para el círculo exterior
            xo = x + np.cos(angle) * radio_outer * factor_outer
            yo = y + np.sin(angle) * radio_outer * factor_outer
            plt.text(xo, yo, f'C_2{label_order[i]}', 
                     horizontalalignment='center', 
                     verticalalignment='center',
                     path_effects=[path_effects.Stroke(linewidth=2, foreground='white'), path_effects.Normal()])

