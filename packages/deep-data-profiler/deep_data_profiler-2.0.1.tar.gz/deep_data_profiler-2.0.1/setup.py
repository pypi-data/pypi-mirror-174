from setuptools import setup, find_packages
import sys
import os.path
from pathlib import Path

__version__ = "2.0.1"

if sys.version_info < (3, 7):
    sys.exit("DeepDataProfiler requires Python 3.7 or later")

this_directory = Path(__file__).parent
long_description = (this_directory / "long_description.md").read_text()
setup(
    name="deep_data_profiler",
    packages=[
        "deep_data_profiler",
        "deep_data_profiler.classes",
        "deep_data_profiler.utils",
        "deep_data_profiler.algorithms",
        "deep_data_profiler.optimization",
    ],
    version=__version__,
    description="The Deep Data Profilerlibrary provides tools for analyzing the internal decision structure of a trained deep neural network.",
    license="3-Clause BSD license",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "torch>=1.10.2",
        "numpy>=1.14.3",
        "networkx>=2.5",
        "scipy",
        "ripser>=0.6.0",
        "powerlaw>=1.4.6",
        "torchvision>=0.11.3",
        "torch-lucent>=0.1.8",
    ],
    extras_require={
        "testing": ["pytest>=4.0"],
        "documentation": ["sphinx>=1.8.2", "nb2plots>=0.6", "sphinx-rtd-theme>=0.4.2","sphinx-autodoc-typehints",],
        "tutorials": ["pillow>=5.2.0","jupyter>=1.0.0","opencv-python","pytorchcv",],
        "frontend": ["streamlit", "boto3"],
        "all": [
            "sphinx>=1.8.2",
            "nb2plots>=0.6",
            "sphinx-rtd-theme>=0.4.2",
            "sphinx-autodoc-typehints",
            "pytest>=4.0",
            "pillow>=5.2.0",
            "jupyter>=1.0.0",
            "opencv-python",
            "pytorchcv",
            "streamlit",
            "boto3",
        ],
    },
)
