
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

    if start_point[2] == plane_height == end_point[2]:
        return "Количество точек пересечения бесконечно!"

    elif start_point[2] == end_point[2] and start_point[2] != plane_height:
        return "Прямая параллельна плоскости"

    elif start_point[2] <= plane_height <= end_point[2] or start_point[2] >= plane_height >= end_point[2]:
        sought_x = plane_height   # sought - искомый (с англ.)
        sought_y = start_point[1] + (end_point[1] / end_point[0]) * (plane_height - start_point[0])
        sought_z = start_point[2] + (end_point[2] / end_point[0]) * (plane_height - start_point[0])
        return sought_x, sought_y, sought_z

