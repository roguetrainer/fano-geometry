# Fano Geometry Explorer - Module 1

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the demos
cd src
python fano_geometry.py
python fano_visualization.py

# Run tests
cd ../tests
python test_fano.py

# Explore interactively
cd ../notebooks
jupyter notebook 01_basic_fano.ipynb
```

## Project Structure

```
fano-geometry-module1/
├── README.md                 # This file - quick overview
├── requirements.txt          # Python dependencies
│
├── src/                      # Source code
│   ├── __init__.py          # Package initialization
│   ├── fano_geometry.py     # Core Fano plane implementation
│   └── fano_visualization.py # Visualization tools
│
├── notebooks/                # Interactive tutorials
│   └── 01_basic_fano.ipynb  # Complete learning notebook
│
├── tests/                    # Test suites
│   └── test_fano.py         # Comprehensive tests
│
├── visualizations/           # Generated images
│   ├── fano_standard.png
│   ├── fano_representations.png
│   └── fano_incidence.png
│
└── docs/                     # Documentation
    ├── README.md            # Detailed documentation
    ├── QUICKSTART.md        # Fast start guide
    └── ROADMAP.md           # Complete project roadmap
```

## What is the Fano Plane?

The **Fano plane** is the smallest projective plane:
- 7 points and 7 lines
- Each line contains exactly 3 points
- Each point lies on exactly 3 lines
- Any two points determine a unique line
- Any two lines intersect at a unique point

Named after Italian mathematician Gino Fano (1871-1952).

## Why Study It?

The Fano plane is the geometric foundation for:
- **Hamming (7,4) code** - Perfect error-correcting code
- **Steane [[7,1,3]] code** - Quantum error correction
- Graph theory (Heawood graph)
- Combinatorics (Steiner systems)
- Finite geometry

## Key Features

### Core Implementation
- `FanoPlane` class with complete API
- Cyclic {1,2,4} construction
- Incidence matrix computation
- Automorphism group operations
- Axiom verification

### Visualizations
- Standard triangle + inscribed circle
- Circular layout
- Cube corner projection  
- Incidence matrix heatmap

### Interactive Learning
- Jupyter notebook with step-by-step exploration
- Multiple code examples
- Exercises for practice

## Documentation

- **docs/README.md** - Comprehensive technical documentation
- **docs/QUICKSTART.md** - Quick start with code examples
- **docs/ROADMAP.md** - Complete 7-module series roadmap

## Next Steps

After mastering Module 1:
- Module 2: Incidence structures & Heawood graph
- Module 3: Symmetries (PSL(2,7))
- Module 4-5: Applications and embeddings
- Module 6-7: Path to Hamming and Steane codes

## Requirements

- Python 3.8+
- NumPy
- Matplotlib
- Jupyter

See `requirements.txt` for exact versions.

## License

MIT License - Free for educational use.

## Getting Help

1. Start with `docs/QUICKSTART.md`
2. Work through `notebooks/01_basic_fano.ipynb`
3. Read `docs/README.md` for deep dive
4. Check `docs/ROADMAP.md` for the bigger picture

Enjoy exploring the beautiful mathematics of the Fano plane!
