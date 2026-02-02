# H5 Image Tools

A Python library for extracting images from HDF5 files, **specifically designed to handle SZIP compression**. It is designed to work for the use-case of our interest but it can be easily repurpoused for other uses.

## Why This Library?

Standard HDF5 libraries in Python (like `h5py`) often cannot read files compressed with SZIP due to:

1. **Patent restrictions**: SZIP has patent limitations that prevent it from being included in many open-source HDF5 distributions
2. **Library dependencies**: The decompression requires the SZIP library to be compiled into the HDF5 C library. 

This library uses **PyTables**, which includes pre-compiled binaries with SZIP support:
- Includes the necessary decompression codecs
- Handles various HDF5 compression formats automatically
- Provides a Pythonic interface for HDF5 data

## Required Packages

- tables 
- numpy
 
## File Structure Compatibility

This library works with HDF5 files that have:
- Nested group structures (our use-case, `ImageData/timestamp/RawImages/RawImage_00000`)
- 2D or 3D array datasets
- Various compression formats (SZIP, GZIP, LZF, etc.)
- Mixed compressed/uncompressed datasets

## Performance Notes

- PyTables reads data efficiently but may be slightly slower than h5py for uncompressed files
- For large datasets, consider extracting images in batches
- Images are loaded into memory, so ensure sufficient RAM for large extractions

## Troubleshooting

### "Images have inconsistent shapes"
- The library returns an object array if images have different dimensions
- Access individual images: `images[0], images[1], ...`

## Version

Current version: 1.0.0
