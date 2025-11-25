# Fano Plane Geometry Explorer - Module 1

## Overview

This module provides a comprehensive introduction to the **Fano plane**, the smallest projective plane with 7 points and 7 lines. This elegant mathematical structure appears throughout coding theory, quantum information, graph theory, and combinatorics.

## What is the Fano Plane?

The Fano plane is a finite projective plane of order 2 with these remarkable properties:
- **7 points** and **7 lines**
- Each line contains exactly **3 points**
- Each point lies on exactly **3 lines**
- Any two points determine a **unique line**
- Any two lines intersect at a **unique point**

It's named after Italian mathematician Gino Fano (1871-1952) who pioneered the study of finite geometries.

## Module Contents

### Python Modules

1. **`fano_geometry.py`** - Core data structures and algorithms
   - `FanoPlane` class with cyclic {1,2,4} construction
   - Incidence matrix computation
   - Point-line duality operations
   - Automorphism (symmetry) functions
   - Axiom verification

2. **`fano_visualization.py`** - Visualization tools
   - Standard triangle + circle representation
   - Circular layout
   - Cube corner projection
   - Incidence matrix heatmap
   - Animation capabilities

3. **`01_basic_fano.ipynb`** - Interactive Jupyter notebook
   - Step-by-step exploration
   - Axiom verification
   - Multiple visualizations
   - Structural queries
   - Symmetry analysis
   - Preview of coding theory connection

## Installation

```bash
# Install required packages
pip install numpy matplotlib ipywidgets jupyter

# Run the demo scripts
python fano_geometry.py      # View structure and verify axioms
python fano_visualization.py  # Generate visualizations

# Or explore interactively
jupyter notebook 01_basic_fano.ipynb
```

## Key Concepts Covered

### 1. Construction
The Fano plane is built using the **cyclic difference set {1,2,4}** over ℤ₇:
- Start with base line {0, 1, 3}
- Generate all lines by adding k (mod 7) for k = 0,1,...,6

### 2. Projective Axioms
Verify computationally that:
- P1: Two points → unique line
- P2: Two lines → unique point
- P3: Non-degenerate (4 independent points exist)

### 3. Incidence Matrix
The 7×7 matrix M where M[i,j] = 1 if point i is on line j:
- Row sums = 3 (each point on 3 lines)
- Column sums = 3 (each line has 3 points)
- M·Mᵀ = 3I + J (beautiful matrix relation!)

### 4. Symmetries
The automorphism group PSL(2,7) has order 168:
- Contains cyclic group C₇ of rotations
- Acts transitively on points and lines
- Preserves all incidence relations

### 5. Duality
Points and lines can be swapped:
- "Point on line" ↔ "Line through point"
- Results in isomorphic structure (self-dual!)

## Example Usage

```python
from fano_geometry import FanoPlane, verify_axioms
from fano_visualization import FanoVisualizer

# Create the Fano plane
fano = FanoPlane()

# Basic queries
line_idx = fano.line_through_points(0, 1)  # Find line
point = fano.intersection(0, 1)             # Find intersection
is_collinear = fano.is_collinear(0, 1, 3)  # Test collinearity

# Verify axioms
axioms = verify_axioms(fano)
print(axioms)  # All should be True!

# Visualize
viz = FanoVisualizer(fano)
viz.plot_standard()              # Classic triangle + circle
viz.plot_circular()              # All points on circle  
viz.plot_all_representations()   # Multiple views
viz.plot_incidence_matrix()      # Heatmap
```

## Visualizations Generated

The module produces several PNG files:

1. **`fano_standard.png`** - Classic representation with triangle and inscribed circle
2. **`fano_representations.png`** - Multiple layouts (standard, circular, cube, highlighted)
3. **`fano_incidence.png`** - Incidence matrix heatmap

## Connection to Coding Theory

The Fano plane is intimately connected to error-correcting codes:

- **Points** ↔ Non-zero vectors in F₂³ (3-bit binary vectors)
- **Lines** ↔ Parity check equations in Hamming(7,4) code
- **Duality** ↔ Relationship between generator and parity check matrices

This connection is explored in depth in Module 6 (Binary Codes) and Module 7 (Hamming Bridge).

## Mathematical Background

### Finite Projective Planes
The Fano plane is a projective plane of order n=2. In general:
- Order n plane has n²+n+1 points and n²+n+1 lines
- Each line has n+1 points, each point on n+1 lines
- For n=2: 7 points, 7 lines, 3 per line/point

### PSL(2,7) Automorphism Group
The symmetry group has order 168 = 7×3×8:
- Simple group (no normal subgroups except trivial)
- Acts sharply 3-transitively on 7 points
- Isomorphic to PSL(3,2) (projective linear group)

### Block Design (7,3,1)-BIBD
The Fano plane is a balanced incomplete block design:
- v = 7 points
- k = 3 points per block (line)
- λ = 1 (any two points in exactly one block)
- Also called Steiner system S(2,3,7)

## References

1. **Ed Pegg Jr.** - "The Fano Plane" (MAA Math Games, 2006)
   - https://www.mathpuzzle.com/MAA/47-Fano/mathgames_05_30_06.html

2. **John Baez** - "The Octonions" (includes Fano plane section)
   - http://math.ucr.edu/home/baez/octonions/

3. **Burkard Polster** - "The Smallest Perfect Universe"
   - Explores 15-point projective space built from Fano planes

4. **Coxeter** - "Projective Geometry" (Springer, 1992)
   - Classic reference on projective planes

## What's Next?

After mastering Module 1, continue to:

- **Module 2**: Incidence structures and the Heawood graph
- **Module 3**: Symmetries and automorphism groups (PSL(2,7))
- **Module 4**: The Heawood graph and torus embeddings
- **Module 5**: Applications (Nim, social golfer, MUBs)
- **Module 6**: Binary codes and simplex/Hamming duality
- **Module 7**: Bridge to Hamming(7,4) and Steane [[7,1,3]] codes

## Learning Objectives

By the end of this module, you should be able to:

- ✅ Define and construct the Fano plane
- ✅ Verify projective plane axioms
- ✅ Compute with the incidence matrix
- ✅ Visualize the geometry in multiple ways
- ✅ Understand point-line duality
- ✅ Apply cyclic automorphisms
- ✅ Preview connections to coding theory

## Contributing

This is part of a larger project exploring the path from Fano plane geometry to quantum error correction (Steane codes). Feedback and improvements welcome!

## License

MIT License - Feel free to use for educational purposes.

## Author

Created as part of the Fano Geometry to Steane Code educational series.
