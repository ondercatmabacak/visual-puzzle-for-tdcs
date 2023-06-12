from math import sin, cos, radians

def rotate_point(point, angle, center_point=(0, 0)):
    """Rotates a point around center_point(origin by default)
    Angle is in degrees.
    Rotation is counter-clockwise
    """
    angle_rad = radians(angle % 360)
    # Shift the point so that center_point becomes the origin
    new_point = (point[0] - center_point[0], point[1] - center_point[1])
    new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                 new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))
    # Reverse the shifting we have done
    new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
    return new_point

print(rotate_point((1, 1), 90, (2, 1)))
# This prints (2.0, 0.0)
print(rotate_point((1, 1), -90, (2, 1)))
# This prints (2.0, 2.0)
print(rotate_point((2, 2), 45, (1, 1)))
# This prints (1.0, 2.4142) which is equal to (1,1+sqrt(2))