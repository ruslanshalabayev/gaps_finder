from collections import namedtuple

BaseCoordinate = namedtuple('Coordinate', ['x', 'y', 'z'])


# noinspection PyInitNewSignature,PyArgumentList,PyArgumentList,PyArgumentList
class Coordinate(BaseCoordinate):
    """
    Объект для координаты от класс namedtuple BaseCoordinate.
    Удобно инициализировать и распаковывать.

    x,y,z = named tuple

    >>> x,y,z = Coordinate(y=1)
    >>> x,y,z
    (0, 1, 0)

    >>> Coordinate().x
    0

    """
    __slots__ = ()

    # noinspection PyInitNewSignature
    def __new__(cls, x=0, y=0, z=0):
        return super(Coordinate, cls).__new__(cls, x, y, z)

    def __repr__(self):
        return str((self.x, self.y, self.z))
