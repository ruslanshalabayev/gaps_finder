"""
Расчет зазоров между плоскостью и поверхностью заготовки
"""
from random import choice

import numpy as np
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from gap_finder.coordinate import Coordinate
from gap_finder.generation import build_plane_by_three_coordinates
from gap_finder.graphics import init_2d_graphic, init_3d_graphic
from gap_finder.models import get_engine
from gap_finder.models import surface
from gap_finder.services.surfaces import SurfaceService
from gap_finder.settings import DB_SETTINGS

COLORS = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
          '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
          '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
          '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
          '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
          '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
          '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
          '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
          '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
          '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF']


def get_z_of_surface_and_plane(surface_: surface):
    cord1, cord2, cord3 = surface_.plane_cords[0]
    cord1 = Coordinate(*cord1)
    cord2 = Coordinate(*cord2)
    cord3 = Coordinate(*cord3)

    _, _, z = build_plane_by_three_coordinates(
        cord1, cord2, cord3,
        dots_count=surface_.dots_count
    )

    _, _, Z = surface_.xyz_grid

    return Z, z


def build_histogram(x, axis: list, title=None, standart_deviation=None):
    """
    Строит 2d диаграмму
    :param x:
    :param axis:
    :param axis:
    :return:
    """
    plot = init_2d_graphic()

    # the histogram of the data
    _, _, _ = plot.hist(x, facecolor='g', alpha=0.75, bins=50)

    plot.xlabel('Размер зазоров')
    plot.ylabel('Количество зазоров')

    if title:
        plot.title(title)

    if standart_deviation:
        plot.axvline(x=standart_deviation)
        plot.text(
            standart_deviation * 1.5,  # на 20% левее ymax принтануть
            y=(axis[3] * 0.9),  # на 10% ниже ymax принтануть
            s=r'$\sigma=%s$' % round(standart_deviation, 8)
        )

    plot.axis(axis)
    plot.grid(True)
    plot.show()


def gather_base_cords(surfaces: list):
    """
    Собирает x,y координаты поверхностей

    :param surfaces:
    :return:
    """
    all_base_cords = []
    for surface_ in surfaces:
        cords = surface_.plane_cords[0]
        all_base_cords.append(cords)

    return all_base_cords


def build_dot_square(plt):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    currentAxis = plt.gca()
    currentAxis.add_patch(Rectangle((0, 0), 10, 10, fill=None, alpha=1))

    # Major ticks every 20, minor ticks every 5
    major_ticks = np.arange(-1, 12)
    minor_ticks = np.arange(-1, 12)

    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)

    # And a corresponding grid
    ax.grid(which='both')

    # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)


def build_bases_2d(plot, base_cords):
    color = choice(COLORS)

    for cords in base_cords[:200]:
        y, x = cords
        x.append(x[0])
        y.append(y[0])
        plot.plot(x, y, 'C3', lw=3, color=color, alpha=0.2)
        plot.scatter(x, y, s=120, alpha=0.2)

        plot.plot(x, y, 'C3', zorder=1, lw=3, color=color, alpha=0.2)
        plot.scatter(x, y, s=120, zorder=2, alpha=0.2)


def build_bases_3d_cords(
        ax,
        cord1,
        cord2,
        cord3
):
    v = np.array([
        cord1,
        cord2,
        cord3,
    ])

    ax.scatter3D(v[:, 0], v[:, 1], v[:, 2], alpha=.25)
    verts = [[v[0], v[1], v[2], v[0]]]

    ax.add_collection3d(Line3DCollection(
        verts,
        facecolors='white',
        linewidths=2,
        colors='r',
        alpha=.2)
    )


def build_nominal_plane_square():
    pass


def main():
    engine = get_engine(**DB_SETTINGS)
    service = SurfaceService(engine)
    surfaces = service.get_surfaces(limit=50)

    base_cords = gather_base_cords(surfaces)

    # plot = init_2d_graphic()

    # build_dot_square(plot)
    # build_bases_2d(plot, base_cords)

    ax, plot = init_3d_graphic()

    fig = plot.figure()
    ax = fig.add_subplot(111, projection='3d')

    v = np.array([
        (10, 0, -0.4),
        (0, 0, -0.4),
        (0, 10, -0.4),
        (10, 10, -0.4),
    ])

    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 11)
    ax.scatter3D(v[:, 0], v[:, 1], v[:, 2], alpha=.25)
    verts = [[v[0], v[1], v[2], v[3], v[0]]]

    ax.add_collection3d(Line3DCollection(
        verts,
        facecolors='white',
        linewidths=4,
        colors='b',
        alpha=.1)
    )

    for cords in base_cords:
        cord1, cord2, cord3 = cords
        build_bases_3d_cords(ax, cord1, cord2, cord3)

    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 11)
    plot.show()


if __name__ == '__main__':
    main()
