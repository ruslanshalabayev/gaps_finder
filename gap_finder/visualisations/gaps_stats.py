import numpy as np

from gap_finder.coordinate import Coordinate
from gap_finder.generation import build_plane_by_three_coordinates
from gap_finder.graphics import init_2d_graphic
from gap_finder.models import get_engine
from gap_finder.models import surface
from gap_finder.services.surfaces import SurfaceService
from gap_finder.settings import DB_SETTINGS
from gap_finder.utils import calculate_mean_and_standard_deviation

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
    _, _, _ = plot.hist(x, facecolor='g', alpha=0.75, bins=16)

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
    gaps_coordinates =[]
    tot_list=[]
    val=[0,5,55,60]
    for i in range(4):
        for surface_ in surfaces:
            gaps = surface_.meta["gaps"]
            print(gaps[val[i]].get("coordinates"),"Зазор: ",gaps[val[i]].get("value"))
            gaps_values.append((gaps[val[i]].get("value")))
            # gaps_values.extend(
            #     np.array([gap["value"] for gap in gaps])
            # )
        tot_list.append(gaps_values)
        gaps_values = []
    # print(tot_list)
    return tot_list
engine = get_engine(**DB_SETTINGS)
service = SurfaceService(engine)
surfaces = service.get_surfaces(limit=200)
a=(gather_gaps(surfaces))
build_histogram(
    a[0],
    axis=[0, 0.5, 0, 25],
    title='Распределение зазоров точки(0,0)',
    standart_deviation=calculate_mean_and_standard_deviation(a[0])[1]
)
build_histogram(
    a[1],
    axis=[0, 0.5, 0, 25],
    title='Распределение зазоров точки(5,0)',
    standart_deviation=calculate_mean_and_standard_deviation(a[1])[1]
)
build_histogram(
    a[2],
    axis=[0, 0.5, 0, 25],
    title='Распределение зазоров точки(0,5)',
    standart_deviation=calculate_mean_and_standard_deviation(a[2])[1]
)
build_histogram(
    a[3],
    axis=[0, 0.5, 0, 25],
    title='Распределение зазоров точки(5,5)',
    standart_deviation=calculate_mean_and_standard_deviation(a[3])[1]
)

