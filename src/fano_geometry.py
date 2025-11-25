"""
Core Fano Plane Geometry Module

Defines the fundamental structure of the Fano plane, the smallest projective plane,
with 7 points and 7 lines satisfying projective axioms.
"""

import numpy as np
from typing import List, Set, Tuple, Dict
from dataclasses import dataclass


@dataclass
class FanoPlane:
    """
    The Fano plane: a finite projective plane of order 2.
    
    Properties:
    - 7 points
    - 7 lines
    - 3 points per line
    - 3 lines per point
    - Any two points determine a unique line
    - Any two lines intersect at a unique point
    """
    
    def __init__(self):
        """Initialize the Fano plane using the cyclic {1,2,4} construction."""
        self.points = list(range(7))
        
        # Define lines using the cyclic {1,2,4} mod 7 pattern
        # Start with base line {0,1,3}, then add i mod 7 to get all lines
        self.lines = [
            frozenset([0, 1, 3]),  # Line 0
            frozenset([1, 2, 4]),  # Line 1
            frozenset([2, 3, 5]),  # Line 2
            frozenset([3, 4, 6]),  # Line 3
            frozenset([4, 5, 0]),  # Line 4
            frozenset([5, 6, 1]),  # Line 5
            frozenset([6, 0, 2]),  # Line 6
        ]
        
        # Alternative standard naming (for reference)
        self.line_names = {
            0: "ABC",
            1: "BDE",
            2: "CEF",
            3: "DFG",
            4: "EGA",
            5: "FGB",
            6: "GAC"
        }
        
    def incidence_matrix(self) -> np.ndarray:
        """
        Return the point-line incidence matrix.
        Entry (i,j) is 1 if point i is on line j, 0 otherwise.
        """
        matrix = np.zeros((7, 7), dtype=int)
        for i, line in enumerate(self.lines):
            for point in line:
                matrix[point, i] = 1
        return matrix
    
    def lines_through_point(self, point: int) -> List[int]:
        """Return indices of all lines containing the given point."""
        return [i for i, line in enumerate(self.lines) if point in line]
    
    def points_on_line(self, line_idx: int) -> Set[int]:
        """Return the set of points on the given line."""
        return self.lines[line_idx]
    
    def intersection(self, line1_idx: int, line2_idx: int) -> int:
        """Return the unique point where two lines intersect."""
        intersection = self.lines[line1_idx] & self.lines[line2_idx]
        assert len(intersection) == 1, "Lines must intersect at exactly one point"
        return list(intersection)[0]
    
    def line_through_points(self, p1: int, p2: int) -> int:
        """Return the unique line containing both points."""
        for i, line in enumerate(self.lines):
            if p1 in line and p2 in line:
                return i
        raise ValueError(f"No line found through points {p1} and {p2}")
    
    def third_point(self, p1: int, p2: int) -> int:
        """Given two points, return the third point on their common line."""
        line_idx = self.line_through_points(p1, p2)
        line = self.points_on_line(line_idx)
        third = line - {p1, p2}
        return list(third)[0]
    
    def is_collinear(self, p1: int, p2: int, p3: int) -> bool:
        """Check if three points are collinear (lie on the same line)."""
        try:
            line_idx = self.line_through_points(p1, p2)
            return p3 in self.points_on_line(line_idx)
        except ValueError:
            return False
    
    def complement_line(self, line_idx: int) -> Set[int]:
        """Return the set of points NOT on the given line."""
        return set(self.points) - self.points_on_line(line_idx)
    
    def automorphism_cyclic(self, k: int) -> Dict[int, int]:
        """
        Return the cyclic automorphism that adds k (mod 7) to each point.
        This generates the cyclic group C_7 ⊂ PSL(2,7).
        """
        return {i: (i + k) % 7 for i in self.points}
    
    def apply_automorphism(self, automorphism: Dict[int, int]) -> 'FanoPlane':
        """Apply an automorphism to get a (isomorphic) Fano plane."""
        new_fano = FanoPlane()
        new_fano.lines = [
            frozenset(automorphism[p] for p in line)
            for line in self.lines
        ]
        return new_fano


def verify_axioms(fano: FanoPlane) -> Dict[str, bool]:
    """
    Verify all axioms of a projective plane hold for the Fano plane.
    
    Returns a dictionary of axiom names to boolean verification results.
    """
    axioms = {}
    
    # Axiom 1: Any two distinct points lie on exactly one line
    axiom1_holds = True
    for p1 in fano.points:
        for p2 in fano.points:
            if p1 < p2:  # Check each pair once
                lines_count = sum(1 for line in fano.lines if p1 in line and p2 in line)
                if lines_count != 1:
                    axiom1_holds = False
                    break
        if not axiom1_holds:
            break
    axioms["Two points determine unique line"] = axiom1_holds
    
    # Axiom 2: Any two distinct lines intersect at exactly one point
    axiom2_holds = True
    for i in range(len(fano.lines)):
        for j in range(i + 1, len(fano.lines)):
            intersection = fano.lines[i] & fano.lines[j]
            if len(intersection) != 1:
                axiom2_holds = False
                break
        if not axiom2_holds:
            break
    axioms["Two lines intersect at unique point"] = axiom2_holds
    
    # Axiom 3: Each line has exactly 3 points
    axiom3_holds = all(len(line) == 3 for line in fano.lines)
    axioms["Each line has 3 points"] = axiom3_holds
    
    # Axiom 4: Each point is on exactly 3 lines
    axiom4_holds = all(
        sum(1 for line in fano.lines if point in line) == 3
        for point in fano.points
    )
    axioms["Each point on 3 lines"] = axiom4_holds
    
    # Additional property: There exist 4 points, no three collinear
    # (guarantees it's not degenerate)
    found_independent_set = False
    for p1 in range(7):
        for p2 in range(p1+1, 7):
            for p3 in range(p2+1, 7):
                for p4 in range(p3+1, 7):
                    # Check no three are collinear
                    if not (fano.is_collinear(p1, p2, p3) or
                           fano.is_collinear(p1, p2, p4) or
                           fano.is_collinear(p1, p3, p4) or
                           fano.is_collinear(p2, p3, p4)):
                        found_independent_set = True
                        break
                if found_independent_set:
                    break
            if found_independent_set:
                break
        if found_independent_set:
            break
    axioms["Has 4 independent points"] = found_independent_set
    
    return axioms


def print_structure(fano: FanoPlane):
    """Print the structure of the Fano plane in a readable format."""
    print("=" * 60)
    print("FANO PLANE STRUCTURE")
    print("=" * 60)
    print(f"\nPoints: {fano.points}")
    print(f"Number of points: {len(fano.points)}")
    print(f"Number of lines: {len(fano.lines)}")
    
    print("\nLines (as sets of points):")
    for i, line in enumerate(fano.lines):
        points = sorted(list(line))
        print(f"  Line {i}: {{{points[0]}, {points[1]}, {points[2]}}}")
    
    print("\nIncidence Matrix (rows=points, cols=lines):")
    matrix = fano.incidence_matrix()
    print("   ", "  ".join(f"L{i}" for i in range(7)))
    for i, row in enumerate(matrix):
        print(f"P{i}:", "  ".join(str(x) for x in row))
    
    print("\nLines through each point:")
    for point in fano.points:
        lines = fano.lines_through_point(point)
        print(f"  Point {point}: Lines {lines}")
    
    print("\nLine intersection table:")
    print("    ", "  ".join(f"L{i}" for i in range(7)))
    for i in range(7):
        row = [fano.intersection(i, j) if i != j else "-" for j in range(7)]
        print(f"L{i}:  " + "  ".join(str(x) for x in row))
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Create and verify the Fano plane
    fano = FanoPlane()
    
    # Print structure
    print_structure(fano)
    
    # Verify axioms
    print("\nAXIOM VERIFICATION")
    print("=" * 60)
    axioms = verify_axioms(fano)
    for axiom, holds in axioms.items():
        status = "✓" if holds else "✗"
        print(f"{status} {axiom}")
    
    print("\n" + "=" * 60)
    
    # Some example queries
    print("\nEXAMPLE QUERIES")
    print("=" * 60)
    print(f"Line through points 0 and 1: Line {fano.line_through_points(0, 1)}")
    print(f"Third point on line with 0 and 1: Point {fano.third_point(0, 1)}")
    print(f"Intersection of Lines 0 and 1: Point {fano.intersection(0, 1)}")
    print(f"Points 0, 1, 3 collinear? {fano.is_collinear(0, 1, 3)}")
    print(f"Points 0, 1, 2 collinear? {fano.is_collinear(0, 1, 2)}")
    print(f"Complement of Line 0: {sorted(fano.complement_line(0))}")
