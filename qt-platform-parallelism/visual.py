import matplotlib.pyplot as plt
from numpy import sqrt
import numpy as np
import json

# file_path = "dummy_data.json"
file_path = "testing_data.json"

GRID = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

POINTS_N_COORDINATES = { # x, y
    0: [0, 2],
    1: [1, 2],
    2: [2, 2],
    3: [0, 1],
    4: [1, 1],
    5: [2, 1],
    6: [0, 0],
    7: [1, 0],
    8: [2, 0]
}

def load_json_data(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def plot_3d(fig, data: dict, index: int, set_name: str):
    # set up the figure and Axes
    ax1 = fig.add_subplot(2, 5, index, projection='3d')

    data1 = data.values()

    # Loading Data
    x = np.array([1, 2, 3, 1, 2, 3, 1, 2, 3])
    y = np.array([3, 3, 3, 2, 2, 2, 1, 1, 1])
    z = np.zeros(9)

    dx = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])  # width of the bars along the x-axis
    dy = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])  # width of the bars along the y-axis
    # dz = data1  # Actual expected height
    dz = [a - 1.5 for a in data1]  # For more detailed visualisation
    colours = ['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']

    # Use three highest peaks
    sorted_dict_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    # top_3 = list(sorted_dict_data.keys())[:3]
    # colours = ['g' if str(a) in top_3 else 'b' for a in range(9)]

    # Use Pressure Simulation Algorithm
    points = compute_contact_triangle_points(sorted_dict_data)
    assert(type(points) is dict)


    for point in points.keys():
        colours[int(point)] = 'b'

    x_centered = x - dx / 2
    y_centered = y - dy / 2

    ax1.bar3d(x_centered, y_centered, z, dx, dy, dz, shade=True, color=colours)
    ax1.set_title('Parallelism Values')
    ax1.set_xlabel('X - Front')
    ax1.set_ylabel('Y - Side')
    ax1.set_zlabel('Z')

    ax1.set_xticks(np.arange(1, 4, 1))
    ax1.set_yticks(np.arange(1, 4, 1))
    # ax1.set_zticks(np.arange(-0.2, 0.2, 0.001))
    ax1.set_title(set_name)
    ax1.set_box_aspect((1, 1, 1))

# Returns the indexes of points of calculated triangle (str)
def compute_contact_triangle_points(sorted_dict_data: dict) -> dict:
    # Highest peak is the largest number
    p1 = list(sorted_dict_data.items())[0]
    p1_index, p1_value = p1


    p2_index, p2_value = compute_p2(sorted_dict_data, (int(p1_index), p1_value))
    p3_index, p3_value = compute_p3(sorted_dict_data, (int(p1_index), p1_value), (int(p2_index), p2_value))
    
    # print(f"P1: {p1_index},{p1_value} - P2: {p2_index},{p2_value} - P3: {p3_index},{p3_value}")

    return {
        int(p1_index): p1_value,
        int(p2_index): p2_value,
        int(p3_index): p3_value
    }
    
def compute_p2(sorted_dict_data: dict, p1: tuple) -> tuple:
    p1_index, p1_value = p1

    if p1_index == 4: # Middle High peak balance case
        # print("Middle peak balance")
        quadrant_groups = {
            1: [1, 2, 5],
            2: [0, 1, 3],
            3: [3, 6, 7],
            4: [5, 7, 8]
        }
        averages = {quadrant: (sum(indexes) / 3) for quadrant, indexes in quadrant_groups.items()}
        sorted_averages = dict(sorted(averages.items(), key=lambda item: item[1], reverse=False))
        
        p2_candidates = quadrant_groups[list(sorted_averages.items())[0][0]] # Indexes in target quadrant are the p2 candidates, still need to find the highest

    else: # Handle Normal Case
        # Get direction that the plane will be sloping down towards
        # Should be pointing towards the middle point
        seek_p2_direction_vector = np.array([1, 1]) - np.array(POINTS_N_COORDINATES[p1_index])
        
        # GET P2 CANDIDATES
        # Consider these points in x - plane
        if seek_p2_direction_vector[0] < 0:
            p2_x_candidates = [point for point in POINTS_N_COORDINATES.keys() if POINTS_N_COORDINATES[point][0] < POINTS_N_COORDINATES[p1_index][0]]
        elif seek_p2_direction_vector[0] > 0:
            p2_x_candidates = [point for point in POINTS_N_COORDINATES.keys() if POINTS_N_COORDINATES[point][0] > POINTS_N_COORDINATES[p1_index][0]]
        else:
            p2_x_candidates = []

        # Consider these points in y - plane
        if seek_p2_direction_vector[1] < 0:
            p2_y_candidates = [point for point in POINTS_N_COORDINATES.keys() if POINTS_N_COORDINATES[point][1] < POINTS_N_COORDINATES[p1_index][1]]
        elif seek_p2_direction_vector[1] > 0:
            p2_y_candidates = [point for point in POINTS_N_COORDINATES.keys() if POINTS_N_COORDINATES[point][1] > POINTS_N_COORDINATES[p1_index][1]]
        else:
            p2_y_candidates = []

        # p2 candidates after plane rotation
        p2_candidates = list(set(p2_x_candidates + p2_y_candidates))

    assert(type(p2_candidates) is list)
    # Get values of p2 candidates
    p2_candidates_index_n_values = {k: v for k, v in sorted_dict_data.items() if int(k) in p2_candidates}

    # Get p2 index & value, from calculating the point with min distance from golden plane touching highest peak    
    p2_index = max(p2_candidates_index_n_values, key=p2_candidates_index_n_values.get)
    p2_value = p2_candidates_index_n_values[p2_index]

    return (p2_index, p2_value)
        
def compute_p3(sorted_dict_data: dict, p1: tuple, p2: tuple) -> tuple:
    p1_index, p1_value = p1
    p2_index, p2_value = p2

    midpoint_x = (POINTS_N_COORDINATES[p1_index][0] + POINTS_N_COORDINATES[p2_index][0]) / 2
    midpoint_y = (POINTS_N_COORDINATES[p1_index][1] + POINTS_N_COORDINATES[p2_index][1]) / 2
    midpoint_z = (p1_value + p2_value) / 2

    # Two peaks balancing case
    if ((midpoint_x, midpoint_y) == (1, 1) 
        or (4 in [p1_index, p2_index])): # BALANCE CASE
        # print("Two Peak balance case")
        group1 = []
        group2 = []
        match (p1_index if p1_index != 4 else p2_index): # Can pre determine which groups to weight average
            case 0 | 8:
                group1.extend([1, 2, 5])
                group2.extend([3, 6, 7])
            case 1 | 7:
                group1.extend([2, 5, 8])
                group2.extend([0, 3, 6])
            case 2 | 6: 
                group1.extend([5, 7, 8])
                group2.extend([0, 1, 3])
            case 3 | 5: 
                group1.extend([6, 7, 8])
                group2.extend([0, 1, 2])
        group1_average = sum([sorted_dict_data[str(index)] for index in group1]) / 3
        group2_average = sum([sorted_dict_data[str(index)] for index in group2]) / 3
        
        p3_candidates = group1 if group1_average > group2_average else group2

    else: # Non balance case
        
        seek_p3_direction_vector = [1 - midpoint_x, 1 - midpoint_y]

        # GET X - plane P3 CANDIDATES
        if seek_p3_direction_vector[0] < 0:
            p3_x_candidates = [point for point in POINTS_N_COORDINATES.keys() if POINTS_N_COORDINATES[point][0] < midpoint_x]
        elif seek_p3_direction_vector[0] > 0:
            p3_x_candidates = [point for point in POINTS_N_COORDINATES.keys() if POINTS_N_COORDINATES[point][0] > midpoint_x]
        else:
            p3_x_candidates = []
        # Get Y - plane P3 candidates
        if seek_p3_direction_vector[1] < 0:
            p3_y_candidates = [point for point in POINTS_N_COORDINATES.keys() if POINTS_N_COORDINATES[point][1] < midpoint_y]
        elif seek_p3_direction_vector[1] > 0:
            p3_y_candidates = [point for point in POINTS_N_COORDINATES.keys() if POINTS_N_COORDINATES[point][1] > midpoint_y]
        else:
            p3_y_candidates = []

        p3_candidates = list(set(p3_x_candidates + p3_y_candidates) - set([p1_index, p2_index]))
        
    assert(type(p3_candidates) is list)
    # print(p3_candidates)    
    p3_candidates = [p3_candidate for p3_candidate in p3_candidates if centre_in_triangle(p1_index, p2_index, p3_candidate)]
    # print(p3_candidates)    

    # Get values of p3 candidates
    p3_candidates_index_n_values = {k: v for k, v in sorted_dict_data.items() if int(k) in p3_candidates}    
    sorted_p3_candidates = dict(sorted(p3_candidates_index_n_values.items(), key=lambda item: item[1], reverse=True))

    p3_index, p3_value = list(sorted_p3_candidates.items())[0]
    return (p3_index, p3_value)

def centre_in_triangle(p1_index: int, p2_index: int, p3_index: int) -> bool:
    if 4 in [p1_index, p2_index, p3_index]:
        return True
    
    def area(x1, y1, x2, y2, x3, y3):
        return abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) / 2.0)
    
    x1, y1 = POINTS_N_COORDINATES[p1_index]
    x2, y2 = POINTS_N_COORDINATES[p2_index]
    x3, y3 = POINTS_N_COORDINATES[p3_index]

    full_area = area(x1, y1, x2, y2, x3, y3)

    area1 = area(1, 1, x2, y2, x3, y3)
    area2 = area(x1, y1, 1, 1, x3, y3)
    area3 = area(x1, y1, x2, y2, 1, 1)

    return full_area == area1 + area2 + area3

def convert_to_3d(point: tuple) -> tuple:
    index, z = point
    x, y = POINTS_N_COORDINATES[index]
    return (x, y, z)

def compute_plane_equation(p1: tuple, p2: tuple, p3: tuple) -> tuple:
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    
    # Calculate two vectors from the points
    v1 = p2 - p1
    v2 = p3 - p1
    
    # Calculate the cross product of the two vectors to get the normal vector
    normal_vector = np.cross(v1, v2)
    
    # The coefficients a, b, and c of the plane equation
    a, b, c = normal_vector
    
    # Calculate d using the point p1
    d = np.dot(normal_vector, p1)
    
    return (round(a, 3), round(b, 3), round(c, 3), -round(d, 3))

def plane_z(plane, x_val, y_val):
    a, b, c, d = plane
    return -(a * x_val + b * y_val + d) / c

def compute_parallelism_value(indexes: list, sorted_dict_data: dict) -> float:
    # Get plane from 3d coordinates of chosen peaks
    p1_3d_coords = convert_to_3d((indexes[0], sorted_dict_data[str(indexes[0])]))
    p2_3d_coords = convert_to_3d((indexes[1], sorted_dict_data[str(indexes[1])]))
    p3_3d_coords = convert_to_3d((indexes[2], sorted_dict_data[str(indexes[2])]))
    
    # Gets plane
    a, b, c, d = compute_plane_equation(p1_3d_coords, p2_3d_coords, p3_3d_coords)

    # Calculate the z values for each of 4 limit corners
    z_val_corner0 = plane_z((a, b, c, d), POINTS_N_COORDINATES[0][0], POINTS_N_COORDINATES[0][1])
    z_val_corner2 = plane_z((a, b, c, d), POINTS_N_COORDINATES[2][0], POINTS_N_COORDINATES[2][1])
    z_val_corner6 = plane_z((a, b, c, d), POINTS_N_COORDINATES[6][0], POINTS_N_COORDINATES[6][1])
    z_val_corner8 = plane_z((a, b, c, d), POINTS_N_COORDINATES[8][0], POINTS_N_COORDINATES[8][1])

    # Translate plane and parallelism val by applying positive of magnitude of lowest point
    translation_val = min([z_val_corner0, z_val_corner2, z_val_corner6, z_val_corner8])

    highest_z = max([z_val_corner0, z_val_corner2, z_val_corner6, z_val_corner8])

    parallelism_value = highest_z - translation_val

    # print(f"Highest Z: {highest_z}")
    # print(f"Lowest Z: {translation_val}")
    # print(f"Parallelism Val: {parallelism_value}")
    
    return parallelism_value, (a, b, c, d)

def compute_flatness(sorted_dict_data: dict, computed_plane: tuple) -> float:
    # find the index with the lowest value, ie the deepest trough in the BP
    # Compute z value of of same index x y coordinate, find difference
    sorted_dict_data = dict(sorted(sorted_dict_data.items(), key=lambda item: item[1], reverse=False))

    lowest_point = list(sorted_dict_data.items())[0]
    index, lowest_z = lowest_point

    equivalent_z = plane_z(computed_plane, POINTS_N_COORDINATES[int(index)][0], POINTS_N_COORDINATES[int(index)][1])

    return abs(equivalent_z - lowest_z)

def generate_graphs(dummy_data):
    fig = plt.figure(figsize=(20, 10))

    num_subplots = 0
    for set_name in dummy_data.keys():
        num_subplots += 1

        dict_data = dummy_data[set_name]
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        for a in dict_data.keys():
            data[int(a)] = dict_data[a]

        plot_3d(fig, dict_data, num_subplots, set_name)

    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.2, hspace=0.1)
    plt.show()


########### PROGRAM

dummy_data = load_json_data(file_path)

for set_name in dummy_data.keys():
    dict_data = dummy_data[set_name]
    sorted_dict_data = dict(sorted(dict_data.items(), key=lambda item: item[1], reverse=True))

    points = compute_contact_triangle_points(sorted_dict_data)
    assert(type(points) is dict)

    points_n_values = list(points.items())

    # Translates, computes plane and parallelism value
    parallelism_value, plane_coeff = compute_parallelism_value(list(points.keys()), sorted_dict_data)
    a, b, c, d = plane_coeff

    flatness = compute_flatness(sorted_dict_data, plane_coeff)

    # a, b, c, d = compute_plane_equation(convert_to_3d(points_n_values[0]), convert_to_3d(points_n_values[1]), convert_to_3d(points_n_values[2]))
    print(f"{set_name:<15} | CALCULATED EQUATION: {'-' if a < 0 else '+'}{abs(a):5} x {'-' if b < 0 else '+'}{abs(b):5} y {'-' if c < 0 else '+'}{abs(c):4} z {'-' if d < 0 else '+'}{abs(d):5} = 0 | PARALLELISM: {parallelism_value:<20} | FLATNESS: {flatness}")


generate_graphs(dummy_data)

# Highest peak will always be touching the plane