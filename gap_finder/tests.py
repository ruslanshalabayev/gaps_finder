from unittest import TestCase

from gap_finder.coordinate import Coordinate
from gap_finder.generation import (
    build_plane_by_three_coordinates,
    build_surface,
    PLOT,
    AXES,
    DOTS_COUNT
)
from gap_finder.utils import (
    get_triangle_square_from_three_cords, is_dot_in_triangle
)


class GapFinderTestCase(TestCase):
    cord1 = Coordinate(x=0, y=0, z=1)
    cord2 = Coordinate(x=0, y=1, z=1)
    cord3 = Coordinate(x=2, y=0, z=0)
    cords = [cord1, cord2, cord3]

    normal_in_triangle = Coordinate(x=1, y=0)
    normal_not_in_triangle = Coordinate(x=10, y=0)

    def test_triangle_square(self):
        zero_square = get_triangle_square_from_three_cords(self.cord1, self.cord1, self.cord1)

        self.assertEqual(zero_square, 0)

        square = get_triangle_square_from_three_cords(self.cord1, self.cord2, self.cord3)
        self.assertEqual(square, 1)

    def test_dot_in_triangle(self):
        is_dot_in = is_dot_in_triangle(self.cords, self.normal_in_triangle)
        self.assertEqual(is_dot_in, True)

        is_dot_in = is_dot_in_triangle(self.cords, self.normal_not_in_triangle)
        self.assertEqual(is_dot_in, False)

    def test_plane_generation(self):
        x, y, z = build_plane_by_three_coordinates(*self.cords, dots_count=DOTS_COUNT)
        build_surface(AXES, x, y, z)

        # TODO: описать в документации
        # z[y coordinate ][ x coordinate]
        self.assertEqual(z[0][0], self.cord1.z)
        self.assertEqual(z[1][0], self.cord2.z)
        self.assertEqual(z[0][2], self.cord3.z)
        PLOT.show()


if __name__ == '__main__':
    GapFinderTestCase()
