from gap_finder.generation import (
    PLOT,
    AXES
)
from gap_finder.models import get_engine
from gap_finder.sandbox import show_current_surface
from gap_finder.services.surfaces import SurfaceService
from gap_finder.settings import DB_SETTINGS

import numpy as np

from gap_finder.utils import find_equation_plane_rates
from gap_finder.coordinate import Coordinate
import math


def find_angle_between_two_planes(
        plane_coords1: tuple,
        plane_coords2: tuple
):
    #     TODO: взять между нормалями

    """
    Косинус угла между плоскостями и его значение угла


    :param plane_coords1:
    :param plane_coords2:
    :return:
    """
    cord1_1, cord1_2, cord1_3 = plane_coords1
    cord2_1, cord2_2, cord2_3 = plane_coords2

    a1, b1, c1, d1 = 0, 0, 0, 1

    a2, b2, c2, d2 = find_equation_plane_rates(
        *cord2_1,
        *cord2_2,
        *cord2_3
    )

    print("First plane rates %s*x+%s*y+c%s+%s" % (a1, b1, c1, d1))
    print("Second plane rates %s*x+%s*y+c%s+%s" % (a2, b2, c2, d2))

    sqrt_sum_1 = math.sqrt(
        sum([
            pow(a1, 2),
            pow(b1, 2),
            pow(c1, 2),
            pow(d1, 2)])
    )

    sqrt_sum_2 = math.sqrt(
        sum([
            pow(a2, 2),
            pow(b2, 2),
            pow(c2, 2),
            pow(d2, 2)])
    )

    print(sqrt_sum_1, sqrt_sum_2)
    sum_multiplication = abs(a1 * a2 + b1 * b2 + c1 * c2)
    cos_alpha = sum_multiplication / (sqrt_sum_1 * sqrt_sum_2)

    return cos_alpha


if __name__ == '__main__':
    engine = get_engine(**DB_SETTINGS)
    service = SurfaceService(engine)
    surface = service.get_surfaces(limit=1)[0]
    # show_current_surface(surface, AXES, PLOT, show=True)
    # cord1, cord2, cord3 =

    cord1 = Coordinate(x=0, y=0, z=1)
    cord2 = Coordinate(x=2, y=2, z=1)
    cord3 = Coordinate(x=3, y=3, z=1)

    # TODO: не работает!
    s = find_angle_between_two_planes(
        (cord1, cord2, cord3),
        surface.plane_cords[0]
    )

    print(s)
