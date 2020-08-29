__version__ = "1.0.1"
__version_info__ = tuple(
    [
        int(num) if num.isdigit() else num
        for num in __version__.replace("-", ".", 1).split(".")
    ]
)

__title__ = "CodeDevils Website"
__author__ = "CodeDevils"
__license__ = "MIT"
__copyright__ = "Copyright 2020 CodeDevils"
