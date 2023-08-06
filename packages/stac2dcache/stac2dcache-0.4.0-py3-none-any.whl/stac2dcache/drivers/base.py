import fsspec

from abc import ABC, abstractmethod

from fsspec.core import split_protocol


class Driver(ABC):
    """ Driver base class """
    def __init__(self, uri):
        """

        :param uri: URI of the asset to be loaded
        """
        self.uri = uri
        self.filesystem = None

    def set_filesystem(self, filesystem=None):
        """
        Configure driver authentication

        :param filesystem: (optional, `fsspec` compatible FileSystem instance)
            file system associated to the driver. If not specified it will be
            inferred from the protocol.
        """
        self.filesystem = filesystem or \
            fsspec.filesystem(split_protocol(self.uri)[0])

    @abstractmethod
    def get(self, **kwargs):
        """
        Load and return the asset

        :param kwargs: driver-specific arguments
        :return asset
        """
        return
