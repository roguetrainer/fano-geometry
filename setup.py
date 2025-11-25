"""
Setup script for Fano Geometry Explorer - Module 1
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fano-geometry-module1",
    version="1.0.0",
    author="Fano Geometry Project",
    description="Explore the Fano plane: foundation for understanding quantum error correction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fano-geometry-explorer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=6.0", "pytest-cov>=2.0"],
        "jupyter": ["jupyter>=1.0.0", "ipywidgets>=7.6.0"],
    },
    package_dir={"": "src"},
    include_package_data=True,
)
