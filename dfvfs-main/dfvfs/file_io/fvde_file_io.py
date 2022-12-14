# -*- coding: utf-8 -*-
"""The FileVault Drive Encryption (FVDE) file-like object."""

import pyfvde

from dfvfs.file_io import file_object_io
from dfvfs.lib import errors
from dfvfs.lib import fvde_helper
from dfvfs.resolver import resolver


class FVDEFile(file_object_io.FileObjectIO):
  """File input/output (IO) object using pyfvde."""

  def _Close(self):
    """Closes the file-like object."""
    try:
      # TODO: ensure pyfvde volume object is open.
      self._file_object.close()
    except IOError:
      pass

    self._file_object = None

  def _OpenFileObject(self, path_spec):
    """Opens the file-like object defined by path specification.

    Args:
      path_spec (PathSpec): path specification.

    Returns:
      FileIO: a file-like object.

    Raises:
      PathSpecError: if the path specification is incorrect.
    """
    if not path_spec.HasParent():
      raise errors.PathSpecError(
          'Unsupported path specification without parent.')

    resolver.Resolver.key_chain.ExtractCredentialsFromPathSpec(path_spec)

    file_object = resolver.Resolver.OpenFileObject(
        path_spec.parent, resolver_context=self._resolver_context)
    fvde_volume = pyfvde.volume()
    fvde_helper.FVDEOpenVolume(
        fvde_volume, path_spec, file_object, resolver.Resolver.key_chain)
    return fvde_volume

  @property
  def is_locked(self):
    """bool: True if the volume is locked."""
    return self._file_object.is_locked()
