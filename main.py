"""
3D Solar System Simulator
Interactive solar system with realistic orbits, scaling options, and camera controls
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider
import matplotlib.patches as mpatches


class CelestialBody:
    """Represents a celestial body (planet or sun)"""
    
    def __init__(self, name, radius, distance, orbital_period, color, tilt=0):
        """
        Initialize celestial body
        
        Args:
            name: Body name
            radius: Radius (km)
            distance: Distance from sun (AU - Astronomical Units)
            orbital_period: Orbital period (Earth days)
            color: Display color
            tilt: Orbital tilt in degrees
        """
        self.name = name
        self.radius = radius  # km
        self.distance = distance  # AU
        self.orbital_period = orbital_period  # days
        self.color = color
        self.tilt = np.radians(tilt)
        self.angle = np.random.uniform(0, 2 * np.pi)  # Random starting position
        self.position = np.array([0.0, 0.0, 0.0])
        
    def update_position(self, time_step):
        """Update planet position based on orbital mechanics"""
        # Angular velocity (radians per time step)
        angular_velocity = (2 * np.pi) / self.orbital_period
        self.angle += angular_velocity * time_step
        
        # Calculate position in orbital plane
        x = self.distance * np.cos(self.angle)
        y = self.distance * np.sin(self.angle)
        z = y * np.sin(self.tilt)  # Apply orbital tilt
        y = y * np.cos(self.tilt)
        
        self.position = np.array([x, y, z])
        return self.position


class SolarSystem:
    """Solar system simulator with interactive controls"""
    
    def __init__(self, scale_mode='logarithmic'):
        """
        Initialize solar system
        
        Args:
            scale_mode: 'realistic', 'logarithmic', or 'artistic'
        """
        self.scale_mode = scale_mode
        self.time_step = 1  # days per frame
        self.bodies = []
        self.trails = {}  # Store orbital trails
        self.trail_length = 100
        self.paused = False
        self.show_orbits = True
        self.show_labels = True
        
        self._initialize_bodies()
        
    def _initialize_bodies(self):
        """Initialize all celestial bodies with real data"""
        # Data: (name, radius_km, distance_AU, period_days, color, tilt_degrees)
        bodies_data = [
            ('Sun', 696000, 0, 0, '#FDB813', 0),
            ('Mercury', 2440, 0.39, 88, '#8C7853', 7.0),
            ('Venus', 6052, 0.72, 225, '#FFC649', 3.4),
            ('Earth', 6371, 1.0, 365, '#4169E1', 0.0),
            ('Mars', 3390, 1.52, 687, '#CD5C5C', 1.9),
            ('Jupiter', 69911, 5.20, 4333, '#DAA520', 1.3),
            ('Saturn', 58232, 9.54, 10759, '#F4A460', 2.5),
            ('Uranus', 25362, 19.19, 30687, '#4FD0E0', 0.8),
            ('Neptune', 24622, 30.07, 60190, '#4169E1', 1.8),
        ]
        
        for data in bodies_data:
            body = CelestialBody(*data)
            self.bodies.append(body)
            if body.name != 'Sun':
                self.trails[body.name] = []
    
    def get_scaled_radius(self, radius):
        """Scale planet radius for visualization"""
        if self.scale_mode == 'realistic':
            return radius / 100000  # Very small, hard to see
        elif self.scale_mode == 'logarithmic':
            return 0.02 + np.log10(radius) * 0.01  # Logarithmic scale
        else:  # artistic
            return 0.05 + (radius / 100000) * 2  # Exaggerated but visible
    
    def get_scaled_distance(self, distance):
        """Scale orbital distance for visualization"""
        if self.scale_mode == 'realistic':
            return distance
        elif self.scale_mode == 'logarithmic':
            if distance == 0:
                return 0
            return np.log10(distance * 10 + 1) * 3
        else:  # artistic
            return distance ** 0.7 * 5  # Compressed distances
    
    def update(self, frame):
        """Update all bodies for animation"""
        if not self.paused:
            for body in self.bodies[1:]:  # Skip sun
                body.update_position(self.time_step)
                
                # Update trail
                if body.name in self.trails:
                    self.trails[body.name].append(body.position.copy())
                    if len(self.trails[body.name]) > self.trail_length:
                        self.trails[body.name].pop(0)
    
    def create_sphere(self, radius, center=(0, 0, 0), resolution=20):
        """Create sphere vertices for planet rendering"""
        u = np.linspace(0, 2 * np.pi, resolution)
        v = np.linspace(0, np.pi, resolution)
        x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
        y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]
        return x, y, z
    
    def visualize_interactive(self):
        """Create interactive 3D visualization"""
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Adjust layout to make room for controls
        plt.subplots_adjust(bottom=0.25, right=0.85)
        
        # Get maximum orbital distance for plot limits
        max_distance = max([self.get_scaled_distance(b.distance) for b in self.bodies])
        
        def draw_frame(frame):
            """Draw single frame of animation"""
            ax.clear()
            
            # Update positions
            self.update(frame)
            
            # Draw orbital paths
            if self.show_orbits:
                for body in self.bodies[1:]:  # Skip sun
                    orbit_points = 100
                    angles = np.linspace(0, 2 * np.pi, orbit_points)
                    distance = self.get_scaled_distance(body.distance)
                    
                    orbit_x = distance * np.cos(angles)
                    orbit_y = distance * np.sin(angles) * np.cos(body.tilt)
                    orbit_z = distance * np.sin(angles) * np.sin(body.tilt)
                    
                    ax.plot(orbit_x, orbit_y, orbit_z, 
                           color=body.color, alpha=0.3, linestyle='--', linewidth=0.5)
            
            # Draw Sun
            sun = self.bodies[0]
            sun_radius = self.get_scaled_radius(sun.radius)
            x, y, z = self.create_sphere(sun_radius, resolution=30)
            ax.plot_surface(x, y, z, color=sun.color, alpha=1.0, shade=True)
            
            if self.show_labels:
                ax.text(0, 0, sun_radius * 1.5, sun.name, 
                       fontsize=10, fontweight='bold', color='white')
            
            # Draw planets
            for body in self.bodies[1:]:
                pos = body.position
                scaled_pos = pos * np.array([
                    self.get_scaled_distance(1) / 1,
                    self.get_scaled_distance(1) / 1,
                    self.get_scaled_distance(1) / 1
                ])
                
                radius = self.get_scaled_radius(body.radius)
                
                # Draw planet
                x, y, z = self.create_sphere(radius, center=scaled_pos, resolution=20)
                ax.plot_surface(x, y, z, color=body.color, alpha=0.9, shade=True)
                
                # Draw label
                if self.show_labels:
                    ax.text(scaled_pos[0], scaled_pos[1], scaled_pos[2] + radius * 2,
                           body.name, fontsize=8, color='white')
                
                # Draw trail
                if body.name in self.trails and len(self.trails[body.name]) > 1:
                    trail = np.array(self.trails[body.name])
                    scaled_trail = trail * np.array([
                        self.get_scaled_distance(1) / 1,
                        self.get_scaled_distance(1) / 1,
                        self.get_scaled_distance(1) / 1
                    ])
                    ax.plot(scaled_trail[:, 0], scaled_trail[:, 1], scaled_trail[:, 2],
                           color=body.color, alpha=0.6, linewidth=1.5)
            
            # Set plot properties
            ax.set_xlim([-max_distance * 1.2, max_distance * 1.2])
            ax.set_ylim([-max_distance * 1.2, max_distance * 1.2])
            ax.set_zlim([-max_distance * 0.5, max_distance * 0.5])
            
            ax.set_xlabel('X (AU)', color='white', fontsize=10)
            ax.set_ylabel('Y (AU)', color='white', fontsize=10)
            ax.set_zlabel('Z (AU)', color='white', fontsize=10)
            
            # Style
            ax.set_facecolor('black')
            fig.patch.set_facecolor('black')
            ax.grid(True, alpha=0.2)
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            
            title_text = f'Solar System Simulator - Scale: {self.scale_mode.title()}'
            if self.paused:
                title_text += ' [PAUSED]'
            ax.set_title(title_text, color='white', fontsize=14, fontweight='bold', pad=20)
            
            return ax,
        
        # Create animation
        anim = FuncAnimation(fig, draw_frame, frames=None, interval=50, blit=False)
        
        # Add control buttons
        ax_pause = plt.axes([0.15, 0.05, 0.15, 0.04])
        btn_pause = Button(ax_pause, 'Pause/Resume', color='lightgray', hovercolor='gray')
        
        ax_orbits = plt.axes([0.35, 0.05, 0.15, 0.04])
        btn_orbits = Button(ax_orbits, 'Toggle Orbits', color='lightgray', hovercolor='gray')
        
        ax_labels = plt.axes([0.55, 0.05, 0.15, 0.04])
        btn_labels = Button(ax_labels, 'Toggle Labels', color='lightgray', hovercolor='gray')
        
        ax_reset = plt.axes([0.75, 0.05, 0.15, 0.04])
        btn_reset = Button(ax_reset, 'Reset View', color='lightblue', hovercolor='skyblue')
        
        # Speed slider
        ax_speed = plt.axes([0.15, 0.12, 0.75, 0.02])
        slider_speed = Slider(ax_speed, 'Speed', 0.1, 10.0, valinit=1.0, 
                             color='skyblue', valstep=0.1)
        
        def toggle_pause(event):
            self.paused = not self.paused
        
        def toggle_orbits(event):
            self.show_orbits = not self.show_orbits
        
        def toggle_labels(event):
            self.show_labels = not self.show_labels
        
        def reset_view(event):
            ax.view_init(elev=20, azim=45)
            plt.draw()
        
        def update_speed(val):
            self.time_step = slider_speed.val
        
        btn_pause.on_clicked(toggle_pause)
        btn_orbits.on_clicked(toggle_orbits)
        btn_labels.on_clicked(toggle_labels)
        btn_reset.on_clicked(reset_view)
        slider_speed.on_changed(update_speed)
        
        # Add legend
        legend_elements = [
            mpatches.Patch(color=body.color, label=f"{body.name} ({body.orbital_period:.0f}d)")
            for body in self.bodies[:5]  # First 5 planets
        ]
        ax.legend(handles=legend_elements, loc='upper right', 
                 fontsize=8, facecolor='black', edgecolor='white', 
                 labelcolor='white', framealpha=0.8)
        
        plt.show()
    
    def print_info(self):
        """Print information about the solar system"""
        print("\n" + "=" * 70)
        print("SOLAR SYSTEM BODIES")
        print("=" * 70)
        print(f"{'Body':<12} {'Radius (km)':<15} {'Distance (AU)':<15} {'Period (days)':<15}")
        print("-" * 70)
        
        for body in self.bodies:
            print(f"{body.name:<12} {body.radius:<15,.0f} {body.distance:<15.2f} {body.orbital_period:<15,.0f}")
        
        print("=" * 70)


def main():
    """Main function to run the solar system simulator"""
    print("=" * 70)
    print("3D SOLAR SYSTEM SIMULATOR")
    print("=" * 70)
    
    print("\n[1/4] Initializing solar system...")
    print("✓ Loaded 9 celestial bodies (Sun + 8 planets)")
    
    # Choose scale mode
    print("\n[2/4] Select visualization scale mode:")
    print("  1. Realistic - True scale (planets very small)")
    print("  2. Logarithmic - Logarithmic scale (balanced)")
    print("  3. Artistic - Artistic scale (exaggerated, most visible)")
    
    choice = input("\nEnter choice (1-3) [default: 2]: ").strip()
    
    scale_modes = {
        '1': 'realistic',
        '2': 'logarithmic',
        '3': 'artistic',
        '': 'logarithmic'
    }
    
    scale_mode = scale_modes.get(choice, 'logarithmic')
    print(f"✓ Using {scale_mode} scale mode")
    
    # Create solar system
    print("\n[3/4] Creating solar system simulation...")
    solar_system = SolarSystem(scale_mode=scale_mode)
    solar_system.print_info()
    
    print("\n[4/4] Launching interactive 3D visualization...")
    print("\n" + "=" * 70)
    print("CONTROLS:")
    print("=" * 70)
    print("Mouse Controls:")
    print("  • Click and drag       - Rotate view")
    print("  • Scroll wheel         - Zoom in/out")
    print("  • Right-click and drag - Pan view")
    print("\nButton Controls:")
    print("  • Pause/Resume  - Pause or resume animation")
    print("  • Toggle Orbits - Show/hide orbital paths")
    print("  • Toggle Labels - Show/hide planet names")
    print("  • Reset View    - Return to default camera angle")
    print("\nSlider:")
    print("  • Speed - Adjust simulation speed (0.1x to 10x)")
    print("\nColor Legend:")
    print("  • Yellow/Gold - Sun")
    print("  • Gray/Brown  - Mercury")
    print("  • Yellow      - Venus")
    print("  • Blue        - Earth")
    print("  • Red         - Mars")
    print("  • Gold        - Jupiter")
    print("  • Tan         - Saturn")
    print("  • Cyan        - Uranus")
    print("  • Blue        - Neptune")
    print("=" * 70)
    print("\nClose the window to exit.")
    print("\nStarting simulation...\n")
    
    # Launch visualization
    solar_system.visualize_interactive()
    
    print("\n" + "=" * 70)
    print("Simulation ended. Thank you for exploring the solar system!")
    print("=" * 70)


if __name__ == "__main__":
    main()