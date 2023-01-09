from gap_finder.models import surface
import sqlalchemy as sa


class SurfaceNotFoundException(Exception):
    pass


class SurfaceService:
    def __init__(self, engine):
        self.engine = engine

    def insert_new_surface(
            self,
            xyz_grid=None,
            plane_cords=None,
            dots_count=None,
            meta=None
    ):
        if not meta:
            meta = {}

        query = surface.insert().values(
            xyz_grid=xyz_grid,
            plane_cords=plane_cords,
            dots_count=dots_count,
            plane_cords_count=len(plane_cords),
            meta=meta
        )

        self.engine.execute(query)

    def get_surfaces(self, offset: int = None, limit: int = None):
        query = sa.select([surface])

        if offset:
            query = query.offset(offset)

        if limit:
            query = query.limit(limit)

        return self.engine.execute(query).fetchall()

    def update_meta(self, surface_id, meta_to_update):
        query = sa.select(
            [
                surface.c.meta,
                surface.c.id
            ]
        ).where(
            surface.c.id == surface_id
        )

        result = self.engine.execute(query)
        meta = result.fetchone()["meta"]

        if meta is None:
            raise SurfaceNotFoundException

        meta.update(**meta_to_update)

        query = surface.update().where(
            surface.c.id == surface_id
        ).values(meta=meta)

        self.engine.execute(query)

        return True
