import fsspec

from fsspec.core import split_protocol
from pystac.stac_io import DefaultStacIO, StacIO


class CustomIO(DefaultStacIO):
    """
    Allows PySTAC to perform IO tasks with a `fsspec` compatible file system.

    :param filesystem: (optional) `fsspec` compatible file system instance. If
        not provided, it will be inferred from the protocol.
    """
    def __init__(self, filesystem=None):
        self.filesystem = filesystem

    def _get_filesystem_for_href(self, href):
        return self.filesystem or fsspec.filesystem(split_protocol(href)[0])

    def read_text_from_href(self, href):
        """
        Read from local or remote file system.

        :param href: (str) URI where to read from.
        :return: (bytes) file content
        """
        fs = self._get_filesystem_for_href(href)
        with fs.open(href, mode="r") as f:
            text = f.read()
        return text

    def write_text_to_href(self, href, txt):
        """
        Write to local or remote file system.

        :param href: (str) URI where to write to.
        :param txt: (str) text to be written.
        """
        fs = self._get_filesystem_for_href(href)
        fs.makedirs(fs._parent(href), exist_ok=True)
        with fs.open(href, mode="w") as f:
            f.write(txt)


def set_default_stac_io():
    """
    Register CustomIO class as default IO class in PySTAC.
    """
    StacIO.set_default(CustomIO)


def configure_stac_io(filesystem=None):
    """
    Configure PySTAC to read from/write to the provided file system.

    :param filesystem: `fsspec` compatible file system instance.
    :return: StacIO instance
    """
    return CustomIO(filesystem)
