"""
Example usage of h5_image_tools library
"""

import sys
from pathlib import Path

# Add parent directory to path to import h5_image_tools
sys.path.insert(0, str(Path(__file__).parent.parent))

from h5_image_tools import H5ImageExtractor, extract_h5_images
import matplotlib.pyplot as plt

def example_basic(path):
    """Basic extraction example"""
    print("=" * 70)
    print("Example 1: Basic Extraction")
    print("=" * 70)
    
    data_file = Path(path)
    images = extract_h5_images(str(data_file), n_images=5)
    print(f"Extracted {len(images)} images with shape {images.shape}")
    print(f"Data range: [{images.min()}, {images.max()}]")
    print()

def example_detailed(path):
    """Detailed extraction with class"""
    print("=" * 70)
    print("Example 2: Using H5ImageExtractor Class")
    print("=" * 70)
    
    # Create extractor
    data_file = Path(path)
    extractor = H5ImageExtractor(str(data_file))
    
    # Scan file
    image_count = extractor.scan_file()
    print(f"\nImage count: {image_count}")
    
    # Get summary
    summary = extractor.get_summary()
    print(f"\nSummary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Extract images
    images = extractor.extract_images(n_images=10)
    print(f"\nExtracted images shape: {images.shape}")
    print(f"Data type: {images.dtype}")
    print()
    
    return images

def example_visualization(images):
    """Visualize extracted images"""
    print("=" * 70)
    print("Example 3: Visualizing Images")
    print("=" * 70)
    
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.ravel()
    
    for i in range(min(6, len(images))):
        axes[i].imshow(images[i], cmap='gray')
        axes[i].set_title(f'Image {i+1}')
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.show()
    print("Displaying images...")
    print()

if __name__ == "__main__":
    # Run examples with the examplary file
    example_file = Path(__file__).parent / "example_file.h5"
    
    example_basic(str(example_file))
    images = example_detailed(str(example_file))
    example_visualization(images)
    
    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
