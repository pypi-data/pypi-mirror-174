"""
(*)~----------------------------------------------------------------------------------
 Pupil - eye tracking platform
 Copyright (C) 2012-2015  Pupil Labs

 Distributed under the terms of the CC BY-NC-SA License.
 License details are in the file LICENSE, distributed as part of this software.
----------------------------------------------------------------------------------~(*)
"""


# start delvewheel patch
def _delvewheel_init_patch_1_1_0():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'ndsi.libs'))
    os.add_dll_directory(libs_dir)


_delvewheel_init_patch_1_1_0()
del _delvewheel_init_patch_1_1_0
# end delvewheel patch




class CaptureError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class StreamError(CaptureError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


from ndsi.formatter import DataFormat

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version("ndsi")
except PackageNotFoundError:
    # package is not installed
    __version__ = "unknown"

__protocol_version__ = str(DataFormat.latest().version_major)


from ndsi import frame
from ndsi.network import Network
from ndsi.sensor import Sensor
from ndsi.writer import H264Writer

__all__ = ["Network", "Sensor", "H264Writer", "__version__", "frame"]