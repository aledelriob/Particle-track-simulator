# ============================================
# PARTICLE TRACK SIMULATOR
# ============================================
# A simple simulation of particle trajectories
# for DESY Ausbildung application
#
# Author: Alejandra del Río B.
# Date: September 2026
# ============================================

# Import required libraries
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation, PillowWriter

# ============================================
# PARTICLE TYPES DEFINITION
# ============================================

# Define different particle types with their properties
PARTICLE_TYPES = {
    'electron': {'charge': -1, 'mass': 0.0005, 'color': 'blue', 'label': 'e⁻'},
    'proton':   {'charge':  1, 'mass': 1.0,    'color': 'red',  'label': 'p⁺'},
    'muon':     {'charge': -1, 'mass': 0.1,    'color': 'green','label': 'μ⁻'},
    'neutron':  {'charge':  0, 'mass': 1.0,    'color': 'gray', 'label': 'n⁰'}
}

# ============================================
# FUNCTION 1: CREATE A PARTICLE
# ============================================

def create_particle():
    """
    Creates a particle with random type and direction.
    
    Returns:
        dict: Dictionary with particle properties
    """
    
    # Choose a random particle type
    particle_type = random.choice(list(PARTICLE_TYPES.keys()))
    
    # Get properties from the type definition
    type_props = PARTICLE_TYPES[particle_type]
    
    # Generate random angle between 0 and 360 degrees
    angle_degrees = random.uniform(0, 360)
    
    # Convert to radians (Python uses radians, not degrees)
    angle_radians = angle_degrees * (np.pi / 180)
    
    # Random velocity between 1 and 10 (arbitrary units)
    velocity = random.uniform(1, 10)
    
    # Create dictionary with particle properties
    particle = {
        'type': particle_type,
        'angle_degrees': angle_degrees,
        'angle_radians': angle_radians,
        'velocity': velocity,
        'x_initial': 0,
        'y_initial': 0,
        'charge': type_props['charge'],
        'mass': type_props['mass'],
        'color': type_props['color'],
        'label': type_props['label']
    }
    
    return particle


# ============================================
# TEST THE FUNCTION
# ============================================

# Create a test particle
# test_particle = create_particle()

# Print its properties
# print("=" * 50)
# print("TEST PARTICLE")
# print("=" * 50)
# print(f"Angle: {test_particle['angle_degrees']:.2f} degrees")
# print(f"Angle in radians: {test_particle['angle_radians']:.2f} rad")
# print(f"Velocity: {test_particle['velocity']:.2f}")
# print(f"Initial position: ({test_particle['x_initial']}, {test_particle['y_initial']})")
# print("=" * 50)

# ============================================
# FUNCTION 2: CALCULATE PARTICLE POSITION
# ============================================

def calculate_position(particle, time, magnetic_field=0.0):
    """
    Calculates the position of a particle at a given time.
    
    Args:
        particle (dict): Dictionary with particle properties
        time (float): Time in arbitrary units
        magnetic_field (float): Magnetic field strength in Z direction (default: 0)
    
    Returns:
        tuple: (x, y) position coordinates
    """
    
    # Extract particle properties
    velocity = particle['velocity']
    angle = particle['angle_radians']
    x0 = particle['x_initial']
    y0 = particle['y_initial']
    charge = particle['charge']
    mass = particle['mass']
    
    # If no magnetic field or neutral particle, use straight line motion
    if magnetic_field == 0.0 or charge == 0:
        # Calculate position using physics formulas
        # x = x0 + v * t * cos(θ)
        # y = y0 + v * t * sin(θ)
        x = x0 + velocity * time * np.cos(angle)
        y = y0 + velocity * time * np.sin(angle)
        
    else:
        # If magnetic field exists and particle is charged, calculate curved trajectory
        # Radius of curvature: r = (m * v) / (|q| * B)
        # Angular frequency: ω = (|q| * B) / m
        
        # Calculate radius of curvature
        radius = (mass * velocity) / (abs(charge) * abs(magnetic_field))
        
        # Calculate angular frequency
        omega = (abs(charge) * abs(magnetic_field)) / mass
        
        # Direction of curvature depends on charge sign
        # Positive charge: counterclockwise
        # Negative charge: clockwise
        direction = 1 if charge > 0 else -1
        
        # Calculate position on circular path
        # The particle moves in a circle with radius r
        # Center of circle is offset from origin
        
        # Initial velocity components
        vx = velocity * np.cos(angle)
        vy = velocity * np.sin(angle)
        
        # Center of circular motion (offset from origin)
        # Perpendicular to initial velocity
        center_x = x0 + direction * (mass * vy) / (charge * magnetic_field)
        center_y = y0 - direction * (mass * vx) / (charge * magnetic_field)
        
        # Angle swept by the particle
        theta = omega * time * direction
        
        # Position at time t (circular motion)
        x = center_x - direction * radius * np.sin(theta + np.arctan2(y0 - center_y, x0 - center_x))
        y = center_y + direction * radius * np.cos(theta + np.arctan2(y0 - center_y, x0 - center_x))
    
    # Return the position (outside the if/else)
    return (x, y)

# ============================================
# TEST THE POSITION FUNCTION
# ============================================

# Create a particle
# test_particle = create_particle()

# Calculate position at different times
# print("\nTEST: PARTICLE POSITION AT DIFFERENT TIMES")
# print("=" * 50)

# for t in [0, 1, 2, 3, 4, 5]:
#    position = calculate_position(test_particle, t)
#    print(f"Time t={t}: Position = ({position[0]:.2f}, {position[1]:.2f})")

# print("=" * 50)

# ============================================
# FUNCTION 3: SIMULATE MULTIPLE PARTICLES
# ============================================

def simulate_particles(num_particles, max_time, time_steps, magnetic_field=0.0):
    """
    Simulates multiple particles and calculates their trajectories.
    
    Args:
        num_particles (int): Number of particles to simulate
        max_time (float): Maximum time to simulate
        time_steps (int): Number of time points to calculate
        magnetic_field (float): Magnetic field strenght (defaul: 0)
    
    Returns:
        tuple: (trajectories, particle_info)
            - trajectories: List of trajectories
            - particle_info: List of dicts with particle properties
    """
    
    # Create list to store all trajectories
    all_trajectories = []
    
    # Create list to store particle info
    all_particle_info = []
    
    # Generate and simulate each particle
    for i in range(num_particles):
        
        # Create a new particle
        particle = create_particle()
        
        # Store particle info (type, charge, color, etc.)
        all_particle_info.append(particle)
        
        # Create list to store this particle's trajectory
        trajectory = []
        
        # Calculate position at different times
        for t in range(time_steps):
            # Calculate time value (0, 1, 2, ..., max_time)
            current_time = t * (max_time / time_steps)
            
            # Calculate position at this time
            position = calculate_position(particle, current_time, magnetic_field)
            
            # Add position to trajectory
            trajectory.append(position)
        
        # Add this trajectory to the list
        all_trajectories.append(trajectory)
    
    return all_trajectories, all_particle_info

# ============================================
# TEST THE SIMULATION FUNCTION
# ============================================

# Simulate 5 particles for 10 time units with 100 time steps
# print("\nTEST: SIMULATING 5 PARTICLES")
# print("=" * 50)

# trajectories = simulate_particles(num_particles=5, max_time=10, time_steps=100)

# print(f"Number of trajectories: {len(trajectories)}")
# print(f"Points per trajectory: {len(trajectories[0])}")
# print(f"First trajectory, first point: {trajectories[0][0]}")
# print(f"First trajectory, last point: {trajectories[0][-1]}")
# print("=" * 50)

# ============================================
# HELPER FUNCTION: GET PARTICLE COLORS
# ============================================

def get_particle_colors_and_labels(num_particles):
    """
    Generates colors and labels for particle types.
    
    Args:
        num_particles (int): Number of particles
    
    Returns:
        tuple: (colors_list, labels_dict)
    """
    
    colors = []
    
    # Generate random particle types for visualization
    particle_types_list = list(PARTICLE_TYPES.keys())
    
    for i in range(num_particles):
        # Assign random type for this trajectory
        ptype = random.choice(particle_types_list)
        colors.append(PARTICLE_TYPES[ptype]['color'])
    
    return colors, {}

# ============================================
# FUNCTION 4: PLOT TRAJECTORIES
# ============================================

def plot_trajectories(trajectories, particle_info=None, detector_positions=None, show_legend=True):
    """
    Plots particle trajectories using matplotlib.
    
    Args:
        trajectories (list): List of trajectories from simulate_particles()
        detector_positions (list, optional): List of x-coordinates for detectors
        show_legend (bool): Whether to show legend (disable for many particles)
    """
    
    # Create a new figure with specific size
    plt.figure(figsize=(12, 10))
    
    # Plot each trajectory
    # Use actual particle colors from particle_info
    if particle_info is None:
        # Fallback to random colors if no particle info provided
        type_colors, _ = get_particle_colors_and_labels(len(trajectories))
    else:
        # Use actual colors from particle info
        type_colors = [p['color'] for p in particle_info]
        
    
    for i, trajectory in enumerate(trajectories):
        
        # Extract x and y coordinates
        x_coords = [point[0] for point in trajectory]
        y_coords = [point[1] for point in trajectory]
        
        # Get color for this particle type
        particle_color = type_colors[i]
        
        # Set line properties based on number of particles
        alpha_value = 0.5 if len(trajectories) > 20 else 0.7
        line_width = 1 if len(trajectories) > 20 else 2
        
        # Plot the trajectory
        plt.plot(x_coords, y_coords, color=particle_color, linewidth=line_width, alpha=alpha_value)
    
    # Add detector lines if provided
    if detector_positions:
        for x_pos in detector_positions:
            # Draw vertical line for detector
            plt.axvline(x=x_pos, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    
    # Add labels and title
    plt.xlabel('X Position (arbitrary units)', fontsize=14)
    plt.ylabel('Y Position (arbitrary units)', fontsize=14)
    plt.title(f'Particle Trajectories Simulation\n{len(trajectories)} Particles - DESY Ausbildung Application', 
              fontsize=16, fontweight='bold')
    
    # Add grid
    plt.grid(True, alpha=0.3)

    # Add legend for particle types
    from matplotlib.lines import Line2D
    
    legend_elements = []
    for ptype, props in PARTICLE_TYPES.items():
        legend_elements.append(Line2D([0], [0], color=props['color'], linewidth=2, label=f"{props['label']} ({ptype})"))
    
    plt.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.8)
    
    # Set equal aspect ratio (so circles look like circles)
    plt.axis('equal')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the figure BEFORE showing it
    plt.savefig('output/tracks.png', dpi=300, bbox_inches='tight')
    print(f"Plot saved to output/tracks.png ({len(trajectories)} particles)")
    
    # Show the plot
    plt.show()
    
# ============================================
# TEST THE PLOT FUNCTION
# ============================================

# print("\nTEST: PLOTTING TRAJECTORIES")
# print("=" * 50)
# print("Generating plot... (a window should appear)")
# print("=" * 50)

# Simulate 50 particles
# trajectories = simulate_particles(num_particles=50, max_time=10, time_steps=100)

# Define detector positions (vertical lines at x=5, 10, 15)
# detectors = [5, 10, 15]

# Plot the trajectories
# plot_trajectories(trajectories, detector_positions=detectors)

# print("Plot displayed successfully!")
# print("=" * 50)


# ============================================
# FUNCTION 4B: PLOT TRAJECTORIES 3D
# ============================================

def plot_trajectories_3d(trajectories, detector_positions=None):
    """
    Plots particle trajectories in 3D using matplotlib.
    
    Args:
        trajectories (list): List of trajectories from simulate_particles()
        detector_positions (list, optional): List of x-coordinates for detectors
    """
    
    # Import 3D toolkit
    from mpl_toolkits.mplot3d import Axes3D
    
    # Create a new figure with 3D projection
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
        # Plot each trajectory
    for i, trajectory in enumerate(trajectories):
        
        # Extract x, y, and z coordinates
        # For 3D, we'll use time as z-coordinate
        x_coords = [point[0] for point in trajectory]
        y_coords = [point[1] for point in trajectory]
        z_coords = list(range(len(trajectory)))  # Time steps as z
        
        # Use color from particle_info if available (we'll add this parameter later)
        # For now, use viridis colormap
        color = plt.cm.viridis(i / len(trajectories))
        ax.plot(x_coords, y_coords, z_coords, color=color, linewidth=1.5, alpha=0.7)
        
        # Mark the starting point
        ax.scatter(trajectory[0][0], trajectory[0][1], 0, c='red', s=50, marker='o')
    
    # Add detector planes if provided
    if detector_positions:
        for x_pos in detector_positions:
            # Create a mesh for the detector plane
            y_range = np.linspace(-50, 50, 10)
            z_range = np.linspace(0, len(trajectories[0]), 10)
            Y, Z = np.meshgrid(y_range, z_range)
            X = np.full_like(Y, x_pos)
            
            # Plot the detector plane
            ax.plot_surface(X, Y, Z, alpha=0.1, color='gray', label=f'Detector at x={x_pos}')
    
    # Add labels and title
    ax.set_xlabel('X Position', fontsize=12, labelpad=10)
    ax.set_ylabel('Y Position', fontsize=12, labelpad=10)
    ax.set_zlabel('Time Step', fontsize=12, labelpad=10)
    ax.set_title('Particle Trajectories Simulation (3D)\nDESY Ausbildung Application', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add grid
    ax.grid(True, alpha=0.3)

        # Add legend for particle types
    from matplotlib.lines import Line2D
    
    legend_elements = []
    for ptype, props in PARTICLE_TYPES.items():
        legend_elements.append(Line2D([0], [0], color=props['color'], linewidth=2, label=f"{props['label']} ({ptype})"))
    
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.8)
    
    # Set viewing angle
    ax.view_init(elev=20, azim=45)
    
    # Set viewing angle
    ax.view_init(elev=20, azim=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('output/tracks_3d.png', dpi=300, bbox_inches='tight')
    print("3D plot saved to output/tracks_3d.png")
    
    # Show the plot
    plt.show()


# ============================================
# FUNCTION 4C: ANIMATE TRAJECTORIES
# ============================================

def animate_trajectories(trajectories, particle_info=None, detector_positions=None, num_frames=50):
    """
    Creates an animation of particle trajectories.
    
    Args:
        trajectories (list): List of trajectories
        detector_positions (list, optional): X-coordinates of detectors
        num_frames (int): Number of frames in the animation
    """
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Initialize empty lines for each trajectory
    lines = []
    points = []
    
    for i in range(len(trajectories)):
        # Get color from particle info if available
        if particle_info is not None:
            color = particle_info[i]['color']
        else:
            color = plt.cm.viridis(i / len(trajectories))
        
        line, = ax.plot([], [], color=color, linewidth=1.5, alpha=0.6)
        point, = ax.plot([], [], 'o', color=color, markersize=6, alpha=0.7)
        lines.append(line)
        points.append(point)
    
    # Add detector lines
    if detector_positions:
        for x_pos in detector_positions:
            ax.axvline(x=x_pos, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    
    # Set axis limits
    all_x = [point[0] for traj in trajectories for point in traj]
    all_y = [point[1] for traj in trajectories for point in traj]
    
    margin = 10
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
    
    # Labels and title
    ax.set_xlabel('X Position', fontsize=12)
    ax.set_ylabel('Y Position', fontsize=12)
    ax.set_title('Particle Trajectories Animation\nDESY Ausbildung Application', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    # Add legend for particle types
    from matplotlib.lines import Line2D
    
    legend_elements = []
    for ptype, props in PARTICLE_TYPES.items():
        legend_elements.append(Line2D([0], [0], color=props['color'], linewidth=2, label=f"{props['label']} ({ptype})"))
    
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.8)
    
    ax.set_aspect('equal')
    ax.set_aspect('equal')
    
    # Add text for frame counter
    frame_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=10, 
                         verticalalignment='top')
    
    # Initialization function
    def init():
        for line, point in zip(lines, points):
            line.set_data([], [])
            point.set_data([], [])
        frame_text.set_text('')
        return lines + points + [frame_text]
    
    # Animation function
    def animate(frame):
        # Calculate how many points to show
        points_to_show = int(frame * len(trajectories[0]) / num_frames)
        
        for i, (line, point, trajectory) in enumerate(zip(lines, points, trajectories)):
            # Get points up to current frame
            x_data = [trajectory[j][0] for j in range(min(points_to_show, len(trajectory)))]
            y_data = [trajectory[j][1] for j in range(min(points_to_show, len(trajectory)))]
            
            # Update line
            line.set_data(x_data, y_data)
            
            # Update point (show only the last point)
            if len(x_data) > 0:
                point.set_data([x_data[-1]], [y_data[-1]])
            else:
                point.set_data([], [])
        
        # Update frame counter
        frame_text.set_text(f'Frame: {frame}/{num_frames}')
        
        return lines + points + [frame_text]
    
    # Create animation
    anim = FuncAnimation(fig, animate, init_func=init, frames=num_frames, 
                         interval=50, blit=True, repeat=False)
    
    # Save as GIF
    anim.save('output/animation.gif', writer=PillowWriter(fps=20), dpi=150)
    print("Animation saved to output/animation.gif")
    
    # Show the animation (optional, can be slow)
    # plt.show()
    
    return anim



# ============================================
# FUNCTION 5: DETECT PARTICLE HITS
# ============================================

def detect_hits(trajectories, detector_positions):
    """
    Detects where particles cross detector planes.
    
    Args:
        trajectories (list): List of particle trajectories
        detector_positions (list): X-coordinates of detector planes
    
    Returns:
        dict: Dictionary with hits for each detector
    """
    
    # Create dictionary to store hits for each detector
    hits = {}
    
    # Initialize hits for each detector
    for i, x_pos in enumerate(detector_positions):
        hits[f'detector_{i+1}'] = {
            'x_position': x_pos,
            'y_hits': [],
            'particle_indices': []
        }
    
    # Check each trajectory
    for particle_idx, trajectory in enumerate(trajectories):
        
        # Check each detector
        for det_idx, x_detector in enumerate(detector_positions):
            
            # Look for where trajectory crosses this detector
            for point_idx in range(len(trajectory) - 1):
                
                # Get two consecutive points
                x1, y1 = trajectory[point_idx]
                x2, y2 = trajectory[point_idx + 1]
                
                # Check if trajectory crosses the detector between these points
                if (x1 <= x_detector <= x2) or (x2 <= x_detector <= x1):
                    
                    # Calculate exact y position using linear interpolation
                    # Formula: y = y1 + (y2 - y1) * (x_detector - x1) / (x2 - x1)
                    if x2 != x1:  # Avoid division by zero
                        y_hit = y1 + (y2 - y1) * (x_detector - x1) / (x2 - x1)
                        
                        # Store the hit
                        detector_key = f'detector_{det_idx + 1}'
                        hits[detector_key]['y_hits'].append(y_hit)
                        hits[detector_key]['particle_indices'].append(particle_idx)
    
    return hits

# ============================================
# TEST THE DETECT HITS FUNCTION
# ============================================

# print("\nTEST: DETECTING PARTICLE HITS")
# print("=" * 50)

# Simulate particles
# trajectories = simulate_particles(num_particles=10, max_time=10, time_steps=100)

# Define detector positions
# detectors = [5, 10, 15]

# Detect hits
# hits = detect_hits(trajectories, detectors)

# Print results
# for detector_key, detector_data in hits.items():
#    print(f"\n{detector_key} (x={detector_data['x_position']}):")
#    print(f"  Number of hits: {len(detector_data['y_hits'])}")
#    if len(detector_data['y_hits']) > 0:
#         print(f"  Y positions: {[f'{y:.2f}' for y in detector_data['y_hits']]}")

# print("=" * 50)

# ============================================
# FUNCTION 6: CALCULATE STATISTICS
# ============================================

def calculate_statistics(hits):
    """
    Calculates statistics from detected hits.
    
    Args:
        hits (dict): Dictionary with hits from detect_hits()
    
    Returns:
        dict: Dictionary with statistics for each detector
    """
    
    stats = {}
    
    for detector_key, detector_data in hits.items():
        y_hits = detector_data['y_hits']
        
        if len(y_hits) > 0:
            # Calculate statistics
            stats[detector_key] = {
                'num_hits': len(y_hits),
                'mean_y': np.mean(y_hits),
                'std_y': np.std(y_hits),
                'min_y': np.min(y_hits),
                'max_y': np.max(y_hits)
            }
        else:
            stats[detector_key] = {
                'num_hits': 0,
                'mean_y': 0,
                'std_y': 0,
                'min_y': 0,
                'max_y': 0
            }
    
    return stats


# ============================================
# TEST THE STATISTICS FUNCTION
# ============================================

# print("\nTEST: CALCULATING STATISTICS")
# print("=" * 50)

# Calculate statistics
# stats = calculate_statistics(hits)

# Print results
# for detector_key, detector_stats in stats.items():
#    print(f"\n{detector_key}:")
#    print(f"  Number of hits: {detector_stats['num_hits']}")
#    print(f"  Mean Y position: {detector_stats['mean_y']:.2f}")
#    print(f"  Std deviation: {detector_stats['std_y']:.2f}")
#    print(f"  Range: [{detector_stats['min_y']:.2f}, {detector_stats['max_y']:.2f}]")

# print("=" * 50)

# ============================================
# FUNCTION 7: MAIN SIMULATION
# ============================================

def main_simulation():
    """
    Runs the complete particle track simulation.
    This is the main function that integrates all components.
    """
    
    print("=" * 70)
    print("PARTICLE TRACK SIMULATOR")
    print("DESY Ausbildung Application - Alejandra del Río B.")
    print("=" * 70)
    print()
    
    # Configuration
    NUM_PARTICLES = 50
    MAX_TIME = 10
    TIME_STEPS = 100
    DETECTOR_POSITIONS = [5, 10, 15]
    MAGNETIC_FIELD = 0.5   # NEW: Magnetic field strenght
    
    print(f"Configuration:")
    print(f"  - Number of particles: {NUM_PARTICLES}")
    print(f"  - Maximum time: {MAX_TIME}")
    print(f"  - Time steps: {TIME_STEPS}")
    print(f"  - Detector positions: {DETECTOR_POSITIONS}")
    print()
    
    # Step 1: Simulate particles
    print("Step 1: Simulating particle trajectories...")
    print(f" Particle types available: (list(PARTICLE_TYPES.keys())")
    trajectories, particle_info = simulate_particles(NUM_PARTICLES, MAX_TIME, TIME_STEPS, MAGNETIC_FIELD)
    print(f"  ✓ Generated {len(trajectories)} trajectories")
    print(f"    Magnetic field: {MAGNETIC_FIELD}")
    print()
    
    # Step 2: Detect hits
    print("Step 2: Detecting particle hits on detectors...")
    hits = detect_hits(trajectories, DETECTOR_POSITIONS)
    
    # Count total hits
    total_hits = 0
    for detector_key, detector_data in hits.items():
        total_hits += len(detector_data['y_hits'])
    
    print(f"  [OK] Detected {total_hits} total hits across {len(hits)} detectors")
    print()
    
    # Step 3: Calculate statistics
    print("Step 3: Calculating statistics...")
    stats = calculate_statistics(hits)
    
    for detector_key, detector_stats in stats.items():
        if detector_stats['num_hits'] > 0:
            print(f"  {detector_key}: {detector_stats['num_hits']} hits, "
                  f"mean Y = {detector_stats['mean_y']:.2f}, "
                  f"std = {detector_stats['std_y']:.2f}")
    print()
    
    # Step 4: Plot trajectories
    print("Step 4: Plotting trajectories...")
    plot_trajectories(trajectories, particle_info, detector_positions=DETECTOR_POSITIONS, show_legend=True)
    print(f"  [OK] 2D plot saved to output/tracks.png")
    
    # Step 4B: Plot trajectories in 3D
    print("Step 4B: Plotting trajectories in 3D...")
    plot_trajectories_3d(trajectories, detector_positions=DETECTOR_POSITIONS)
    print(f"  [OK] 3D plot saved to output/tracks_3d.png")
    print()

        # Step 4C: Create animation
    print("Step 4C: Creating animation...")
    animate_trajectories(trajectories, particle_info, detector_positions=DETECTOR_POSITIONS, num_frames=50)
    print(f"  [OK] Animation saved to output/animation.gif")
    print()
    
    # Step 5: Save data to file
    print("Step 5: Saving data to file...")
    save_data_to_csv(trajectories, hits, stats)
    print(f"  ✓ Data saved to output/data.csv")
    print()
    
    print("=" * 70)
    print("SIMULATION COMPLETE!")
    print("=" * 70)

    # Verification: Check some trajectory points
    print("\n=== VERIFICATION ===")
    print(f"First particle, first 5 points:")
    for i in range(5):
        x, y = trajectories[0][i]
        print(f"  Point {i}: ({x:.2f}, {y:.2f})")
    
    # Check if trajectories are curved (not straight lines)
    # For a straight line, the ratio y/x should be constant
    # For a curved line, it changes
    first_traj = trajectories[0]
    ratios = []
    for point in first_traj[1:10]:  # Skip origin (0,0)
        if abs(point[0]) > 0.1:  # Avoid division by zero
            ratios.append(point[1] / point[0])
    
    if len(ratios) > 1:
        ratio_change = abs(ratios[-1] - ratios[0])
        if ratio_change > 0.1:
            print(f"\n✓ Trajectories are CURVED (ratio change: {ratio_change:.2f})")
        else:
            print(f"\n⚠ Trajectories are STRAIGHT (ratio change: {ratio_change:.2f})")
    print("====================\n")


# ============================================
# FUNCTION 6B: SAVE DATA TO CSV
# ============================================

def save_data_to_csv(trajectories, hits, stats):
    """
    Saves simulation data to a CSV file.
    
    Args:
        trajectories (list): Particle trajectories
        hits (dict): Detected hits
        stats (dict): Statistics
    """
    
    # Open file for writing
    with open('output/data.csv', 'w') as f:
        
        # Write header
        f.write("Particle Track Simulation Data\n")
        f.write(f"Number of particles: {len(trajectories)}\n")
        f.write(f"Generated by: Alejandra del Río B.\n")
        f.write(f"Date: September 2026\n")
        f.write("\n")
        
        # Write statistics
        f.write("=== DETECTOR STATISTICS ===\n")
        f.write("Detector,Num_Hits,Mean_Y,Std_Y,Min_Y,Max_Y\n")
        
        for detector_key, detector_stats in stats.items():
            f.write(f"{detector_key},{detector_stats['num_hits']},"
                    f"{detector_stats['mean_y']:.4f},{detector_stats['std_y']:.4f},"
                    f"{detector_stats['min_y']:.4f},{detector_stats['max_y']:.4f}\n")
        
        f.write("\n")
        
        # Write sample of trajectories (first 5 particles, first 10 points)
        f.write("=== SAMPLE TRAJECTORIES (first 5 particles, first 10 points) ===\n")
        f.write("Particle_ID,Time_Step,X_Position,Y_Position\n")
        
        for particle_idx in range(min(5, len(trajectories))):
            for point_idx in range(min(10, len(trajectories[particle_idx]))):
                x, y = trajectories[particle_idx][point_idx]
                f.write(f"{particle_idx+1},{point_idx},{x:.6f},{y:.6f}\n")

# ============================================
# FUNCTION 8: COUNT PARTICLES BY TYPE
# ============================================

def count_particles_by_type(trajectories):
    """
    Counts how many particles of each type were simulated.
    
    Args:
        trajectories (list): List of trajectories
    
    Returns:
        dict: Dictionary with counts for each particle type
    """
    
    counts = {ptype: 0 for ptype in PARTICLE_TYPES.keys()}
    
    # This would require passing particle info with trajectories
    # For now, we'll just count total
    total = len(trajectories)
    
    return {'total': total, 'by_type': counts}


                
# ============================================
# RUN THE SIMULATION
# ============================================

if __name__ == "__main__":
    main_simulation()
