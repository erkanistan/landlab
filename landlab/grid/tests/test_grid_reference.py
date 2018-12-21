
import numpy as np
import pytest
from numpy.testing import assert_array_equal
from pytest import approx

from landlab import HexModelGrid, RadialModelGrid, RasterModelGrid

_START_REFERENCE = (10., 20.)
_MOVE_REFERENCE = (30., 45.)


def test_move_reference_raster():
    xy_of_lower_left = 1000. * (np.random.random_sample(2) - .5)

    mg = RasterModelGrid(9, 5, xy_spacing=2.0, xy_of_lower_left=xy_of_lower_left)
    assert mg.xy_of_lower_left == approx(xy_of_lower_left)
    assert mg.x_of_node.min() == approx(xy_of_lower_left[0])
    assert mg.y_of_node.min() == approx(xy_of_lower_left[1])

    xy_of_new_lower_left = 1000. * (np.random.random_sample(2) - .5)

    mg.xy_of_lower_left = xy_of_new_lower_left
    assert mg.xy_of_lower_left == approx(xy_of_new_lower_left)
    assert mg.x_of_node.min() == approx(xy_of_new_lower_left[0])
    assert mg.y_of_node.min() == approx(xy_of_new_lower_left[1])


def test_raster_lower_left_as_iterables():
    xy_of_lower_left = np.random.random_sample(2) - .5
    expected = approx(tuple(xy_of_lower_left))

    grid = RasterModelGrid(9, 5, xy_of_lower_left=xy_of_lower_left)
    assert isinstance(grid.xy_of_lower_left, tuple)
    assert grid.xy_of_lower_left == expected

    grid = RasterModelGrid(9, 5, xy_of_lower_left=tuple(xy_of_lower_left))
    assert isinstance(grid.xy_of_lower_left, tuple)
    assert grid.xy_of_lower_left == expected

    grid = RasterModelGrid(9, 5, xy_of_lower_left=list(xy_of_lower_left))
    assert isinstance(grid.xy_of_lower_left, tuple)
    assert grid.xy_of_lower_left == expected


@pytest.mark.parametrize("orientation", ["horizontal", "vertical"])
@pytest.mark.parametrize("shape", ["rect"])
@pytest.mark.parametrize("n_cols", [12, 11, 10, 9])
@pytest.mark.parametrize("n_rows", [12, 11, 10, 9])
def test_move_reference_hex(n_rows, n_cols, shape, orientation):
    _START_REFERENCE_2 = [(0., 0.), (10., 20.)]

    for xy_of_ref in ((0., 0.), (10., 20.)):
        mg = HexModelGrid(
            n_rows,
            n_cols,
            dx=2.0,
            xy_of_lower_left=xy_of_ref,
            orientation=orientation,
            shape=shape,
        )

        assert mg.xy_of_lower_left == xy_of_ref
        assert mg.x_of_node.min() == xy_of_ref[0]
        assert mg.y_of_node.min() == xy_of_ref[1]

        mg.xy_of_lower_left = (30., 45.)
        assert mg._xy_of_lower_left == (30., 45.)
        assert mg.x_of_node.min() == approx(30.)
        assert mg.y_of_node.min() == approx(45.)


def test_move_reference_radial():
    mg = RadialModelGrid(num_shells=9, dr=10., xy_of_center=_START_REFERENCE)

    assert mg._xy_of_center == _START_REFERENCE

    pre_move_llc = (mg.x_of_node.min(), mg.y_of_node.min())

    mg.xy_of_center = _MOVE_REFERENCE
    assert mg._xy_of_center == _MOVE_REFERENCE

    post_move_llc = (mg.x_of_node.min(), mg.y_of_node.min())

    actual_dydx = (
        post_move_llc[0] - pre_move_llc[0],
        post_move_llc[1] - pre_move_llc[1],
    )
    known_dydx = (
        _MOVE_REFERENCE[0] - _START_REFERENCE[0],
        _MOVE_REFERENCE[1] - _START_REFERENCE[1],
    )

    assert known_dydx == actual_dydx


def test_radial_deprecate_origin_x():
    with pytest.warns(DeprecationWarning):
        mg = RadialModelGrid(num_shells=1, dr=1., origin_x=10)
    assert mg._xy_of_center == (10., 0.)
    pts, npts = mg._create_radial_points(1, 1, xy_of_center=mg._xy_of_center)
    assert pts[0, 0] == mg._xy_of_center[0]
    assert pts[0, 1] == mg._xy_of_center[1]


def test_radial_deprecate_origin_y():
    with pytest.warns(DeprecationWarning):
        mg = RadialModelGrid(num_shells=1, dr=1., origin_y=10)
    assert mg._xy_of_center == (0., 10.)
    pts, npts = mg._create_radial_points(1, 1, xy_of_center=mg._xy_of_center)
    assert pts[0, 0] == mg._xy_of_center[0]
    assert pts[0, 1] == mg._xy_of_center[1]


def test_raster_with_args_and_shape():
    with pytest.raises(ValueError):
        RasterModelGrid(3, 3, num_cols=3)


def test_raster_with_negative_shape():
    with pytest.raises(ValueError):
        RasterModelGrid(-2, 3)


def test_raise_deprecation_dx():
    with pytest.warns(DeprecationWarning):
        mg = RasterModelGrid(3, 3, dx=3)
    X, Y = np.meshgrid([0., 3., 6.], [0., 3., 6.])
    assert_array_equal(mg.x_of_node, X.flatten())
    assert_array_equal(mg.y_of_node, Y.flatten())


def test_raise_deprecation_dxdx():
    with pytest.warns(DeprecationWarning):
        mg = RasterModelGrid(3, 3, dx=(4, 5))
    X, Y = np.meshgrid([0., 5., 10.], [0., 4., 8.])
    assert_array_equal(mg.x_of_node, X.flatten())
    assert_array_equal(mg.y_of_node, Y.flatten())


def test_raise_deprecation_spacing():
    with pytest.warns(DeprecationWarning):
        mg = RasterModelGrid(3, 3, spacing=(4, 5))
    X, Y = np.meshgrid([0., 5., 10.], [0., 4., 8.])
    assert_array_equal(mg.x_of_node, X.flatten())
    assert_array_equal(mg.y_of_node, Y.flatten())


def test_raise_deprecation_spacing_as_arg():
    with pytest.warns(DeprecationWarning):
        mg = RasterModelGrid(3, 3, 3)
    X, Y = np.meshgrid([0., 3., 6.], [0., 3., 6.])
    assert_array_equal(mg.x_of_node, X.flatten())
    assert_array_equal(mg.y_of_node, Y.flatten())


def test_raise_deprecation_spacing2_as_arg():
    with pytest.warns(DeprecationWarning):
        mg = RasterModelGrid(3, 3, (4, 5))
    X, Y = np.meshgrid([0., 5., 10.], [0., 4., 8.])
    assert_array_equal(mg.x_of_node, X.flatten())
    assert_array_equal(mg.y_of_node, Y.flatten())


def test_bad_shape_xy_spacing():
    with pytest.raises(ValueError):
        RasterModelGrid(3, 3, xy_spacing=(4, 5, 5))


def test_bad_type_xy_spacing():
    with pytest.raises(ValueError):
        RasterModelGrid(3, 3, xy_spacing="spam and eggs")


def test_deprecate_origin():
    with pytest.warns(DeprecationWarning):
        mg = RasterModelGrid(3, 3, origin=(10, 13))
    X, Y = np.meshgrid([0., 1., 2.], [0., 1., 2.])
    assert_array_equal(mg.x_of_node, X.flatten() + 10.)
    assert_array_equal(mg.y_of_node, Y.flatten() + 13.)


def test_bad_origin():
    with pytest.raises(ValueError):
        RasterModelGrid(3, 3, xy_of_lower_left=(10, 13, 12))


def test_curent_vs_past_origin():
    with pytest.warns(DeprecationWarning):
        mg1 = RasterModelGrid(3, 3, origin=(10, 13))
    mg2 = RasterModelGrid(3, 3, xy_of_lower_left=(10, 13))
    assert_array_equal(mg1.x_of_node, mg2.x_of_node)
    assert_array_equal(mg1.y_of_node, mg2.y_of_node)


def test_curent_vs_past_spacing():
    with pytest.warns(DeprecationWarning):
        mg1 = RasterModelGrid(3, 3, spacing=(5, 4))
    mg2 = RasterModelGrid(3, 3, xy_spacing=(4, 5))
    assert_array_equal(mg1.x_of_node, mg2.x_of_node)
    assert_array_equal(mg1.y_of_node, mg2.y_of_node)
