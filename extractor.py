"""
HDF5 Image Extractor using PyTables for SZIP compression support.

This module extracts images from a single HDF5 file, including those with SZIP compression
which is commonly used in scientific imaging applications.
"""

import tables
import numpy as np
from pathlib import Path
from typing import List, Optional, Union
import warnings


class H5ImageExtractor:
    """
    A class to handle extraction of images from a single HDF5 file with SZIP compression.
    
    Attributes:
        file_path (Path): Path to the HDF5 file
        total_images (int): Total number of images in the file
    """
    
    def __init__(self, file_path: Union[str, Path]):
        """
        Initialize the H5ImageExtractor.
        
        Parameters:
            file_path: Path to a specific .h5 file
        
        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the path is not a file
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        if not self.file_path.is_file():
            raise ValueError(f"Path must be a file, not a directory: {file_path}")
        
        if self.file_path.suffix.lower() != '.h5':
            warnings.warn(f"File doesn't have .h5 extension: {self.file_path}")
        
        self.total_images = 0
        
    def scan_file(self) -> int:
        """
        Scan the HDF5 file and count images.
            
        Returns:
            Number of images in the file
        """
        
        try:
            self.total_images = self._count_images_in_file(self.file_path)
            print(f"{self.file_path.name}: {self.total_images} images")
        except Exception as e:
            warnings.warn(f"Error reading {self.file_path}: {str(e)}")
            self.total_images = 0
        
        print("-" * 70)
        print(f"Total images found: {self.total_images}")
        
        return self.total_images
    
    def _count_images_in_file(self, h5_file: Path) -> int:
        """
        Count the number of images in a single HDF5 file using PyTables.
        
        Parameters:
            h5_file: Path to HDF5 file
            
        Returns:
            Number of images in the file
        """
        count = 0
        with tables.open_file(str(h5_file), mode='r') as f:
            count = self._recursive_count_arrays(f.root)
        return count
    
    def _recursive_count_arrays(self, node, count: int = 0) -> int:
        """
        Recursively count array datasets in HDF5 group.
        
        Parameters:
            node: PyTables node (Group or Array)
            count: Running count of arrays
            
        Returns:
            Total count of arrays
        """
        for child in node._f_iter_nodes():
            if isinstance(child, tables.Array):
                if len(child.shape) >= 2:
                    count += 1
            elif isinstance(child, tables.Group):
                count = self._recursive_count_arrays(child, count)
        return count
    
    def extract_images(self, n_images: Optional[int] = None) -> np.ndarray:
        """
        Extract specified number of images from the HDF5 file.
        
        Parameters:
            n_images: Number of images to extract. If None, extracts all images.
            
        Returns:
            Numpy array containing extracted images. Shape depends on whether
            images have uniform dimensions.
            
        Raises:
            ValueError: If n_images exceeds total available images
        """
        if self.total_images == 0:
            raise ValueError("No images found in file. Run scan_file() first.")
        
        if n_images is None:
            n_images = self.total_images
        
        if n_images > self.total_images:
            raise ValueError(
                f"Requested {n_images} images but only {self.total_images} available"
            )
        
        if n_images <= 0:
            raise ValueError("Number of images must be positive")
        
        print(f"\nExtracting {n_images} image(s)")
        
        images = self._extract_from_file(self.file_path, n_images)
            
        print(f"Extracted {len(images)} from {self.file_path.name}")
        
        # Try to stack into single array if shapes are compatible
        try:
            result = np.array(images)
            print(f"Output shape: {result.shape}")
            return result
        except ValueError:
            # Images have different shapes, return as list
            warnings.warn(
                "Images have inconsistent shapes. Returning as object array."
            )
            return np.array(images, dtype=object)
    
    def _extract_from_file(self, h5_file: Path, max_count: Optional[int] = None) -> List[np.ndarray]:
        """
        Extract images from a single HDF5 file using PyTables.
        
        Parameters:
            h5_file: Path to HDF5 file
            max_count: Maximum number of images to extract
            
        Returns:
            List of numpy arrays containing image data
        """
        images = []
        with tables.open_file(str(h5_file), mode='r') as f:
            self._recursive_extract_arrays(f.root, images, max_count)
        return images
    
    def _recursive_extract_arrays(self, node, images: List[np.ndarray], 
                                  max_count: Optional[int] = None):
        """
        Recursively extract array datasets from PyTables node.
        
        Parameters:
            node: PyTables node
            images: List to append extracted images to
            max_count: Maximum number of images to extract
        """
        if max_count is not None and len(images) >= max_count:
            return
        
        for child in node._f_iter_nodes():
            if max_count is not None and len(images) >= max_count:
                break
            
            if isinstance(child, tables.Array):
                if len(child.shape) >= 2:
                    try:
                        images.append(child.read())
                    except Exception as e:
                        warnings.warn(f"Could not read dataset '{child._v_pathname}': {str(e)}")
            elif isinstance(child, tables.Group):
                self._recursive_extract_arrays(child, images, max_count)
    
    def get_summary(self) -> dict:
        """
        Get summary of the scanned file and image count.
        
        Returns:
            Dictionary with summary information
        """
        return {
            'file_path': str(self.file_path),
            'total_images': self.total_images
        }


def extract_h5_images(file_path: Union[str, Path], 
                      n_images: Optional[int] = None) -> np.ndarray:
    """
    Convenience function to extract images from an HDF5 file in one call.
    
    Parameters:
        file_path: Path to a specific .h5 file
        n_images: Number of images to extract. If None, extracts all.
        
    Returns:
        Numpy array containing extracted images
    """
    extractor = H5ImageExtractor(file_path)
    extractor.scan_file()
    
    if n_images is None:
        print(f"\nNo specific count requested. Will extract all {extractor.total_images} images.")
        user_input = input("Continue? (y/n): ").strip().lower()
        if user_input != 'y':
            print("Extraction cancelled.")
            return np.array([])
    
    return extractor.extract_images(n_images)
