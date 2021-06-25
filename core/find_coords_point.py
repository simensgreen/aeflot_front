
def find_intersection_point(space_point: tuple, direction_vector: tuple, plane_height: float):
    """
    Данный метод находит пересечение прямой и плоскости
    (плоскости, которая перпендикулярна оси)

    Args:
        space_point: точка пространства. Необходимо передать кортеж с тремя значениями (x, y, z)
        direction_vector: направляющий вектор. Необходимо передать кортеж с тремя значениями (q1, q2, q3)
        plane_height: высота плоскости (уровень, на котором расположена плоскость, перпендикулярная оси)

    Returns:
         координаты точки пересечения прямой с плоскостью

    Examples:
        >>> find_intersection_point((10.0, -2.0, 3.0), (100.0, 2.0, 9.0), .5)
    """

    sought_x = plane_height   # sought - искомый (с англ.)
    sought_y = space_point[1] + (direction_vector[1] / direction_vector[0]) * (plane_height-space_point[0])
    sought_z = space_point[2] + (direction_vector[2] / direction_vector[0]) * (plane_height-space_point[0])

    return sought_x, sought_y, sought_z
