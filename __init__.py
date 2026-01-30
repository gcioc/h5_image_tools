"""
H5 Image Tools - A library for extracting images from HDF5 files with SZIP compression support.
"""

from .extractor import H5ImageExtractor, extract_h5_images

__version__ = "1.0.0"
__all__ = ["H5ImageExtractor", "extract_h5_images"]
