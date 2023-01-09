import numpy as np

__all__ = [
    'find_equation_plane_rates',
    'get_triangle_square_from_three_cords',
    'is_dot_in_triangle',
    'calculate_mean_and_standard_deviation'
]


def get_triangle_square_from_three_cords(coord1, coord2, coord3) -> float:
    """
    Площадь треугольника по трём кординатам


    :param coord1:
    :param coord2:
    :param coord3:

    :return: (float) S - площадь треугольника
    """
    x1, y1, _ = coord1
    x2, y2, _ = coord2
    x3, y3, _ = coord3
    S = 0.5 * abs(((x1 - x3) * (y2 - y3)) - ((x2 - x3) * (y1 - y3)))
    return S


def find_equation_plane_rates(x1, y1, z1, x2, y2, z2, x3, y3, z3) -> (int, int, int, int):
    """
    Функция находит коэффициенты уравнения плоскости по трем точкам,
    принимая координаты этих трёх точек.

    # TODO Форматирование докстрингов почитать

    :param x1: Координата x точки #1
    :param y1: Координата y точки #1
    :param z1:  Координата z точки #1
    :param x2: Координата x точки #2
    :param y2: Координата y точки #2
    :param z2:  Координата z точки #2
    :param x3: Координата x точки #3
    :param y3: Координата y точки #3
    :param z3:  Координата z точки #3

    :return: a, b, c, d
    """
    a1 = x2 - x1
    b1 = y2 - y1
    c1 = z2 - z1
    a2 = x3 - x1
    b2 = y3 - y1
    c2 = z3 - z1
    a = b1 * c2 - b2 * c1
    b = a2 * c1 - a1 * c2
    c = a1 * b2 - b1 * a2
    d = (- a * x1 - b * y1 - c * z1)

    # print("equation of plane is ", a, "x +", b, "y +", c, "z +", d, "= 0.")

    return a, b, c, d


# TODO enum
def is_dot_in_triangle(cords: list, cords_to_check: tuple) -> bool:
    """
    Очень простой способ проверить находится ли точка в треугольнике или нет.

    Проверяется сумма площадей трех треугольников, на которые точка.

    :param cords: (tuple(cord, cord, cord)): три точки
    :param cords_to_check:
    :return: (bool) нах
    """

    A_cord, B_cords, C_cords = cords
    ABC = get_triangle_square_from_three_cords(A_cord, B_cords, C_cords)
    ABN = get_triangle_square_from_three_cords(A_cord, B_cords, cords_to_check)
    ACN = get_triangle_square_from_three_cords(A_cord, C_cords, cords_to_check)
    BCN = get_triangle_square_from_three_cords(B_cords, C_cords, cords_to_check)

    triangles_square_sum = (ABN + ACN + BCN)
    equals = ABC >= triangles_square_sum  # TODO: задать вопрос >= или =

    if equals:
        pass
        # print(ABC, ">=" if equals else "<", triangles_square_sum, "=", ABN, "+", ACN, "+", BCN)

    return equals


def calculate_mean_and_standard_deviation(array):
    """
    Стандартное отклонение на основании несмещённой оценки дисперсии
    (подправленная выборочная дисперсия[1],
    в ГОСТ Р 8.736-2011 — «среднее квадратическое отклонение»)

    :return:
    """
    mean = np.mean(array, dtype=np.float64)

    div_el_sum = np.sum(
        [
            (np.power((element - mean), 2) / (len(array) - 1)) for element in array
        ],
        dtype=np.float64
    )
    deviation = np.sqrt(div_el_sum)

    return mean, deviation * 1.2


if __name__ == '__main__':
    print(calculate_mean_and_standard_deviation([1, 2, 3, 4, 5]))
