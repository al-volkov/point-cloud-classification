import math as m
from math import pi, floor
import numpy as np

# point coordinates -(minus camera coordinates)-> vector coordinates ->
# -(x rotation matrix)-> rotated vector -> spherical coordinates ->
# -> coordinates on image


# main function
def project_on_image(point_coordinates, camera_coordinates, camera_angles):
    vector_coordinates = point_coordinates - camera_coordinates
    vector_coordinates[0] *= 0.9997720449
    vector_coordinates[1] *= 0.9997720449
    rotated_vector_coordinates = rotate_vector(vector_coordinates, camera_angles)
    spherical_coordinates = convert_to_spherical_coordinates(rotated_vector_coordinates)
    return spherical_to_mercator(spherical_coordinates[1], spherical_coordinates[2])


def rotate_vector(vector_coordinates, camera_angles):
    return np.asarray(get_rotation_matrix(camera_angles) @ vector_coordinates).reshape(-1)


# camera angles - roll, pitch, heading (in degrees)
def get_rotation_matrix(camera_angles):
    roll_angle, pitch_angle, heading_angle = np.radians(camera_angles)
    return (
        get_roll_rotation_matrix(roll_angle)
        @ get_pitch_rotation_matrix(pitch_angle)
        @ get_heading_rotation_matrix(heading_angle)
    )


def get_roll_rotation_matrix(roll_angle):
    cos_value = np.cos(roll_angle)
    sin_value = np.sin(roll_angle)
    return np.matrix([[cos_value, 0, -sin_value], [0, 1, 0], [sin_value, 0, cos_value]])


def get_pitch_rotation_matrix(pitch_angle):
    cos_value = np.cos(pitch_angle)
    sin_value = np.sin(pitch_angle)
    return np.matrix([[1, 0, 0], [0, cos_value, -sin_value], [0, sin_value, cos_value]])


def get_heading_rotation_matrix(heading_angle):
    cos_value = np.cos(heading_angle)
    sin_value = np.sin(heading_angle)
    return np.matrix([[cos_value, -sin_value, 0], [sin_value, cos_value, 0], [0, 0, 1]])


def convert_to_spherical_coordinates(vector_coordinates):
    x, y, z = vector_coordinates
    x_p_y_sq = x**2 + y**2
    r = m.sqrt(x_p_y_sq + z**2)
    theta = m.atan2(z, m.sqrt(x_p_y_sq))  # elev
    phi = m.atan2(y, x)  # az
    return np.array([r, theta, phi])


width = 8000
height = 4000


def spherical_to_mercator(theta, phi):
    phi *= -1
    x = (width * phi) / (2 * np.pi) + 3 * width / 4
    y = height / 2 - height * np.log(np.tan(theta / 2 + pi / 4)) / np.pi
    return np.array([round(x), round(y)])
