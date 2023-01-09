"""
Скрипт для генерации нормированной поверхности и
добавления её в базу

"""
from itertools import combinations
# import Numpy

import numpy as np

import gap_finder.settings
from gap_finder.coordinate import Coordinate
from gap_finder.graphics import build_surface, build_main_surface, init_3d_graphic
from gap_finder.models import get_engine
from gap_finder.services.surfaces import SurfaceService
from gap_finder.settings import (
    DB_SETTINGS,
    GENERATION_TRIES,
    DOTS_COUNT,
    DEVIATION,
    MU
)
from gap_finder.utils import find_equation_plane_rates, is_dot_in_triangle

AXES, PLOT = init_3d_graphic()


def get_x_y_grid(dots_count):
    """
    Генерация квадратной X и Y cетки dots_count на dots_count.

    :param dots_count: количество точек
    :return: X, Y , который возвращает np.meshgrid(x, y)
    """

    x_values = np.linspace(0, dots_count, dots_count + 1, endpoint=True)
    y_values = np.linspace(0, dots_count, dots_count + 1, endpoint=True)
    return np.meshgrid(x_values, y_values)


def generate_main_surface(deviation=DEVIATION, mu=MU):
    """
    Генерация X,Y,Z массивов координат поверхности заготовки, главной поверхности,
    которую мы моделируем.

    X, Y  массивы от np.meshgrid(x, y), см. get_x_y_grid
    Z - сгенирированные по нормальному закону распределения z-координаты поверхности


    :param deviation: дисперсия, диапазон значений
    :param mu: математическое ожидание

    :return: X, Y, Z
    """

    Z = np.random.normal(
        loc=mu,
        scale=deviation,
        size=(DOTS_COUNT + 1, DOTS_COUNT + 1),

    )

    # Генерация X и Y cетки
    X, Y = get_x_y_grid(DOTS_COUNT)
    return X, Y, Z


# TODO: enum
def get_all_coordinates_triplets(coordinates_array):
    """
    Развёртка ndarray'я numpy в список tuple'ов (x,y,z)

    :param coordinates_array: numpy ndarray
    :return: list of named tuples
    """
    coordinates = []
    for index, zn in np.ndenumerate(coordinates_array):
        yn, xn = index
        coordinates.append(Coordinate(xn, yn, zn))

    return coordinates


def build_plane_by_three_coordinates(coord_1: Coordinate, coord_2: Coordinate, coord_3: Coordinate, dots_count):
    """
    Построение плоскости по трём координатам

    :param dots_count:
    :param coord_1:
    :param coord_2:
    :param coord_3:
    :return: X, Y, Z
    """
    x1, y1, z1 = coord_1
    x2, y2, z2 = coord_2
    x3, y3, z3 = coord_3
    a, b, c, d = find_equation_plane_rates(x1, y1, z1, x2, y2, z2, x3, y3, z3)

    def f(x_array, y_array):
        """Уравнение плокости z=f(x,y)"""

        # print("( -", d, "-", a, "*", "X", "-", b, "*", "Y", ")", "/", c)
        return (-d - a * x_array - b * y_array) / c

    XX, YY = get_x_y_grid(dots_count)

    ZZ = f(XX, YY)

    return XX, YY, ZZ


def filter_in_triangle_combinations(combinations_cords, normal_cords):
    """
    Комбинации трёх точек, входящих в треугольник с нормалью
    :return: list of tuples
    """
    in_triangle = []
    for coordinates in combinations_cords:

        if is_dot_in_triangle(coordinates, normal_cords):
            in_triangle.append(coordinates)

    return in_triangle


def filter_normal_coords_in_combinations(combinations_cords, normal_cords):
    # TODO: учитывать ли случай когда точка нормали совпадаетс теми, как быть

    xn, yn, _ = normal_cords

    no_normal = []
    for coordinates in combinations_cords:
        c1, c2, c3 = coordinates

        x1, y1, z1 = c1
        x2, y2, z2 = c2
        x3, y3, z3 = c3
        if x1 == xn or x2 == xn or x3 == xn:
            continue

        if y1 == yn or y2 == yn or y3 == yn:
            continue

        no_normal.append(coordinates)

    return no_normal


def filter_is_not_stucked_plane(plane_coordinates, surface_z_coord):
    square_build_cords = []

    for plane_num, cords in enumerate(plane_coordinates):

        x_plane, y_plane, z_plane = build_plane_by_three_coordinates(*cords, dots_count=DOTS_COUNT)

        was_ok = []

        for index, zn in np.ndenumerate(surface_z_coord):
            yn, xn = index
            one_cord_condition = z_plane[yn][xn] <= surface_z_coord[yn][xn]
            was_ok.append(one_cord_condition)

        if all(was_ok):
            square_build_cords.append(cords)

    return square_build_cords


def log_all_stuff(
        all_coordinates,
        all_possible_combinations,
        in_triangle,
        square_build_cords
):
    message = "\nИз сетки {} x {} т.е. {} количества " \
              "точек получается {} базовых комбинаций 3-х точек.\n" \
              "После поиска трёх точек входящих в треугольник " \
              "с нормалью: {} комб.\n Точек,удовлетворяющих " \
              "условий плоскости: {}"

    print(message.format(
        DOTS_COUNT,
        DOTS_COUNT,
        len(all_coordinates),
        len(all_possible_combinations),
        len(in_triangle),
        len(square_build_cords)))


def generate_one_normal_surface_and_plane_for_it():
    X, Y, Z = generate_main_surface()
    build_main_surface(AXES, PLOT, X, Y, Z)
    all_coordinates = get_all_coordinates_triplets(Z)

    all_possible_combinations = list(combinations(all_coordinates, 3))  # TODO: magic number remove

    # https://stackoverflow.com/questions/44355546/how-to-connect-points-in-python-ax-scatter-3d-plot

    # ЗАДАЧА СВОДИТСЯ К 2D
    normal_x = DOTS_COUNT / 2
    normal_y = DOTS_COUNT / 2
    normal_cords = Coordinate(x=normal_x, y=normal_y, z=0)

    # TODO: rename
    not_with_normal = filter_in_triangle_combinations(all_possible_combinations, normal_cords)
    in_triangle = filter_normal_coords_in_combinations(not_with_normal, normal_cords)
    square_build_cords = filter_is_not_stucked_plane(in_triangle, Z)

    # # TODO: построить вектор нормали
    # X = (0, 1, 1)
    # Y = (0, 1, 1)
    # Z1 = (normal_y, normal_y, 0)
    # Z2 = (normal_y, normal_y, 0)
    # ax.quiver(X, Y, Z1, X, Y, Z2, length=1, arrow_length_ratio=5)

    # plt.show()

    log_all_stuff(
        all_coordinates,
        all_possible_combinations,
        in_triangle,
        square_build_cords
    )

    if not square_build_cords:
        raise IndexError

    for num, plane_cords in enumerate(square_build_cords, start=1):
        cord1, cord2, cord3 = plane_cords
        print("%s) Три точки: %s %s %s" % (num, cord1, cord2, cord3))

        # TODO: показать соединение точек
        x_plane, y_plane, z_plane = build_plane_by_three_coordinates(*plane_cords, dots_count=DOTS_COUNT)
        build_surface(AXES, x_plane, y_plane, z_plane)
        # TODO: отделить граф логику от расчета PLOT.show()

    return {
        "xyz_grid": (X, Y, Z),
        "plane_cords": [[cord1, cord2, cord3]
                        for cord1, cord2, cord3 in square_build_cords],
    }


def main(add_to_db=200):

    '''
    :param add_to_db: сколько поверхностей добавить в базу

    :return:'''

    engine = get_engine(**DB_SETTINGS)
    service = SurfaceService(engine)

    at_db_count = 0
    for x in range(GENERATION_TRIES):

        if at_db_count == add_to_db:
            break

        try:
            print("\n Попытка генерации поверхности №%s" % str(x + 1))
            surface_info = generate_one_normal_surface_and_plane_for_it()
        except IndexError:
            PLOT.cla()
            continue
        else:
            service.insert_new_surface(**surface_info, dots_count=DOTS_COUNT)
            at_db_count += 1
            print("Добавлено %s из %s" % (at_db_count, add_to_db))


if __name__ == '__main__':
    main()
