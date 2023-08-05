# Copyright 2019-2022 The kikuchipy developers
#
# This file is part of kikuchipy.
#
# kikuchipy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kikuchipy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kikuchipy. If not, see <http://www.gnu.org/licenses/>.

"""Utilities for working with a :class:`~orix.crystal_map.CrystalMap`
and an :class:`~kikuchipy.signals.EBSD` signal.
"""

import warnings

import numpy as np
from orix.crystal_map import CrystalMap


def _crystal_map_is_compatible_with_signal(
    xmap: CrystalMap, navigation_axes: tuple, raise_if_not: bool = False
) -> bool:
    """Check whether a signal's navigation axes are compatible with a
    crystal map.
    """
    nav_shape = tuple([a.size for a in navigation_axes])
    nav_scale = list([a.scale for a in navigation_axes])

    try:
        xmap_scale = list([xmap._step_sizes[a.name] for a in navigation_axes])
    except KeyError:
        warnings.warn(
            "The signal navigation axes must be named 'x' and/or 'y' in order to "
            "compare the signal navigation scale to the CrystalMap step sizes 'dx' and "
            "'dy' (see `EBSD.axes_manager`)"
        )
        xmap_scale = list(xmap._step_sizes.values())[-len(navigation_axes) :]

    compatible = xmap.shape == nav_shape
    if compatible and not np.allclose(xmap_scale, nav_scale, atol=1e-6):
        warnings.warn(
            f"The `xmap` step size(s) {xmap_scale} are different from the signal's "
            f"step size(s) {nav_scale} (see `EBSD.axes_manager`)"
        )
    if not compatible and raise_if_not:
        raise ValueError(
            f"The `xmap` shape {xmap.shape} and step size(s) {xmap_scale} are not "
            f"compatible with the signal navigation shape {nav_shape} and step size(s) "
            f"{nav_scale} (see `EBSD.axes_manager`)"
        )
    else:
        return compatible
