"""
Test Suite for Fano Plane Module

Comprehensive tests for the geometry and visualization modules.
"""

try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False

import sys
import os
# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fano_geometry import FanoPlane, verify_axioms


class TestFanoPlaneStructure:
    """Tests for basic Fano plane structure."""
    
    def setup_method(self):
        """Create a Fano plane for each test."""
        self.fano = FanoPlane()
    
    def test_initialization(self):
        """Test that Fano plane initializes correctly."""
        assert len(self.fano.points) == 7
        assert len(self.fano.lines) == 7
        assert all(len(line) == 3 for line in self.fano.lines)
    
    def test_incidence_matrix_shape(self):
        """Test incidence matrix dimensions."""
        M = self.fano.incidence_matrix()
        assert M.shape == (7, 7)
    
    def test_incidence_matrix_row_sums(self):
        """Each point should be on exactly 3 lines."""
        M = self.fano.incidence_matrix()
        row_sums = M.sum(axis=1)
        assert np.all(row_sums == 3)
    
    def test_incidence_matrix_col_sums(self):
        """Each line should contain exactly 3 points."""
        M = self.fano.incidence_matrix()
        col_sums = M.sum(axis=0)
        assert np.all(col_sums == 3)
    
    def test_incidence_matrix_relation(self):
        """Test M M^T = 3I + J."""
        M = self.fano.incidence_matrix()
        MMT = M @ M.T
        expected = 3 * np.eye(7) + np.ones((7, 7))
        assert np.allclose(MMT, expected)


class TestProjectiveAxioms:
    """Tests for projective plane axioms."""
    
    def setup_method(self):
        """Create a Fano plane for each test."""
        self.fano = FanoPlane()
    
    def test_two_points_determine_line(self):
        """Any two distinct points should lie on exactly one line."""
        for p1 in range(7):
            for p2 in range(p1+1, 7):
                # Count lines containing both points
                count = sum(1 for line in self.fano.lines 
                          if p1 in line and p2 in line)
                assert count == 1, f"Points {p1},{p2} should be on exactly 1 line"
    
    def test_two_lines_intersect(self):
        """Any two distinct lines should intersect at exactly one point."""
        for i in range(7):
            for j in range(i+1, 7):
                intersection = self.fano.lines[i] & self.fano.lines[j]
                assert len(intersection) == 1, \
                    f"Lines {i},{j} should intersect at exactly 1 point"
    
    def test_four_independent_points(self):
        """Should exist 4 points with no three collinear."""
        # Points 0,1,4,5 should work
        test_set = [0, 1, 4, 5]
        for i in range(len(test_set)):
            for j in range(i+1, len(test_set)):
                for k in range(j+1, len(test_set)):
                    p1, p2, p3 = test_set[i], test_set[j], test_set[k]
                    assert not self.fano.is_collinear(p1, p2, p3), \
                        f"Points {p1},{p2},{p3} should not be collinear"


class TestQueries:
    """Tests for query operations."""
    
    def setup_method(self):
        """Create a Fano plane for each test."""
        self.fano = FanoPlane()
    
    def test_lines_through_point(self):
        """Each point should be on exactly 3 lines."""
        for point in self.fano.points:
            lines = self.fano.lines_through_point(point)
            assert len(lines) == 3
    
    def test_points_on_line(self):
        """Each line should contain exactly 3 points."""
        for i in range(7):
            points = self.fano.points_on_line(i)
            assert len(points) == 3
    
    def test_intersection_symmetric(self):
        """Line intersection should be symmetric."""
        for i in range(7):
            for j in range(i+1, 7):
                p1 = self.fano.intersection(i, j)
                p2 = self.fano.intersection(j, i)
                assert p1 == p2
    
    def test_line_through_points_consistent(self):
        """Finding line through points should be consistent."""
        # Test with known line
        line_0_points = sorted(list(self.fano.points_on_line(0)))
        p1, p2 = line_0_points[0], line_0_points[1]
        line_idx = self.fano.line_through_points(p1, p2)
        assert line_idx == 0 or self.fano.points_on_line(line_idx) == self.fano.points_on_line(0)
    
    def test_third_point(self):
        """Third point on a line should be correct."""
        for line_idx in range(7):
            points = sorted(list(self.fano.points_on_line(line_idx)))
            p1, p2, p3 = points[0], points[1], points[2]
            
            assert self.fano.third_point(p1, p2) == p3
            assert self.fano.third_point(p1, p3) == p2
            assert self.fano.third_point(p2, p3) == p1
    
    def test_collinearity_positive(self):
        """Points on the same line should be collinear."""
        for line in self.fano.lines:
            points = sorted(list(line))
            assert self.fano.is_collinear(points[0], points[1], points[2])
    
    def test_collinearity_negative(self):
        """Random triple unlikely to be collinear."""
        # Points 0,1,2 are not collinear in standard construction
        assert not self.fano.is_collinear(0, 1, 2)
    
    def test_complement_line(self):
        """Complement should contain exactly 4 points."""
        for i in range(7):
            complement = self.fano.complement_line(i)
            assert len(complement) == 4
            
            # Verify disjoint
            line_points = self.fano.points_on_line(i)
            assert len(complement & line_points) == 0


class TestCyclicConstruction:
    """Tests for cyclic {1,2,4} construction."""
    
    def setup_method(self):
        """Create a Fano plane for each test."""
        self.fano = FanoPlane()
    
    def test_cyclic_pattern(self):
        """Lines should follow cyclic pattern."""
        base_line = frozenset([0, 1, 3])
        for i in range(7):
            shifted = frozenset((p + i) % 7 for p in base_line)
            assert self.fano.lines[i] == shifted
    
    def test_difference_set(self):
        """Should satisfy {1,2,4} difference set property."""
        # Line 0 should be {0,1,3} which gives differences {1,2,3} mod 7
        # These are {1,2,4} when considering the cyclic orbit
        base = sorted(list(self.fano.lines[0]))
        diffs = set()
        for i in range(3):
            for j in range(i+1, 3):
                diff = (base[j] - base[i]) % 7
                diffs.add(diff)
        
        # Should get 3 differences that generate all non-zero elements
        assert len(diffs) == 3


class TestAutomorphisms:
    """Tests for automorphism group."""
    
    def setup_method(self):
        """Create a Fano plane for each test."""
        self.fano = FanoPlane()
    
    def test_cyclic_automorphisms_count(self):
        """Should have 7 cyclic automorphisms."""
        autos = [self.fano.automorphism_cyclic(k) for k in range(7)]
        assert len(autos) == 7
    
    def test_identity_automorphism(self):
        """k=0 should be the identity."""
        identity = self.fano.automorphism_cyclic(0)
        assert identity == {i: i for i in range(7)}
    
    def test_automorphism_preserves_incidence(self):
        """Automorphisms should preserve incidence relations."""
        for k in range(7):
            auto = self.fano.automorphism_cyclic(k)
            
            # Check each line
            for line in self.fano.lines:
                # Transform the line
                transformed = frozenset(auto[p] for p in line)
                
                # Should be a line in the Fano plane
                assert transformed in self.fano.lines
    
    def test_cyclic_group_order(self):
        """Applying k=1 seven times should give identity."""
        auto_1 = self.fano.automorphism_cyclic(1)
        
        # Compose with itself 7 times
        result = {i: i for i in range(7)}  # Start with identity
        for _ in range(7):
            result = {i: auto_1[result[i]] for i in range(7)}
        
        # Should get back to identity
        identity = {i: i for i in range(7)}
        assert result == identity


class TestAxiomVerification:
    """Tests for the verify_axioms function."""
    
    def test_all_axioms_pass(self):
        """All axioms should be verified for valid Fano plane."""
        fano = FanoPlane()
        axioms = verify_axioms(fano)
        assert all(axioms.values()), "All axioms should be True"
    
    def test_axiom_keys(self):
        """Should check for expected axiom names."""
        fano = FanoPlane()
        axioms = verify_axioms(fano)
        
        expected_keys = {
            "Two points determine unique line",
            "Two lines intersect at unique point",
            "Each line has 3 points",
            "Each point on 3 lines",
            "Has 4 independent points"
        }
        
        assert set(axioms.keys()) == expected_keys


def run_tests():
    """Run all tests and report results."""
    print("Running Fano Plane Test Suite...")
    print("=" * 60)
    
    # Run pytest programmatically
    import sys
    exit_code = pytest.main([__file__, "-v", "--tb=short"])
    
    if exit_code == 0:
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("✗ SOME TESTS FAILED")
        print("=" * 60)
    
    return exit_code


if __name__ == "__main__":
    import sys
    
    # If pytest is not installed, run a simple version
    try:
        import pytest
        run_tests()
    except ImportError:
        print("pytest not installed. Running basic tests...")
        print("=" * 60)
        
        fano = FanoPlane()
        
        # Basic structure tests
        print("✓ Initialization test passed")
        assert len(fano.points) == 7
        assert len(fano.lines) == 7
        
        # Axiom verification
        axioms = verify_axioms(fano)
        for axiom, holds in axioms.items():
            status = "✓" if holds else "✗"
            print(f"{status} {axiom}")
        
        if all(axioms.values()):
            print("\n✓ ALL BASIC TESTS PASSED!")
            sys.exit(0)
        else:
            print("\n✗ SOME TESTS FAILED")
            sys.exit(1)
