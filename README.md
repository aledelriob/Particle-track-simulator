# Particle Track Simulator

A Python-based simulation of particle trajectories in a detector system, created for a DESY Ausbildung application.

## Description

This program simulates particles emerging from a collision point and traveling through detector layers. It demonstrates basic concepts of particle physics, data analysis, and scientific visualization.

### Physics Background

The simulation models:
- Particle generation with random angles and velocities
- Linear trajectory propagation (x = v·t·cos(θ), y = v·t·sin(θ))
- Detector planes that register particle crossings
- Statistical analysis of detected hits

### Features

- Generate random particles with different properties
- Simulate particle trajectories through detector layers
- Detect and record particle hits on detectors
- Calculate statistics (mean, std, min, max)
- Visualize trajectories with matplotlib
- Save results to CSV file

## Technologies

- **Python 3.14**
- **NumPy** - Numerical computations
- **Matplotlib** - Data visualization

## Project Structure

The project has the following structure:

- `main.py` - Main simulation code with all functions
- `functions.py` - Helper functions (optional, for future expansion)
- `README.md` - This file (project documentation)
- `output/` - Folder for generated outputs
  - `tracks.png` - Trajectory visualization (saved automatically)
  - `data.csv` - Simulation data (saved automatically)

## Usage

Run the simulation:
```bash
python main.py
```

The program will:
1. Generate 50 particles with random trajectories
2. Calculate positions at 100 time steps
3. Detect hits on 3 detector planes
4. Calculate statistics for each detector
5. Save visualization to `output/tracks.png`
6. Save data to `output/data.csv`

## Output

### Trajectory Plot
The program generates a plot showing all particle trajectories with detector planes marked as vertical dashed lines.

### Data File
A CSV file containing:
- Detector statistics (hits, mean position, standard deviation)
- Sample trajectory data (first 5 particles, first 10 time points)

## Author

**Alejandra del Rio B.**  
Application for DESY Ausbildung 2027  
Fachinformatikerin für Anwendungsentwicklung

## License

This project is open source and available for educational purposes.

## Acknowledgments

This project was created as part of my application for an Ausbildung position at DESY (Deutsches Elektronen-Synchrotron) in Hamburg, Germany.