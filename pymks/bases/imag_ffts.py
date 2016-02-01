from .abstract import _AbstractMicrostructureBasis
import numpy as np


class _ImagFFTBasis(_AbstractMicrostructureBasis):
    def __init__(self, *args, **kwargs):
        super(_ImagFFTBasis, self).__init__(*args, **kwargs)

    def _fftn(self, X, threads=1, avoid_copy=True):
        if self._pyfftw:
            return self._fftmodule.fftn(np.ascontiguousarray(X),
                                        axes=self._axes,
                                        threads=threads,
                                        planner_effort='FFTW_ESTIMATE',
                                        overwrite_input=True,
                                        avoid_copy=avoid_copy)()
        else:
            return self._fftmodule.fftn(X, axes=self._axes)

    def _ifftn(self, X, threads=1, avoid_copy=True):
        if self._pyfftw:
            return self._fftmodule.ifftn(np.ascontiguousarray(X),
                                         axes=self._axes,
                                         threads=threads,
                                         planner_effort='FFTW_ESTIMATE',
                                         overwrite_input=True,
                                         avoid_copy=avoid_copy)()
        else:
            return self._fftmodule.ifftn(X, axes=self._axes)

    def discretize(self, X):
        raise NotImplementedError

    def _pad_axes(self, X_shape, periodic_axes):
        a = np.ones(len(self._axes), dtype=float) * 1.75
        a[list(periodic_axes)] = 1
        tmp = (np.array(X_shape)[self._axes] * a).astype(int)
        return tmp
