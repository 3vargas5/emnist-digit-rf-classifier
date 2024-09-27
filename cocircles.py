import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

def get_center(image_matrix):
    rows, cols = image_matrix.shape
    image_area = image_matrix.sum()
    x_center = round(np.sum(np.arange(rows)[:, np.newaxis] * image_matrix) / image_area)
    y_center = round(np.sum(np.arange(cols) * image_matrix) / image_area)
    return (y_center,x_center)

def max_distance_from_center(center,image_matrix, threshold = 10) -> int:
    rows, cols = image_matrix.shape
    y, x = np.indices((rows, cols))
    distances_sq = (x - center[0])**2+(y - center[1])**2
    mask = image_matrix > threshold
    return np.ceil(np.sqrt(np.max(distances_sq[mask])))

class ObjectCircleDivider:
    def __new__(cls, image_matrix):
        x, y = get_center(image_matrix)
        radius = max_distance_from_center((x, y), image_matrix)
        dictionary = cls.weighted_average_points_by_section((x, y), np.ceil(radius / 2), radius, image_matrix)
        return dictionary
    
    @staticmethod
    def find_section_point(i, j, center, radius_inner, radius_outer):
        x, y = center
        x0 = j - x
        y0 = -i + y
        distance_center2point = np.sqrt(x0**2 + y0**2)
        angle_center_point = np.arctan2(y0, x0)
        
        if distance_center2point <= radius_inner:
            circle_position = 1
        elif distance_center2point <= radius_outer:
            circle_position = 2
        else:
            circle_position = -1
        
        if 0 <= angle_center_point < np.pi / 4:
            angle_position = 1
        elif np.pi / 4 <= angle_center_point < np.pi / 2:
            angle_position = 2
        elif np.pi / 2 <= angle_center_point < 3 * np.pi / 4:
            angle_position = 3
        elif 3 * np.pi / 4 <= angle_center_point < np.pi:
            angle_position = 4
        elif -np.pi <= angle_center_point < -3 * np.pi / 4 or angle_center_point == np.pi:
            angle_position = 5
        elif -3 * np.pi / 4 <= angle_center_point < -np.pi / 2:
            angle_position = 6
        elif -np.pi / 2 <= angle_center_point < -np.pi / 4:
            angle_position = 7
        elif -np.pi / 4 <= angle_center_point < 0:
            angle_position = 8
        
        return circle_position, angle_position
    
    @staticmethod
    def weighted_average_points_by_section(center, radius_inner, radius_outer, image_matrix, threshold=0):
        x = center[0]
        y = center[1]
        point_divisions = {}
        count_points_sections = {}
        for i, j in np.ndindex(image_matrix.shape):
            circle_position, angle_position = ObjectCircleDivider.find_section_point(i, j, (x, y), radius_inner, radius_outer)
            if circle_position == -1:
                continue
            key = f'C_{circle_position}{angle_position}'
            if key not in point_divisions:
                point_divisions[key] = 0
            elif image_matrix[i, j] > threshold:
                point_divisions[key] += image_matrix[i, j]
            if key not in count_points_sections:
                count_points_sections[key] = 0
            else:
                count_points_sections[key] += 1
        sorted_keys = sorted(point_divisions.keys(), key=lambda k: (int(k[2]), int(k[3])))
        result = {key: round(point_divisions[key] / (count_points_sections[key] * 255), 6) for key in sorted_keys}
        return result

    
class ShowCircles:
    def __init__(self, image_matrix):
        x, y = get_center(image_matrix)
        radius = np.ceil(max_distance_from_center((x,y), image_matrix))
        image = np.asarray(image_matrix).squeeze()
        plt.figure(figsize=(6, 6))
        plt.imshow(image, cmap="gray_r")

        # Draw Circles
        circle1 = plt.Circle((x, y), radius, fill=False, edgecolor='red', linewidth=2)
        circle2 = plt.Circle((x, y), np.ceil(radius/2), fill=False, edgecolor='red', linewidth=2)
        plt.gca().add_artist(circle1)
        plt.gca().add_artist(circle2)
        plt.plot(x, y, 'ro', markersize=5)
        
        # Draw Lines
        self.draw_dividing_lines(x, y, radius)
        self.add_labels(x, y, np.ceil(radius/2), radius)
        plt.plot(6,14,"bo")
        plt.axis('equal')
        plt.show()
    
    def draw_dividing_lines(self, x, y, radius):
        angles = np.linspace(0, 2*np.pi, 9)[:-1]
        for angle in angles:
            dx = radius * np.cos(angle)
            dy = radius * np.sin(angle)
            plt.plot([x, x + dx], [y, y + dy], color='red', linewidth=2)

    def add_labels(self, x, y, radius_inner, radius_outer):
        factor_inner = 0.7
        factor_outer = 0.85
        angles = np.linspace(0, 2*np.pi, 9)[:-1]
        label_angles = angles + np.pi/8
        label_order = [8,7,6,5,4,3,2,1]
        for i, angle in enumerate(label_angles):
            # Inner Circle
            xi = x + np.cos(angle) * radius_inner * factor_inner
            yi = y + np.sin(angle) * radius_inner * factor_inner
            plt.text(xi, yi, f'C_1{label_order[i]}', 
                     horizontalalignment='center', 
                     verticalalignment='center',
                     path_effects=[path_effects.Stroke(linewidth=2, foreground='white'), path_effects.Normal()])

            # Outer Circle
            xo = x + np.cos(angle) * radius_outer * factor_outer
            yo = y + np.sin(angle) * radius_outer * factor_outer
            plt.text(xo, yo, f'C_2{label_order[i]}', 
                     horizontalalignment='center', 
                     verticalalignment='center',
                     path_effects=[path_effects.Stroke(linewidth=2, foreground='white'), path_effects.Normal()])

