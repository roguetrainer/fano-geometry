"""
Visualization Module for Fano Plane

Provides multiple visual representations of the Fano plane:
- Standard triangle with inscribed circle
- Symmetric arrangements
- 3D projections
- Interactive plots
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.collections import LineCollection
import matplotlib.animation as animation
from typing import Dict, List, Tuple, Optional
try:
    from .fano_geometry import FanoPlane
except ImportError:
    from fano_geometry import FanoPlane


class FanoVisualizer:
    """Handles all visualizations of the Fano plane."""
    
    def __init__(self, fano: FanoPlane):
        self.fano = fano
        self.colors = [
            '#FF6B6B',  # Red
            '#4ECDC4',  # Teal
            '#45B7D1',  # Blue
            '#FFA07A',  # Light Salmon
            '#98D8C8',  # Mint
            '#F7DC6F',  # Yellow
            '#BB8FCE',  # Purple
        ]
    
    def get_standard_coordinates(self) -> Dict[int, Tuple[float, float]]:
        """
        Return standard Fano plane coordinates:
        - Points 0,1,2 form an equilateral triangle
        - Points 3,4,5 are midpoints of sides
        - Point 6 is at the center
        """
        # Outer triangle vertices
        coords = {
            0: (0.0, 1.0),           # Top
            1: (-0.866, -0.5),       # Bottom left
            2: (0.866, -0.5),        # Bottom right
        }
        
        # Midpoints of sides
        coords[3] = ((coords[0][0] + coords[1][0])/2, 
                     (coords[0][1] + coords[1][1])/2)  # Midpoint 0-1
        coords[4] = ((coords[1][0] + coords[2][0])/2, 
                     (coords[1][1] + coords[2][1])/2)  # Midpoint 1-2
        coords[5] = ((coords[2][0] + coords[0][0])/2, 
                     (coords[2][1] + coords[0][1])/2)  # Midpoint 2-0
        
        # Center
        coords[6] = (0.0, 0.0)
        
        return coords
    
    def get_circular_coordinates(self) -> Dict[int, Tuple[float, float]]:
        """Return coordinates with all points on a circle."""
        coords = {}
        for i in range(7):
            angle = 2 * np.pi * i / 7 - np.pi/2  # Start at top
            coords[i] = (np.cos(angle), np.sin(angle))
        return coords
    
    def get_cube_projection_coordinates(self) -> Dict[int, Tuple[float, float]]:
        """
        Project the 7 non-origin corners of a 3D cube onto 2D.
        This gives another natural Fano plane embedding.
        """
        # 3D cube corners (excluding origin)
        cube_3d = {
            0: (1, 0, 0),
            1: (0, 1, 0),
            2: (0, 0, 1),
            3: (1, 1, 0),
            4: (1, 0, 1),
            5: (0, 1, 1),
            6: (1, 1, 1),
        }
        
        # Simple orthographic projection (ignore z)
        coords = {i: (x, y) for i, (x, y, z) in cube_3d.items()}
        
        return coords
    
    def plot_standard(self, ax=None, show_labels=True, highlight_line=None,
                     title="Fano Plane - Standard Representation"):
        """
        Plot the standard Fano plane representation with triangle and circle.
        
        Args:
            ax: Matplotlib axis (creates new figure if None)
            show_labels: Whether to show point labels
            highlight_line: Index of line to highlight (None for no highlight)
            title: Plot title
        """
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        
        coords = self.get_standard_coordinates()
        
        # Draw lines
        for line_idx, line in enumerate(self.fano.lines):
            points = sorted(list(line))
            color = self.colors[line_idx]
            alpha = 1.0 if highlight_line is None or highlight_line == line_idx else 0.3
            linewidth = 3 if highlight_line == line_idx else 2
            
            # Special handling for the circle (line containing 3,4,5,6)
            if line == frozenset([3, 4, 5]):
                # Draw as circular arc
                circle = Circle((0, 0), 0.65, fill=False, 
                              color=color, linewidth=linewidth, alpha=alpha)
                ax.add_patch(circle)
            else:
                # Draw as straight line
                line_points = [coords[p] for p in points]
                x_vals = [p[0] for p in line_points]
                y_vals = [p[1] for p in line_points]
                
                # Extend line beyond points for better visibility
                if len(set(x_vals)) > 1:  # Not vertical
                    x_min, x_max = min(x_vals), max(x_vals)
                    x_extended = np.linspace(x_min - 0.2, x_max + 0.2, 100)
                    
                    # Fit line through points
                    if len(set(x_vals)) == len(x_vals):  # All different x
                        z = np.polyfit(x_vals, y_vals, 1)
                        p = np.poly1d(z)
                        y_extended = p(x_extended)
                    else:
                        y_extended = [y_vals[0]] * len(x_extended)
                    
                    ax.plot(x_extended, y_extended, color=color, 
                           linewidth=linewidth, alpha=alpha, zorder=1)
                else:  # Vertical line
                    x_val = x_vals[0]
                    ax.plot([x_val, x_val], [-1, 1.5], color=color,
                           linewidth=linewidth, alpha=alpha, zorder=1)
        
        # Draw points
        for point, (x, y) in coords.items():
            ax.plot(x, y, 'ko', markersize=12, zorder=3)
            ax.plot(x, y, 'wo', markersize=8, zorder=4)
            
            if show_labels:
                ax.text(x, y, str(point), ha='center', va='center',
                       fontsize=12, fontweight='bold', zorder=5)
        
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.0, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=14, pad=20)
        
        return ax
    
    def plot_circular(self, ax=None, show_labels=True, title="Fano Plane - Circular Layout"):
        """Plot Fano plane with all points on a circle."""
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        
        coords = self.get_circular_coordinates()
        
        # Draw lines as chords
        for line_idx, line in enumerate(self.fano.lines):
            points = sorted(list(line))
            color = self.colors[line_idx]
            
            # Draw all three edges of the triangle formed by the three points
            for i in range(3):
                p1, p2 = points[i], points[(i+1) % 3]
                x_vals = [coords[p1][0], coords[p2][0]]
                y_vals = [coords[p1][1], coords[p2][1]]
                ax.plot(x_vals, y_vals, color=color, linewidth=2, alpha=0.7, zorder=1)
        
        # Draw the circle
        circle = Circle((0, 0), 1.0, fill=False, color='gray', 
                       linewidth=1, linestyle='--', alpha=0.3)
        ax.add_patch(circle)
        
        # Draw points
        for point, (x, y) in coords.items():
            ax.plot(x, y, 'ko', markersize=12, zorder=3)
            ax.plot(x, y, 'wo', markersize=8, zorder=4)
            
            if show_labels:
                # Offset labels outward
                offset = 1.15
                ax.text(x * offset, y * offset, str(point), 
                       ha='center', va='center',
                       fontsize=12, fontweight='bold', zorder=5)
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=14, pad=20)
        
        return ax
    
    def plot_all_representations(self):
        """Create a figure showing multiple representations."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 14))
        
        # Standard representation
        self.plot_standard(axes[0, 0], title="Standard (Triangle + Circle)")
        
        # Circular representation
        self.plot_circular(axes[0, 1], title="Circular Layout")
        
        # Highlight individual lines
        self.plot_standard(axes[1, 0], highlight_line=1, 
                          title="Line 1 Highlighted: {1, 2, 4}")
        
        # Cube projection
        coords = self.get_cube_projection_coordinates()
        ax = axes[1, 1]
        
        # Draw lines
        for line_idx, line in enumerate(self.fano.lines):
            points = sorted(list(line))
            color = self.colors[line_idx]
            
            # Draw edges
            for i in range(3):
                p1, p2 = points[i], points[(i+1) % 3]
                x_vals = [coords[p1][0], coords[p2][0]]
                y_vals = [coords[p1][1], coords[p2][1]]
                ax.plot(x_vals, y_vals, color=color, linewidth=2, alpha=0.6, zorder=1)
        
        # Draw points
        for point, (x, y) in coords.items():
            ax.plot(x, y, 'ko', markersize=12, zorder=3)
            ax.plot(x, y, 'wo', markersize=8, zorder=4)
            ax.text(x + 0.08, y + 0.08, str(point), 
                   ha='left', va='bottom',
                   fontsize=11, fontweight='bold', zorder=5)
        
        ax.set_xlim(-0.3, 1.5)
        ax.set_ylim(-0.3, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title("Cube Corner Projection", fontsize=14, pad=20)
        
        plt.tight_layout()
        return fig
    
    def plot_line_by_line_construction(self, save_animation=False, filename='fano_construction.gif'):
        """Animate the construction of the Fano plane line by line."""
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        coords = self.get_standard_coordinates()
        
        # Draw points first
        for point, (x, y) in coords.items():
            ax.plot(x, y, 'ko', markersize=12, zorder=3)
            ax.plot(x, y, 'wo', markersize=8, zorder=4)
            ax.text(x, y, str(point), ha='center', va='center',
                   fontsize=12, fontweight='bold', zorder=5)
        
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.0, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        
        lines_drawn = []
        
        def init():
            return lines_drawn
        
        def animate(frame):
            if frame < len(self.fano.lines):
                line_idx = frame
                line = self.fano.lines[line_idx]
                points = sorted(list(line))
                color = self.colors[line_idx]
                
                # Add line to plot
                if line == frozenset([3, 4, 5]):
                    circle = Circle((0, 0), 0.65, fill=False, 
                                  color=color, linewidth=3)
                    ax.add_patch(circle)
                    lines_drawn.append(circle)
                else:
                    line_points = [coords[p] for p in points]
                    x_vals = [p[0] for p in line_points]
                    y_vals = [p[1] for p in line_points]
                    
                    if len(set(x_vals)) > 1:
                        x_min, x_max = min(x_vals), max(x_vals)
                        x_extended = np.linspace(x_min - 0.2, x_max + 0.2, 100)
                        z = np.polyfit(x_vals, y_vals, 1)
                        p = np.poly1d(z)
                        y_extended = p(x_extended)
                        line_obj, = ax.plot(x_extended, y_extended, color=color, 
                                          linewidth=3, zorder=1)
                    else:
                        x_val = x_vals[0]
                        line_obj, = ax.plot([x_val, x_val], [-1, 1.5], color=color,
                                          linewidth=3, zorder=1)
                    lines_drawn.append(line_obj)
                
                ax.set_title(f"Construction: {frame+1}/7 lines drawn\n"
                           f"Line {line_idx}: {{{', '.join(map(str, sorted(points)))}}}",
                           fontsize=14, pad=20)
            
            return lines_drawn
        
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                      frames=len(self.fano.lines)+5, 
                                      interval=1000, blit=False, repeat=True)
        
        if save_animation:
            anim.save(filename, writer='pillow', fps=1)
            print(f"Animation saved to {filename}")
        
        return anim
    
    def plot_incidence_matrix(self):
        """Visualize the incidence matrix as a heatmap."""
        fig, ax = plt.subplots(1, 1, figsize=(8, 7))
        
        matrix = self.fano.incidence_matrix()
        
        im = ax.imshow(matrix, cmap='RdBu_r', vmin=0, vmax=1, aspect='auto')
        
        # Add grid
        ax.set_xticks(range(7))
        ax.set_yticks(range(7))
        ax.set_xticklabels([f'L{i}' for i in range(7)])
        ax.set_yticklabels([f'P{i}' for i in range(7)])
        
        # Add values in cells
        for i in range(7):
            for j in range(7):
                text = ax.text(j, i, str(matrix[i, j]),
                             ha="center", va="center", color="black",
                             fontsize=14, fontweight='bold')
        
        ax.set_xlabel('Lines', fontsize=12)
        ax.set_ylabel('Points', fontsize=12)
        ax.set_title('Point-Line Incidence Matrix', fontsize=14, pad=20)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_ticks([0, 1])
        cbar.set_ticklabels(['Not Incident', 'Incident'])
        
        plt.tight_layout()
        return fig


def demo_visualizations():
    """Run a demonstration of all visualization capabilities."""
    fano = FanoPlane()
    viz = FanoVisualizer(fano)
    
    # Show all representations
    print("Generating multiple representations...")
    fig1 = viz.plot_all_representations()
    plt.savefig('/home/claude/fano_representations.png', dpi=150, bbox_inches='tight')
    print("Saved: fano_representations.png")
    
    # Show incidence matrix
    print("\nGenerating incidence matrix visualization...")
    fig2 = viz.plot_incidence_matrix()
    plt.savefig('/home/claude/fano_incidence.png', dpi=150, bbox_inches='tight')
    print("Saved: fano_incidence.png")
    
    # Individual standard plot
    print("\nGenerating standard representation...")
    fig3, ax = plt.subplots(1, 1, figsize=(8, 8))
    viz.plot_standard(ax)
    plt.savefig('/home/claude/fano_standard.png', dpi=150, bbox_inches='tight')
    print("Saved: fano_standard.png")
    
    plt.show()


if __name__ == "__main__":
    demo_visualizations()
