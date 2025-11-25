"""
Fano Geometry Explorer - Module 1: Basic Fano Plane

A comprehensive exploration of the Fano plane geometry, 
the smallest projective plane with 7 points and 7 lines.

This module provides the foundation for understanding the path
from elegant finite geometry to quantum error correction codes.
"""

__version__ = "1.0.0"
__author__ = "Fano Geometry Project"

from .fano_geometry import FanoPlane, verify_axioms, print_structure
from .fano_visualization import FanoVisualizer

__all__ = [
    'FanoPlane',
    'FanoVisualizer', 
    'verify_axioms',
    'print_structure',
]
