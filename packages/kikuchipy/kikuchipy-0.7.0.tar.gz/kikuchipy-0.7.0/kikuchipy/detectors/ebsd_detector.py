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

from __future__ import annotations
from copy import deepcopy
from typing import List, Optional, Tuple, Union

from matplotlib.figure import Figure
from matplotlib.markers import MarkerStyle
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


class EBSDDetector:
    r"""An EBSD detector class storing its shape, pixel size, binning
    factor, detector tilt, sample tilt and projection center (PC) per
    pattern. Given one or multiple PCs, the detector's gnomonic
    coordinates are calculated. Uses of these include projecting Kikuchi
    bands, given a unit cell, unit cell orientation and family of
    planes, onto the detector.

    Calculation of gnomonic coordinates is based on the work by Aimo
    Winkelmann in the supplementary material to
    :cite:`britton2016tutorial`.

    Parameters
    ----------
    shape
        Number of detector rows and columns in pixels. Default is
        ``(1, 1)``.
    px_size
        Size of unbinned detector pixel in um, assuming a square
        pixel shape. Default is ``1``.
    binning
        Detector binning, i.e. how many pixels are binned into one.
        Default is ``1``, i.e. no binning.
    tilt
        Detector tilt from horizontal in degrees. Default is ``0``.
    azimuthal
        Sample tilt about the sample RD (downwards) axis. A positive
        angle means the sample normal moves towards the right
        looking from the sample to the detector. Default is ``0``.
    sample_tilt
        Sample tilt from horizontal in degrees. Default is ``70``.
    pc
        X, Y and Z coordinates of the projection/pattern centers
        (PCs), describing the location of the beam on the sample
        measured relative to the detection screen. See *Notes* for
        the definition and conversions between conventions. If
        multiple PCs are passed, they are assumed to be on the form
        ``[[x0, y0, z0], [x1, y1, z1], ...]``. Default is
        ``[0.5, 0.5, 0.5]``.
    convention
        PC convention. If not given, Bruker's convention is assumed.
        Options are ``"tsl"``/``"edax"``, ``"oxford"``, ``"bruker"``,
        ``"emsoft"``, ``"emsoft4"``, and ``"emsoft5"``. ``"emsoft"`` and
        ``"emsoft5"`` is the same convention. See *Notes* for
        conversions between conventions.

    Notes
    -----
    The pattern on the detector is always viewed *from* the detector
    *towards*  the sample. Pattern width and height is here given as
    :math:`N_x` and :math:`N_y` (possibly binned).

    The Bruker PC coordinates :math:`(x_B^*, y_B^*, z_B^*)` are defined
    in fractions of :math:`N_x`, :math:`N_y`, and :math:`N_y`,
    respectively, with :math:`x_B^*` and :math:`y_B^*` defined with
    respect to the upper left corner of the detector. These coordinates
    are used internally, called :math:`(PC_x, PC_y, PC_z)` in the rest
    of the documentation when there is no reference to Bruker
    specifically.

    The EDAX TSL PC coordinates :math:`(x_T^*, y_T^*, z_T^*)` and Oxford
    Instruments PC coordinates :math:`(x_O^*, y_O^*, z_O^*)` are
    identical and defined in fractions of :math:`N_x` with respect to
    the lower left corner of the detector.

    The EMsoft PC coordinates :math:`(x_{pc}, y_{pc})` are defined as
    number of pixels (subpixel accuracy) with respect to the center of
    the detector, with :math:`x_{pc}` towards the right and
    :math:`y_{pc}` upwards. The final PC coordinate :math:`L` is the
    detector distance in microns. Note that prior to EMsoft v5.0,
    :math:`x_{pc}` was defined towards the left.

    Given these definitions, the following is the conversion from
    TSL/Oxford to Bruker

    .. math::

        x_B^* &= x_T^*,\\
        y_B^* &= 1 - \frac{N_x}{N_y} y_T^*,\\
        z_B^* &= \frac{N_x}{N_y} z_T^*.

    The conversion from EMsoft to Bruker is given as

    .. math::

        x_B^* &= \frac{1}{2} - \frac{x_{pc}}{N_x b},\\
        y_B^* &= \frac{1}{2} - \frac{y_{pc}}{N_y b},\\
        z_B^* &= \frac{L}{N_y b \delta},

    where :math:`\delta` is the unbinned detector pixel size in
    microns, and :math:`b` is the binning factor.

    Examples
    --------
    Create an EBSD detector and plot the PC on top of a pattern

    >>> import numpy as np
    >>> import kikuchipy as kp
    >>> det = kp.detectors.EBSDDetector(
    ...     shape=(60, 60),
    ...     pc=np.ones((10, 20, 3)) * (0.421, 0.779, 0.505),
    ...     convention="edax",
    ...     px_size=70,
    ...     binning=8,
    ...     tilt=5,
    ...     sample_tilt=70,
    ... )
    >>> det
    EBSDDetector (60, 60), px_size 70 um, binning 8, tilt 5, azimuthal 0, pc (0.421, 0.221, 0.505)
    >>> det.navigation_shape
    (10, 20)
    >>> det.bounds
    array([ 0, 59,  0, 59])
    >>> det.gnomonic_bounds[0, 0]
    array([-0.83366337,  1.14653465, -1.54257426,  0.43762376])
    >>> s = kp.data.nickel_ebsd_small()
    >>> det.plot(
    ...     pattern=s.inav[0, 0].data,
    ...     coordinates="gnomonic",
    ...     draw_gnomonic_circles=True
    ... )
    """

    def __init__(
        self,
        shape: Tuple[int, int] = (1, 1),
        px_size: float = 1,
        binning: int = 1,
        tilt: float = 0,
        azimuthal: float = 0,
        sample_tilt: float = 70,
        pc: Union[np.ndarray, list, tuple] = (0.5, 0.5, 0.5),
        convention: Optional[str] = None,
    ):
        """Create an EBSD detector with a shape, pixel size, binning,
        and projection/pattern center(s) (PC(s)).
        """
        self.shape = shape
        self.px_size = px_size
        self.binning = binning
        self.tilt = tilt
        self.azimuthal = azimuthal
        self.sample_tilt = sample_tilt
        self.pc = pc
        self._set_pc_convention(convention)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__} {self.shape}, "
            f"px_size {self.px_size} um, binning {self.binning}, "
            f"tilt {self.tilt}, azimuthal {self.azimuthal}, pc {tuple(self.pc_average)}"
        )

    @property
    def specimen_scintillator_distance(self) -> float:
        """Return the specimen to scintillator distance, known in EMsoft
        as :math:`L`.
        """
        return self.pcz * self.height

    @property
    def nrows(self) -> int:
        """Return the number of detector pixel rows."""
        return self.shape[0]

    @property
    def ncols(self) -> int:
        """Return the number of detector pixel columns."""
        return self.shape[1]

    @property
    def size(self) -> int:
        """Return the number of detector pixels."""
        return self.nrows * self.ncols

    @property
    def height(self) -> float:
        """Return the detector height in microns."""
        return self.nrows * self.px_size * self.binning

    @property
    def width(self) -> float:
        """Return the detector width in microns."""
        return self.ncols * self.px_size * self.binning

    @property
    def aspect_ratio(self) -> float:
        """Return the number of detector columns divided by rows."""
        return self.ncols / self.nrows

    @property
    def unbinned_shape(self) -> Tuple[int, int]:
        """Return the unbinned detector shape in pixels."""
        return tuple(np.array(self.shape) * self.binning)

    @property
    def px_size_binned(self) -> float:
        """Return the binned pixel size in microns."""
        return self.px_size * self.binning

    @property
    def pc(self) -> np.ndarray:
        """Return or set all projection center coordinates.

        Parameters
        ----------
        value : numpy.ndarray, list or tuple
            Projection center coordinates. If multiple PCs are passed,
            they are assumed to be on the form ``[[x0, y0, z0],
            [x1, y1, z1], ...]``. Default is ``[[0.5, 0.5, 0.5]]``.
        """
        return self._pc

    @pc.setter
    def pc(self, value: Union[np.ndarray, List, Tuple]):
        """Set all projection center coordinates."""
        self._pc = np.atleast_2d(value)

    @property
    def pcx(self) -> np.ndarray:
        """Return or set the projection center x coordinates.

        Parameters
        ----------
        value : numpy.ndarray, list, tuple or float
            Projection center x coordinates. If multiple x coordinates
            are passed, they are assumed to be on the form
            ``[x0, x1,...]``.
        """
        return self.pc[..., 0]

    @pcx.setter
    def pcx(self, value: Union[np.ndarray, list, tuple, float]):
        """Set the x projection center coordinates."""
        self._pc[..., 0] = np.atleast_2d(value)

    @property
    def pcy(self) -> np.ndarray:
        """Return or set the projection center y coordinates.

        Parameters
        ----------
        value : numpy.ndarray, list, tuple or float
            Projection center y coordinates. If multiple y coordinates
            are passed, they are assumed to be on the form
            ``[y0, y1,...]``.
        """
        return self.pc[..., 1]

    @pcy.setter
    def pcy(self, value: Union[np.ndarray, list, tuple, float]):
        """Set y projection center coordinates."""
        self._pc[..., 1] = np.atleast_2d(value)

    @property
    def pcz(self) -> np.ndarray:
        """Return or set the projection center z coordinates.

        Parameters
        ----------
        value : numpy.ndarray, list, tuple or float
            Projection center z coordinates. If multiple z coordinates
            are passed, they are assumed to be on the form
            ``[z0, z1,...]``.
        """
        return self.pc[..., 2]

    @pcz.setter
    def pcz(self, value: Union[np.ndarray, list, tuple, float]):
        """Set z projection center coordinates."""
        self._pc[..., 2] = np.atleast_2d(value)

    @property
    def pc_average(self) -> np.ndarray:
        """Return the overall average projection center."""
        ndim = self.pc.ndim
        axis = ()
        if ndim == 2:
            axis += (0,)
        elif ndim == 3:
            axis += (0, 1)
        return np.nanmean(self.pc, axis=axis).round(3)

    @property
    def navigation_shape(self) -> tuple:
        """Return or set the navigation shape of the projection center
        array.

        Parameters
        ----------
        value : tuple
            Navigation shape, with a maximum dimension of 2.
        """
        return self.pc.shape[: self.pc.ndim - 1]

    @navigation_shape.setter
    def navigation_shape(self, value: tuple):
        """Set the navigation shape of the projection center array."""
        ndim = len(value)
        if ndim > 2:
            raise ValueError(f"A maximum dimension of 2 is allowed, 2 < {ndim}")
        else:
            self.pc = self.pc.reshape(value + (3,))

    @property
    def navigation_dimension(self) -> int:
        """Return the number of navigation dimensions of the projection
        center array (a maximum of 2).
        """
        return len(self.navigation_shape)

    @property
    def bounds(self) -> np.ndarray:
        """Return the detector bounds ``[x0, x1, y0, y1]`` in pixel
        coordinates.
        """
        return np.array([0, self.ncols - 1, 0, self.nrows - 1])

    @property
    def x_min(self) -> Union[np.ndarray, float]:
        """Return the left bound of detector in gnomonic coordinates."""
        return -self.aspect_ratio * (self.pcx / self.pcz)

    @property
    def x_max(self) -> Union[np.ndarray, float]:
        """Return the right bound of detector in gnomonic coordinates."""
        return self.aspect_ratio * (1 - self.pcx) / self.pcz

    @property
    def x_range(self) -> np.ndarray:
        """Return the x detector limits in gnomonic coordinates."""
        return np.dstack((self.x_min, self.x_max)).reshape(self.navigation_shape + (2,))

    @property
    def y_min(self) -> Union[np.ndarray, float]:
        """Return the top bound of detector in gnomonic coordinates."""
        return -(1 - self.pcy) / self.pcz

    @property
    def y_max(self) -> Union[np.ndarray, float]:
        """Return the bottom bound of detector in gnomonic coordinates."""
        return self.pcy / self.pcz

    @property
    def y_range(self) -> np.ndarray:
        """Return the y detector limits in gnomonic coordinates."""
        return np.dstack((self.y_min, self.y_max)).reshape(self.navigation_shape + (2,))

    @property
    def gnomonic_bounds(self) -> np.ndarray:
        """Return the detector bounds ``[x0, x1, y0, y1]`` in gnomonic
        coordinates.
        """
        return np.concatenate((self.x_range, self.y_range), axis=-1)

    @property
    def _average_gnomonic_bounds(self) -> np.ndarray:
        return np.nanmean(
            self.gnomonic_bounds, axis=(0, 1, 2)[: self.navigation_dimension]
        )

    @property
    def x_scale(self) -> np.ndarray:
        """Return the width of a pixel in gnomonic coordinates."""
        if self.ncols == 1:
            x_scale = np.diff(self.x_range)
        else:
            x_scale = np.diff(self.x_range) / (self.ncols - 1)
        return x_scale.reshape(self.navigation_shape)

    @property
    def y_scale(self) -> np.ndarray:
        """Return the height of a pixel in gnomonic coordinates."""
        if self.nrows == 1:
            y_scale = np.diff(self.y_range)
        else:
            y_scale = np.diff(self.y_range) / (self.nrows - 1)
        return y_scale.reshape(self.navigation_shape)

    @property
    def r_max(self) -> np.ndarray:
        """Return the maximum distance from PC to detector edge in
        gnomonic coordinates.
        """
        corners = np.zeros(self.navigation_shape + (4,))
        corners[..., 0] = self.x_min**2 + self.y_min**2  # Up. left
        corners[..., 1] = self.x_max**2 + self.y_min**2  # Up. right
        corners[..., 2] = self.x_max**2 + self.y_max**2  # Lo. right
        corners[..., 3] = self.x_min**2 + self.y_min**2  # Lo. left
        return np.atleast_2d(np.sqrt(np.max(corners, axis=-1)))

    def pc_emsoft(self, version: int = 5) -> np.ndarray:
        r"""Return PC in the EMsoft convention.

        Parameters
        ----------
        version
            Which EMsoft PC convention to use. The direction of the x PC
            coordinate, :math:`x_{pc}`, flipped in version 5.

        Returns
        -------
        new_pc
            PC in the EMsoft convention.

        Notes
        -----
        The PC coordinate conventions of Bruker, EDAX TSL, Oxford
        Instruments and EMsoft are given in the class description. The
        PC is stored in the Bruker convention internally, so the
        conversion is

        .. math::

            x_{pc} &= N_x b \left(\frac{1}{2} - x_B^*\right),\\
            y_{pc} &= N_y b \left(\frac{1}{2} - y_B^*\right),\\
            L &= N_y b \delta z_B^*,

        where :math:`N_x` and :math:`N_y` are number of detector columns
        and rows, :math:`b` is binning, :math:`\delta` is the unbinned
        pixel size, :math:`(x_B^*, y_B^*, z_B^*)` are the Bruker PC
        coordinates, and :math:`(x_{pc}, y_{pc}, L)` are the returned
        EMsoft PC coordinates.

        Examples
        --------
        >>> import kikuchipy as kp
        >>> det = kp.detectors.EBSDDetector(
        ...     shape=(60, 80),
        ...     pc=(0.4, 0.2, 0.6),
        ...     convention="bruker",
        ...     px_size=59.2,
        ...     binning=8,
        ... )
        >>> det.pc_emsoft()
        array([[   64. ,   144. , 17049.6]])
        >>> det.pc_emsoft(4)
        array([[  -64. ,   144. , 17049.6]])
        """
        return self._pc_bruker2emsoft(version=version)

    def pc_bruker(self) -> np.ndarray:
        """Return PC in the Bruker convention, given in the class
        description.

        Returns
        -------
        new_pc
            PC in the Bruker convention.
        """
        return self.pc

    def pc_tsl(self) -> np.ndarray:
        r"""Return PC in the EDAX TSL convention.

        Returns
        -------
        new_pc
            PC in the EDAX TSL convention.

        Notes
        -----
        The PC coordinate conventions of Bruker, EDAX TSL, Oxford
        Instruments and EMsoft are given in the class description. The
        PC is stored in the Bruker convention internally, so the
        conversion is

        .. math::

            x_T^* &= x_B^*,\\
            y_T^* &= \frac{N_y}{N_x} (1 - y_B^*),\\
            z_T^* &= \frac{N_y}{N_x} z_B^*,

        where :math:`N_x` and :math:`N_y` are number of detector columns
        and rows, :math:`(x_B^*, y_B^*, z_B^*)` are the Bruker PC
        coordinates, and :math:`(x_T^*, y_T^*, z_T^*)` are the returned
        EDAX TSL PC coordinates.

        Examples
        --------
        >>> import kikuchipy as kp
        >>> det = kp.detectors.EBSDDetector(
        ...     shape=(60, 80),
        ...     pc=(0.4, 0.2, 0.6),
        ...     convention="bruker",
        ... )
        >>> det.pc_tsl()
        array([[0.4 , 0.6 , 0.45]])
        """
        return self._pc_bruker2tsl()

    def pc_oxford(self) -> np.ndarray:
        """Return PC in the Oxford convention.

        Returns
        -------
        new_pc
            PC in the Oxford convention.

        Notes
        -----
        The Oxford PC coordinates are identical to the TSL coordinates,
        see :meth:`pc_tsl`.
        """
        return self._pc_bruker2tsl()

    def deepcopy(self) -> EBSDDetector:
        """Return a deep copy using :func:`copy.deepcopy`.

        Returns
        -------
        detector
            Identical detector without shared memory.
        """
        return deepcopy(self)

    def plot(
        self,
        coordinates: str = "detector",
        show_pc: bool = True,
        pc_kwargs: Optional[dict] = None,
        pattern: Optional[np.ndarray] = None,
        pattern_kwargs: Optional[dict] = None,
        draw_gnomonic_circles: bool = False,
        gnomonic_angles: Union[None, list, np.ndarray] = None,
        gnomonic_circles_kwargs: Optional[dict] = None,
        zoom: float = 1,
        return_figure: bool = False,
    ) -> Union[None, Figure]:
        """Plot the detector screen.

        The plotting of gnomonic circles and general style is adapted
        from the supplementary material to :cite:`britton2016tutorial`
        by Aimo Winkelmann.

        Parameters
        ----------
        coordinates
            Which coordinates to use, ``"detector"`` (default) or
            ``"gnomonic"``.
        show_pc
            Show the average projection center in the Bruker convention.
            Default is ``True``.
        pc_kwargs
            A dictionary of keyword arguments passed to
            :meth:`matplotlib.axes.Axes.scatter`.
        pattern
            A pattern to put on the detector. If not given, no pattern
            is displayed. The pattern array must have the same shape as
            the detector.
        pattern_kwargs
            A dictionary of keyword arguments passed to
            :meth:`matplotlib.axes.Axes.imshow`.
        draw_gnomonic_circles
            Draw circles for angular distances from pattern. Default is
            ``False``. Circle positions are only correct when
            ``coordinates="gnomonic"``.
        gnomonic_angles
            Which angular distances to plot if
            ``draw_gnomonic_circles=True``. Default is from 10 to 80 in
            steps of 10.
        gnomonic_circles_kwargs
            A dictionary of keyword arguments passed to
            :meth:`matplotlib.patches.Circle`.
        zoom
            Whether to zoom in/out from the detector, e.g. to show the
            extent of the gnomonic projection circles. A zoom > 1 zooms
            out. Default is ``1``, i.e. no zoom.
        return_figure
            Whether to return the figure. Default is False.

        Returns
        -------
        fig
            Matplotlib figure instance, if `return_figure` is True.

        Examples
        --------
        >>> import kikuchipy as kp
        >>> det = kp.detectors.EBSDDetector(
        ...     shape=(60, 60),
        ...     pc=(0.4, 0.8, 0.5),
        ...     convention="tsl",
        ...     sample_tilt=70,
        ... )
        >>> det.plot()

        Plot with gnomonic coordinates and circles

        >>> det.plot(
        ...     coordinates="gnomonic",
        ...     draw_gnomonic_circles=True,
        ...     gnomonic_circles_kwargs={"edgecolor": "b", "alpha": 0.3}
        ... )

        Plot a pattern on the detector and save it

        >>> s = kp.data.nickel_ebsd_small()
        >>> fig = det.plot(pattern=s.inav[0, 0].data, return_figure=True)
        >>> # fig.savefig("detector.png")
        """
        sy, sx = self.shape
        pcx, pcy = self.pc_average[:2]

        if coordinates == "detector":
            pcy *= sy - 1
            pcx *= sx - 1
            bounds = self.bounds
            bounds[2:] = bounds[2:][::-1]
            x_label = "x detector"
            y_label = "y detector"
        else:
            pcy, pcx = (0, 0)
            bounds = self._average_gnomonic_bounds
            x_label = "x gnomonic"
            y_label = "y gnomonic"

        fig, ax = plt.subplots()
        ax.axis(zoom * bounds)
        ax.set_aspect("equal")
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        # Plot a pattern on the detector
        if isinstance(pattern, np.ndarray):
            if pattern.shape != (sy, sx):
                raise ValueError(
                    f"Pattern shape {pattern.shape} must equal the detector "
                    f"shape {(sy, sx)}"
                )
            if pattern_kwargs is None:
                pattern_kwargs = {}
            pattern_kwargs.setdefault("cmap", "gray")
            ax.imshow(pattern, extent=bounds, **pattern_kwargs)
        else:
            origin = (bounds[0], bounds[2])
            width = np.diff(bounds[:2])[0]
            height = np.diff(bounds[2:])[0]
            ax.add_artist(
                mpatches.Rectangle(origin, width, height, fc=(0.5,) * 3, zorder=-1)
            )

        # Show the projection center
        if show_pc:
            if pc_kwargs is None:
                pc_kwargs = {}
            default_params_pc = dict(
                s=300,
                facecolor="gold",
                edgecolor="k",
                marker=MarkerStyle(marker="*", fillstyle="full"),
                zorder=10,
            )
            _ = [pc_kwargs.setdefault(k, v) for k, v in default_params_pc.items()]
            ax.scatter(x=pcx, y=pcy, **pc_kwargs)

        # Draw gnomonic circles centered on the projection center
        if draw_gnomonic_circles:
            if gnomonic_circles_kwargs is None:
                gnomonic_circles_kwargs = {}
            default_params_gnomonic = {
                "alpha": 0.4,
                "edgecolor": "k",
                "facecolor": "None",
                "linewidth": 3,
            }
            [
                gnomonic_circles_kwargs.setdefault(k, v)
                for k, v in default_params_gnomonic.items()
            ]
            if gnomonic_angles is None:
                gnomonic_angles = np.arange(1, 9) * 10
            for angle in gnomonic_angles:
                ax.add_patch(
                    plt.Circle(
                        (pcx, pcy), np.tan(np.deg2rad(angle)), **gnomonic_circles_kwargs
                    )
                )

        if return_figure:
            return fig

    # ------------------------ Private methods ----------------------- #

    def _set_pc_convention(self, convention: Optional[str] = None):
        if convention is None or convention.lower() == "bruker":
            pass
        elif convention.lower() in ["tsl", "edax", "amatek"]:
            self.pc = self._pc_tsl2bruker()
        elif convention.lower() == "oxford":
            self.pc = self._pc_tsl2bruker()
        elif convention.lower() in ["emsoft", "emsoft4", "emsoft5"]:
            try:
                version = int(convention[-1])
            except ValueError:
                version = 5
            self.pc = self._pc_emsoft2bruker(version=version)
        else:
            conventions = [
                "bruker",
                "emsoft",
                "emsoft4",
                "emsoft5",
                "oxford",
                "tsl",
            ]
            raise ValueError(
                f"Projection center convention '{convention}' not among the "
                f"recognised conventions {conventions}."
            )

    def _pc_emsoft2bruker(self, version: int = 5) -> np.ndarray:
        new_pc = np.zeros_like(self.pc, dtype=float)
        pcx = self.pcx
        if version < 5:
            pcx = -pcx
        new_pc[..., 0] = 0.5 - (pcx / (self.ncols * self.binning))
        new_pc[..., 1] = 0.5 - (self.pcy / (self.nrows * self.binning))
        new_pc[..., 2] = self.pcz / (self.nrows * self.binning * self.px_size)
        return new_pc

    def _pc_tsl2bruker(self) -> np.ndarray:
        new_pc = deepcopy(self.pc)
        new_pc[..., 1] = 1 - self.pcy * self.aspect_ratio
        new_pc[..., 2] *= self.aspect_ratio
        return new_pc

    def _pc_bruker2emsoft(self, version: int = 5) -> np.ndarray:
        new_pc = np.zeros_like(self.pc, dtype=float)
        new_pc[..., 0] = (0.5 - self.pcx) * self.ncols * self.binning
        if version < 5:
            new_pc[..., 0] = -new_pc[..., 0]
        new_pc[..., 1] = (0.5 - self.pcy) * self.nrows * self.binning
        new_pc[..., 2] = self.pcz * self.nrows * self.binning * self.px_size
        return new_pc

    def _pc_bruker2tsl(self) -> np.ndarray:
        new_pc = deepcopy(self.pc)
        new_pc[..., 1] = (1 - self.pcy) / self.aspect_ratio
        new_pc[..., 2] /= self.aspect_ratio
        return new_pc
