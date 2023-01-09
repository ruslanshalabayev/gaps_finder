"""
Расчет зазоров между плоскостью и поверхностью заготовки
"""
import numpy as np

from gap_finder.coordinate import Coordinate
from gap_finder.generation import build_plane_by_three_coordinates
from gap_finder.models import get_engine
from gap_finder.models import surface
from gap_finder.services.surfaces import SurfaceService
from gap_finder.settings import DB_SETTINGS


def find_gaps(z_surface, z_plane):
    gaps = []
    for index, zn in np.ndenumerate(z_surface):
        yn, xn = index
        gaps.append({
            "coordinates": (xn, yn, zn),
            "value": z_surface[yn][xn] - z_plane[yn][xn]
        })

    return gaps


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


def main():
    engine = get_engine(**DB_SETTINGS)
    service = SurfaceService(engine)
    surfaces = service.get_surfaces(limit=200)

    for index, surface_ in enumerate(surfaces, start=1):
        print("Finding gaps of surface #%s" % index)
        Z, z = get_z_of_surface_and_plane(surface_)
        gaps = find_gaps(Z, z)

        service.update_meta(
            surface_.id,
            meta_to_update={
                "gaps": gaps
            }
        )


if __name__ == '__main__':
    main()
