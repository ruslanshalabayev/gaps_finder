"""
Расчет зазоров между плоскостью и поверхностью заготовки
"""
import numpy as np

from gap_finder.coordinate import Coordinate
from gap_finder.generation import build_plane_by_three_coordinates
from gap_finder.graphics import init_2d_graphic
from gap_finder.models import get_engine
from gap_finder.models import surface
from gap_finder.services.surfaces import SurfaceService
from gap_finder.settings import DB_SETTINGS
from gap_finder.utils import calculate_mean_and_standard_deviation


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

    plot.xlabel('Размер зазоров, мм')
    plot.ylabel('Количество зазоров')

    if title:
        plot.title(title)

    if standart_deviation:
        plot.axvline(x=standart_deviation)
        plot.text(
            standart_deviation * 1.5,  # левее ymax принтануть
            y=(axis[3] * 0.9),  # ниже ymax принтануть
            s=r'$\sigma=%s$' % round(standart_deviation, 8)
        )

    plot.axis(axis)
    plot.grid(True)
    plot.show()


def gather_gaps(surfaces: list):
    """
    Берёт все значения зазоров, исключая при этом нулевые
    :param surfaces:
    :return:
    """
    gaps_values = []

    for surface_ in surfaces:
        gaps = surface_.meta["gaps"]

        gaps_values.extend(
            np.array([gap["value"] for gap in gaps if gap["value"] != 0])
        )

    return gaps_values


def build_for_one(surface_):
    gaps = gather_gaps([surface_])
    mean, deviation = calculate_mean_and_standard_deviation(gaps)
    build_histogram(
        gaps,
        axis=[0, 1, 0, 14],
        title='Распределение зазоров поверхности n=1',
        standart_deviation=deviation
    )

    print("Среднеквадратическое отклонение для n=1: %s" % deviation)
    print("Среднее значение для n=1: %s" % mean)


def build_for_all(surfaces):
    gaps = gather_gaps(surfaces)
    mean, deviation = calculate_mean_and_standard_deviation(gaps)
    build_histogram(
        gaps,
        axis=[0, 1.2, 0, 1300],
        title='Распределение зазоров поверхности n=200',
        standart_deviation=deviation
    )

    print("Среднеквадратическое отклонение для n=100: %s" % deviation)
    print("Среднее значение для n=100: %s" % mean)


def main():
    engine = get_engine(**DB_SETTINGS)
    service = SurfaceService(engine)
    surfaces = service.get_surfaces(limit=200)
    build_for_one(surfaces[0])  # build for first surface
    build_for_all(surfaces)


if __name__ == '__main__':
    main()
