import functools


@functools.lru_cache()
def find_intersection_point(start_point: tuple, end_point: tuple, plane_height: float):
    """
    Данный метод находит пересечение прямой и плоскости
    (плоскости, которая перпендикулярна оси)

    Args:
        start_point: точка пространства. Необходимо передать кортеж с тремя значениями (x, y, z)
        end_point: направляющий вектор. Необходимо передать кортеж с тремя значениями (q1, q2, q3)
        plane_height: высота плоскости (уровень, на котором расположена плоскость, перпендикулярная оси)

    Returns:
         координаты точки пересечения прямой с плоскостью

    Examples:
        >>> find_intersection_point((10.0, -2.0, 3.0), (100.0, 2.0, 9.0), .5)
    """
    number = 2
    if start_point[number] == plane_height == end_point[number]:
        return None

    elif start_point[number] == end_point[number] and start_point[number] != plane_height:
        return None

    elif start_point[number] <= plane_height <= end_point[number] or start_point[number] >= plane_height >= end_point[number]:
        try:
            sought_x = start_point[0] + (end_point[0] / end_point[2]) * (-start_point[2])
            sought_y = start_point[1] + (end_point[1] / end_point[2]) * (-start_point[2])
            sought_z = plane_height
            return sought_x, sought_y, sought_z
        except ZeroDivisionError:
            return None
