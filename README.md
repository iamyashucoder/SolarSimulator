# 3D Solar System Simulator

An interactive 3D simulation of our solar system with realistic orbital mechanics, multiple scaling options, and full camera controls for exploration.

## Features

- **Realistic Orbital Mechanics**: Accurate orbital periods and distances
- **Interactive 3D Controls**: Full camera rotation, zoom, and pan
- **Multiple Scale Modes**: Realistic, logarithmic, and artistic scaling
- **Orbital Trails**: Visual tracking of planet paths
- **Animation Controls**: Pause, resume, and speed adjustment
- **Real Astronomical Data**: Actual planet sizes, distances, and periods
- **Customizable Display**: Toggle orbits and labels
![Demo Animation](./assets/demo.gif)
## Setup Instructions

### 1. Create Conda Environment

```bash
conda create -n solar3d python=3.9 -y
conda activate solar3d
```

### 2. Install Required Packages

```bash
pip install numpy matplotlib
```

Same two packages as previous projects!

### 3. Run the Demo

```bash
python main.py
```

You'll be prompted to select a scale mode (logarithmic is recommended).

## Scale Modes

### 1. Realistic Scale
- Uses true proportions from astronomy
- **Pros**: Scientifically accurate
- **Cons**: Inner planets nearly invisible, vast empty space
- **Best for**: Understanding true scale of solar system

### 2. Logarithmic Scale (Recommended)
- Uses logarithmic compression for distances and sizes
- **Pros**: All planets visible, balanced view
- **Cons**: Not to true scale
- **Best for**: General exploration and education

### 3. Artistic Scale
- Exaggerated planet sizes, compressed distances
- **Pros**: Most visually appealing, all features visible
- **Cons**: Least accurate
- **Best for**: Presentations and demonstrations

## Controls

### Mouse Controls
- **Click and drag**: Rotate the 3D view
- **Scroll wheel**: Zoom in/out
- **Right-click and drag**: Pan the view

### Button Controls
- **Pause/Resume**: Pause or resume the orbital animation
- **Toggle Orbits**: Show or hide the dotted orbital paths
- **Toggle Labels**: Show or hide planet name labels
- **Reset View**: Return camera to default angle (20° elevation, 45° azimuth)

### Speed Slider
- Adjust simulation speed from **0.1x to 10x**
- 1.0x = 1 Earth day per frame
- Higher values = faster orbits

## Solar System Data

The simulation uses real astronomical data:

| Planet  | Radius (km) | Distance (AU) | Orbital Period (days) |
|---------|-------------|---------------|----------------------|
| Sun     | 696,000     | 0.00          | -                    |
| Mercury | 2,440       | 0.39          | 88                   |
| Venus   | 6,052       | 0.72          | 225                  |
| Earth   | 6,371       | 1.00          | 365                  |
| Mars    | 3,390       | 1.52          | 687                  |
| Jupiter | 69,911      | 5.20          | 4,333                |
| Saturn  | 58,232      | 9.54          | 10,759               |
| Uranus  | 25,362      | 19.19         | 30,687               |
| Neptune | 24,622      | 30.07         | 60,190               |

**AU** = Astronomical Unit (distance from Earth to Sun: ~150 million km)

## Customization

### Change Starting Positions
Planets start at random positions. To have them start aligned:

```python
# In CelestialBody.__init__, replace:
self.angle = np.random.uniform(0, 2 * np.pi)
# With:
self.angle = 0  # All planets start aligned
```

### Adjust Trail Length
```python
# In SolarSystem.__init__:
self.trail_length = 200  # Longer trails (default: 100)
```

### Change Animation Speed
```python
# In SolarSystem.__init__:
self.time_step = 2  # 2 days per frame (default: 1)
```

### Modify Color Scheme
Edit colors in the `bodies_data` list:
```python
('Earth', 6371, 1.0, 365, '#00FF00', 0.0),  # Green Earth
```

### Add Dwarf Planets
Add to the `bodies_data` list:
```python
('Pluto', 1188, 39.48, 90560, '#D3D3D3', 17.2),
```

## Project Structure

```
├── main.py          # Complete implementation
└── README.md        # This file
```

## Example Output

```
======================================================================
3D SOLAR SYSTEM SIMULATOR
======================================================================

[1/4] Initializing solar system...
✓ Loaded 9 celestial bodies (Sun + 8 planets)

[2/4] Select visualization scale mode:
  1. Realistic - True scale (planets very small)
  2. Logarithmic - Logarithmic scale (balanced)
  3. Artistic - Artistic scale (exaggerated, most visible)

Enter choice (1-3) [default: 2]: 2
✓ Using logarithmic scale mode

[3/4] Creating solar system simulation...

======================================================================
SOLAR SYSTEM BODIES
======================================================================
Body         Radius (km)     Distance (AU)   Period (days)   
----------------------------------------------------------------------
Sun          696,000         0.00            0               
Mercury      2,440           0.39            88              
Venus        6,052           0.72            225             
Earth        6,371           1.00            365             
Mars         3,390           1.52            687             
Jupiter      69,911          5.20            4,333           
Saturn       58,232          9.54            10,759          
Uranus       25,362          19.19           30,687          
Neptune      24,622          30.07           60,190          
======================================================================

[4/4] Launching interactive 3D visualization...
```

## Educational Features

### Understanding Orbital Mechanics
- Watch how planets move at different speeds
- Inner planets orbit much faster than outer planets
- Observe Kepler's laws in action

### Scale Appreciation
- Compare realistic scale to see vast distances in space
- Understand why space exploration is challenging
- Appreciate the emptiness of the solar system

### Interactive Learning
- Pause to examine specific planetary configurations
- Speed up to see long-term orbital patterns
- Rotate view to see orbital plane inclinations

## Advanced Usage

### Taking Screenshots
While the window is open:
1. Pause the animation
2. Adjust the view angle
3. Save using matplotlib's toolbar (disk icon)

### Recording Videos
For longer recordings, consider:
1. Reduce animation interval for smoother motion
2. Use external screen recording software
3. Export frames and compile with video editing tools

### Performance Optimization

For slower computers:
```python
# Reduce sphere resolution in create_sphere():
x, y, z = self.create_sphere(radius, resolution=10)  # Lower detail

# Reduce trail length:
self.trail_length = 50  # Shorter trails

# Increase animation interval:
anim = FuncAnimation(fig, draw_frame, interval=100)  # Slower FPS
```

## Requirements

- Python 3.9+
- numpy
- matplotlib

## Troubleshooting

**Issue**: Animation is choppy
- **Solution**: Reduce sphere resolution or trail length

**Issue**: Planets too small/large
- **Solution**: Try different scale mode (logarithmic recommended)

**Issue**: Can't see outer planets
- **Solution**: Use logarithmic or artistic scale mode

**Issue**: Controls not responding
- **Solution**: Click on the plot area first to focus

**Issue**: Window appears black
- **Solution**: Wait a few seconds for rendering, or check graphics drivers

## Fun Things to Try

1. **Watch a Year Pass**: Set speed to 10x and watch Earth complete an orbit
2. **Find Alignments**: Pause when planets line up
3. **Compare Orbits**: Observe how Mercury races around while Neptune crawls
4. **Zoom to Sun**: See the size comparison between Sun and planets
5. **Tilt View**: Rotate to see orbital inclinations from different angles

## Scientific Notes

- Orbital inclinations are relative to Earth's orbital plane (ecliptic)
- Planets start at random positions for variety
- Rotation speeds are not simulated (only orbital motion)
- Moons are not included (would require hierarchical orbits)
- Rings (Saturn) are not rendered

## Future Enhancements (DIY)

Want to extend the project? Try adding:
- Planet rotation on axis
- Asteroid belt
- Comets with elliptical orbits
- Moons (especially for Jupiter and Saturn)
- Ecliptic plane grid
- Date/time display
- Planet information panel

## License

Free to use and modify for educational purposes.

## Author

Created as an educational tool for exploring our solar system and understanding orbital mechanics.