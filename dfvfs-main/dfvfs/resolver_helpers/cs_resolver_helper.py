# -*- coding: utf-8 -*-
"""The CS path specification resolver helper implementation."""

from dfvfs.file_io import cs_file_io
from dfvfs.lib import definitions
from dfvfs.resolver_helpers import manager
from dfvfs.resolver_helpers import resolver_helper
from dfvfs.vfs import cs_file_system


class CSResolverHelper(resolver_helper.ResolverHelper):
  """Logical Volume Manager (CS) resolver helper."""

  TYPE_INDICATOR = definitions.TYPE_INDICATOR_CS

  def NewFileObject(self, resolver_context, path_spec):
    """Creates a new file input/output (IO) object.

    Args:
      resolver_context (Context): resolver context.
      path_spec (PathSpec): a path specification.

    Returns:
      FileIO: file input/output (IO) object.
    """
    return cs_file_io.CSFile(resolver_context, path_spec)

  def NewFileSystem(self, resolver_context, path_spec):
    """Creates a new file system object.

    Args:
      resolver_context (Context): resolver context.
      path_spec (PathSpec): a path specification.

    Returns:
      FileSystem: file system.
    """
    return cs_file_system.CSFileSystem(resolver_context, path_spec)


manager.ResolverHelperManager.RegisterHelper(CSResolverHelper())
