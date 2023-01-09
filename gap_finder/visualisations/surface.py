"""
Расчет зазоров между плоскостью и поверхностью заготовки
"""
import numpy as np
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from gap_finder.coordinate import Coordinate
from gap_finder.generation import build_plane_by_three_coordinates
from gap_finder.graphics import init_2d_graphic, init_3d_graphic, build_main_surface, build_surface
from gap_finder.models import get_engine
from gap_finder.models import surface
from gap_finder.services.surfaces import SurfaceService
from gap_finder.settings import DB_SETTINGS


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


def main():
    engine = get_engine(**DB_SETTINGS)
    service = SurfaceService(engine)
    surfaces = service.get_surfaces(limit=20)

    for surface in surfaces:
        AXES, PLOT = init_3d_graphic()
        show_current_surface(surface, AXES, PLOT, show=True)
        PLOT.close()


if __name__ == '__main__':
    main()
