from gap_finder.coordinate import Coordinate
from gap_finder.generation import (
    build_plane_by_three_coordinates,
    build_surface,
    build_main_surface,
    PLOT,
    AXES
)
from gap_finder.models import get_engine
from gap_finder.services.surfaces import SurfaceService
from gap_finder.settings import DB_SETTINGS

import numpy as np

"""
Песочница для каких-либо quick-check-пук-штук
"""


# GapFinderTestCase().run()

def calcalate_Ra(coords: list):
    """
    Среднее арифметическое отклонение профиля Ra – среднее
    арифметическое из абсолютных значений отклонений профиля
    в пределах базовой длины:
        Ra ≈ 1/n ⋅ ∑ y i ,
    где l – базовая длина;
    n - число выбранных точек профиля на базовой длине;
    y – отклонение профиля от средней линии.

    :param coords:
    :return:
    """

    coords = [abs(cord) for cord in coords]
    return sum(coords) * (1 / len(coords))


def calculate_Rz(coords: list):
    """
    Высота неровностей по десяти точкам Rz – сумма средних абсолют-
    ных значений высот пяти наибольших выступов профиля и глубин
    пяти наибольших впадин профиля в пределах базовой длины:

    Rz = (∑ y pi + ∑ y vi) / 5 ,
    где y pi - высота i -го наибольшего выступа профиля;
    y vi - глубина i -й наибольшей впадины профиля.
    :param coords:
    :return:
    """
    # TODO: понять как... если их не десять выступов
    coords = [abs(cord) for cord in coords]
    return sum(coords) / 5


def show_current_surface(surface, axes, plot, show=False):
    cord1, cord2, cord3 = surface.plane_cords[0]
    cord1 = Coordinate(*cord1)
    cord2 = Coordinate(*cord2)
    cord3 = Coordinate(*cord3)

    x, y, z = build_plane_by_three_coordinates(
        cord1, cord2, cord3,
        dots_count=surface.dots_count
    )

    X, Y, Z = surface.xyz_grid
    build_main_surface(axes, plot, X, Y, Z)
    build_surface(axes, x, y, z)

    if show:
        plot.show()

    return X, Y, Z


def corr2_coeff(A, B):
    # Rowwise mean of input arrays & subtract from input arrays themeselves
    A_mA = A - A.mean(1)[:, None]
    B_mB = B - B.mean(1)[:, None]

    # Sum of squares across rows
    ssA = (A_mA ** 2).sum(1)
    ssB = (B_mB ** 2).sum(1)

    # Finally get corr coeff
    return np.dot(A_mA, B_mB.T) / np.sqrt(np.dot(ssA[:, None], ssB[None]))


# if __name__ != '__main__':
#     engine = get_engine(**DB_SETTINGS)
#     service = SurfaceService(engine)
#     surfaces = service.get_surfaces(limit=200)
#
#     Ra = []
#     for surface in surfaces:
#         X, Y, Z = show_current_surface(surface)
#
#         rA_lines = sum(
#             [calcalate_Ra(Z[i]) for i in range(surface.dots_count + 1)]
#         ) / (surface.dots_count + 1)
#
#         Ra.append(rA_lines)
#
#     Ra = sum(Ra) / len(Ra)
#     print("Ra=", Ra)

if __name__ == '__main__':
    engine = get_engine(**DB_SETTINGS)
    service = SurfaceService(engine)
    surface = service.get_surfaces(limit=1)[0]
    show_current_surface(surface, AXES, PLOT, show=True)
