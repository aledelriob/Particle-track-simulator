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


# ============================================
# FUNCTION 1: CREATE A PARTICLE
# ============================================

def create_particle():
    """
    Creates a particle with random properties.
    
    Returns:
        dict: Dictionary with particle properties
    """
    
    # Generate random angle between 0 and 360 degrees
    angle_degrees = random.uniform(0, 360)
    
    # Convert to radians (Python uses radians, not degrees)
    # Formula: radians = degrees * (π / 180)
    angle_radians = angle_degrees * (np.pi / 180)
    
    # Random velocity between 1 and 10 (arbitrary units)
    velocity = random.uniform(1, 10)
    
    # Create dictionary with particle properties
    particle = {
        'angle_degrees': angle_degrees,
        'angle_radians': angle_radians,
        'velocity': velocity,
        'x_initial': 0,  # Always starts from origin
        'y_initial': 0
    }
    
    return particle


# ============================================
# TEST THE FUNCTION
# ============================================

# Create a test particle
test_particle = create_particle()

# Print its properties
print("=" * 50)
print("TEST PARTICLE")
print("=" * 50)
print(f"Angle: {test_particle['angle_degrees']:.2f} degrees")
print(f"Angle in radians: {test_particle['angle_radians']:.2f} rad")
print(f"Velocity: {test_particle['velocity']:.2f}")
print(f"Initial position: ({test_particle['x_initial']}, {test_particle['y_initial']})")
print("=" * 50)

# ============================================
# FUNCTION 2: CALCULATE PARTICLE POSITION
# ============================================

def calculate_position(particle, time):
    """
    Calculates the position of a particle at a given time.
    
    Args:
        particle (dict): Dictionary with particle properties
        time (float): Time in arbitrary units
    
    Returns:
        tuple: (x, y) position coordinates
    """
    
    # Extract particle properties
    velocity = particle['velocity']
    angle = particle['angle_radians']
    x0 = particle['x_initial']
    y0 = particle['y_initial']
    
    # Calculate position using physics formulas
    # x = x0 + v * t * cos(θ)
    # y = y0 + v * t * sin(θ)
    x = x0 + velocity * time * np.cos(angle)
    y = y0 + velocity * time * np.sin(angle)
    
    return (x, y)


# ============================================
# TEST THE POSITION FUNCTION
# ============================================

# Create a particle
test_particle = create_particle()

# Calculate position at different times
print("\nTEST: PARTICLE POSITION AT DIFFERENT TIMES")
print("=" * 50)

for t in [0, 1, 2, 3, 4, 5]:
    position = calculate_position(test_particle, t)
    print(f"Time t={t}: Position = ({position[0]:.2f}, {position[1]:.2f})")

print("=" * 50)

# ============================================
# FUNCTION 3: SIMULATE MULTIPLE PARTICLES
# ============================================

def simulate_particles(num_particles, max_time, time_steps):
    """
    Simulates multiple particles and calculates their trajectories.
    
    Args:
        num_particles (int): Number of particles to simulate
        max_time (float): Maximum time to simulate
        time_steps (int): Number of time points to calculate
    
    Returns:
        list: List of trajectories, each trajectory is a list of (x, y) positions
    """
    
    # Create list to store all trajectories
    all_trajectories = []
    
    # Generate and simulate each particle
    for i in range(num_particles):
        
        # Create a new particle
        particle = create_particle()
        
        # Create list to store this particle's trajectory
        trajectory = []
        
        # Calculate position at different times
        for t in range(time_steps):
            # Calculate time value (0, 1, 2, ..., max_time)
            current_time = t * (max_time / time_steps)
            
            # Calculate position at this time
            position = calculate_position(particle, current_time)
            
            # Add position to trajectory
            trajectory.append(position)
        
        # Add this trajectory to the list
        all_trajectories.append(trajectory)
    
    return all_trajectories

# ============================================
# TEST THE SIMULATION FUNCTION
# ============================================

# Simulate 5 particles for 10 time units with 100 time steps
print("\nTEST: SIMULATING 5 PARTICLES")
print("=" * 50)

trajectories = simulate_particles(num_particles=5, max_time=10, time_steps=100)

print(f"Number of trajectories: {len(trajectories)}")
print(f"Points per trajectory: {len(trajectories[0])}")
print(f"First trajectory, first point: {trajectories[0][0]}")
print(f"First trajectory, last point: {trajectories[0][-1]}")
print("=" * 50)


# ============================================
# FUNCTION 4: PLOT TRAJECTORIES
# ============================================

def plot_trajectories(trajectories, detector_positions=None, show_legend=True):
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
    for i, trajectory in enumerate(trajectories):
        
        # Extract x and y coordinates
        x_coords = [point[0] for point in trajectory]
        y_coords = [point[1] for point in trajectory]
        
        # Plot the trajectory with a random color
        # For many particles, use thin lines with low alpha
        alpha_value = 0.5 if len(trajectories) > 20 else 0.7
        line_width = 1 if len(trajectories) > 20 else 2
        
        plt.plot(x_coords, y_coords, linewidth=line_width, alpha=alpha_value)
        
        # Mark the starting point (only for first few particles)
        if i < 5:
            plt.plot(trajectory[0][0], trajectory[0][1], 'o', markersize=6, color='red', alpha=0.5)
    
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
    
    # Add legend only if requested and not too many particles
    if show_legend and len(trajectories) <= 10:
        plt.legend()
    
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

print("\nTEST: PLOTTING TRAJECTORIES")
print("=" * 50)
print("Generating plot... (a window should appear)")
print("=" * 50)

# Simulate 50 particles
trajectories = simulate_particles(num_particles=50, max_time=10, time_steps=100)

# Define detector positions (vertical lines at x=5, 10, 15)
detectors = [5, 10, 15]

# Plot the trajectories
plot_trajectories(trajectories, detector_positions=detectors)

print("Plot displayed successfully!")
print("=" * 50)


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

print("\nTEST: DETECTING PARTICLE HITS")
print("=" * 50)

# Simulate particles
trajectories = simulate_particles(num_particles=10, max_time=10, time_steps=100)

# Define detector positions
detectors = [5, 10, 15]

# Detect hits
hits = detect_hits(trajectories, detectors)

# Print results
for detector_key, detector_data in hits.items():
    print(f"\n{detector_key} (x={detector_data['x_position']}):")
    print(f"  Number of hits: {len(detector_data['y_hits'])}")
    if len(detector_data['y_hits']) > 0:
        print(f"  Y positions: {[f'{y:.2f}' for y in detector_data['y_hits']]}")

print("=" * 50)

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

print("\nTEST: CALCULATING STATISTICS")
print("=" * 50)

# Calculate statistics
stats = calculate_statistics(hits)

# Print results
for detector_key, detector_stats in stats.items():
    print(f"\n{detector_key}:")
    print(f"  Number of hits: {detector_stats['num_hits']}")
    print(f"  Mean Y position: {detector_stats['mean_y']:.2f}")
    print(f"  Std deviation: {detector_stats['std_y']:.2f}")
    print(f"  Range: [{detector_stats['min_y']:.2f}, {detector_stats['max_y']:.2f}]")

print("=" * 50)

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
    
    print(f"Configuration:")
    print(f"  - Number of particles: {NUM_PARTICLES}")
    print(f"  - Maximum time: {MAX_TIME}")
    print(f"  - Time steps: {TIME_STEPS}")
    print(f"  - Detector positions: {DETECTOR_POSITIONS}")
    print()
    
    # Step 1: Simulate particles
    print("Step 1: Simulating particle trajectories...")
    trajectories = simulate_particles(NUM_PARTICLES, MAX_TIME, TIME_STEPS)
    print(f"  ✓ Generated {len(trajectories)} trajectories")
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
    plot_trajectories(trajectories, detector_positions=DETECTOR_POSITIONS, show_legend=False)
    print(f"  ✓ Plot saved to output/tracks.png")
    print()
    
    # Step 5: Save data to file
    print("Step 5: Saving data to file...")
    save_data_to_csv(trajectories, hits, stats)
    print(f"  ✓ Data saved to output/data.csv")
    print()
    
    print("=" * 70)
    print("SIMULATION COMPLETE!")
    print("=" * 70)


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
# RUN THE SIMULATION
# ============================================

if __name__ == "__main__":
    main_simulation()
