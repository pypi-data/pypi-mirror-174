import rasterio
import rioxarray

from .base import Driver


class RasterioDriver(Driver):
    """ Driver to read raster data """
    def get(self, fsspec_kwargs=None, **kwargs):
        """
        Load the raster data in a rasterio-xarray DataArray object

        :param fsspec_kwargs: (optional, dict) arguments passed to fsspec file
            system class open method
        :param kwargs: (optional, dict) arguments to be passed to open_rasterio
        :return :class:`~rioxarray.core.dataarray.DataArray`
        """
        _fsspec_kwargs = fsspec_kwargs if fsspec_kwargs is not None else {}
        with self.filesystem.open(self.uri, "rb", **_fsspec_kwargs) as f:
            with rasterio.MemoryFile(f) as f_rio:
                data_array = rioxarray.open_rasterio(f_rio, **kwargs)
                data_array.load()
        return data_array
