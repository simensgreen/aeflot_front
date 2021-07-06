from functools import lru_cache


@lru_cache(maxsize=1024)
def find_intersections_section(sections, plane_height):
    intersections = (find_intersection_point(section[0], section[1], plane_height) for section in sections)
    return [intersection for intersection in intersections if intersection]


@lru_cache(maxsize=1024)
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


def find_intersection_segment(triangle_points_coords_list: list, plane_height):
    start_point = 0
    end_point = 1
    intersection_point = []

    triangle_sides = [[tuple(triangle_points_coords_list[i]),
                       tuple(triangle_points_coords_list[(i + 1) % 3])] for i in range(3)]

    for side in triangle_sides:
        search_intersection_point = find_intersection_point(side[start_point],
                                                            side[end_point],
                                                            plane_height)
        if search_intersection_point is None:
            pass
        else:
            intersection_point.append(search_intersection_point)

    return tuple(intersection_point)


def points_side_converter(data, geometric_primitive: str):
    """
    Данный метод объединяет точки отрезки или разбивает отрезки на точки
    Args:
        data: набор данных (точек или отрезков), может быть как списком, так и кортежем
        geometric_primitive: "points" или "sides" (в зависимости от того, что передаётся в data)

    Returns: либо набор точек, либо набор отрезков

    """
    output_set = []

    if geometric_primitive == "sides":
        for side in data:
            output_set.append(side[0])
            output_set.append(side[1])

    elif geometric_primitive == "points":
        if len(data) % 2 == 0:
            return [(data[point], data[point + 1]) for point in range(0, len(data), 2)]
        else:
            data.pop(len(data) - 1)
            return [(data[point], data[point + 1]) for point in range(0, len(data), 2)]

    else:
        return TypeError("Неизвестный геометрический примитив!")

    return output_set


if __name__ == '__main__':
    points = [(1, 2), (3, 4), (4, 1), (0, 3), (1, 2)]
    sides = (((1, 2), (6, 3)), ((5, 9), (0, 4)), ((3, 5), (1, 0)), ((9, 3), (4, 8)), ((2, 4), (1, 1)))

    print(points_side_converter(sides, "sides"))
