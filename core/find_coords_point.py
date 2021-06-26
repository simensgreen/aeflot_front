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
    x = 0
    y = 1
    z = 2
    if start_point[z] == plane_height == end_point[z]:
        return None

    elif start_point[z] == end_point[z] and start_point[z] != plane_height:
        return None

    elif start_point[z] <= plane_height <= end_point[z] or \
            start_point[z] >= plane_height >= end_point[z]:
        try:

            sought_z = plane_height

            sought_x = ((end_point[x] - start_point[x]) / (end_point[z] - start_point[z])) \
                       * (sought_z - start_point[z]) + start_point[x]

            sought_y = ((end_point[y] - start_point[y]) / (end_point[z] - start_point[z])) \
                       * (sought_z - start_point[z]) + start_point[y]

            return sought_x, sought_y, sought_z
        except ZeroDivisionError:
            return None
