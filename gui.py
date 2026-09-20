# ============================================
# PARTICLE TRACK SIMULATOR - GUI
# ============================================
# Graphical User Interface for DESY application
#
# Author: Alejandra del Río B.
# Date: September 2026
# ============================================

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os

# Import simulation functions from main.py
from main import simulate_particles, plot_trajectories, plot_trajectories_3d, \
                 animate_trajectories, detect_hits, calculate_statistics, \
                 save_data_to_csv, PARTICLE_TYPES

# ============================================
# MAIN APPLICATION CLASS
# ============================================

class ParticleSimulatorGUI:
    """
    Graphical User Interface for Particle Track Simulator
    """
    
    def __init__(self, root):
        """
        Initialize the GUI
        """
        
        self.root = root
        self.root.title("Particle Track Simulator - DESY Ausbildung")
        self.root.geometry("800x700")
        
        # Variables
        self.num_particles = tk.IntVar(value=50)
        self.max_time = tk.DoubleVar(value=10.0)
        self.time_steps = tk.IntVar(value=100)
        self.magnetic_field = tk.DoubleVar(value=0.5)
        self.detector_positions = tk.StringVar(value="5, 10, 15")
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        """
        Create all GUI widgets
        """
        
        # Title
        title_label = tk.Label(
            self.root,
            text="🔬 Particle Track Simulator",
            font=("Helvetica", 20, "bold"),
            pady=10
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            self.root,
            text="DESY Ausbildung Application - Alejandra del Río B.",
            font=("Helvetica", 12),
            pady=5
        )
        subtitle_label.pack()
        
        # Separator
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # Configuration frame
        config_frame = ttk.LabelFrame(self.root, text="⚙️ Configuration", padding=15)
        config_frame.pack(fill='x', padx=20, pady=10)
        
        # Number of particles
        ttk.Label(config_frame, text="Number of Particles:").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Spinbox(config_frame, from_=1, to=500, textvariable=self.num_particles, width=10).grid(row=0, column=1, padx=10, pady=5)
        
        # Maximum time
        ttk.Label(config_frame, text="Maximum Time:").grid(row=1, column=0, sticky='w', pady=5)
        ttk.Spinbox(config_frame, from_=1, to=100, textvariable=self.max_time, width=10).grid(row=1, column=1, padx=10, pady=5)
        
        # Time steps
        ttk.Label(config_frame, text="Time Steps:").grid(row=2, column=0, sticky='w', pady=5)
        ttk.Spinbox(config_frame, from_=10, to=1000, textvariable=self.time_steps, width=10).grid(row=2, column=1, padx=10, pady=5)
        
        # Magnetic field
        ttk.Label(config_frame, text="Magnetic Field (Z):").grid(row=3, column=0, sticky='w', pady=5)
        ttk.Spinbox(config_frame, from_=-5.0, to=5.0, increment=0.1, textvariable=self.magnetic_field, width=10).grid(row=3, column=1, padx=10, pady=5)
        
        # Detector positions
        ttk.Label(config_frame, text="Detector Positions (X):").grid(row=4, column=0, sticky='w', pady=5)
        ttk.Entry(config_frame, textvariable=self.detector_positions, width=30).grid(row=4, column=1, padx=10, pady=5)
        ttk.Label(config_frame, text="e.g., 5, 10, 15", font=("Helvetica", 9, "italic")).grid(row=4, column=2, padx=5)
        
        # Separator
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=10)
        
        # Run simulation button
        run_button = tk.Button(
            buttons_frame,
            text="▶️ Run Simulation",
            command=self.run_simulation,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 12, "bold"),
            padx=20,
            pady=10
        )
        run_button.pack(side='left', padx=10)
        
        # Plot 2D button
        plot2d_button = tk.Button(
            buttons_frame,
            text="📊 Plot 2D",
            command=self.plot_2d,
            bg="#2196F3",
            fg="white",
            font=("Helvetica", 12),
            padx=15,
            pady=10
        )
        plot2d_button.pack(side='left', padx=10)
        
        # Plot 3D button
        plot3d_button = tk.Button(
            buttons_frame,
            text="🎯 Plot 3D",
            command=self.plot_3d,
            bg="#FF9800",
            fg="white",
            font=("Helvetica", 12),
            padx=15,
            pady=10
        )
        plot3d_button.pack(side='left', padx=10)
        
        # Animate button
        animate_button = tk.Button(
            buttons_frame,
            text="🎬 Animate",
            command=self.animate,
            bg="#9C27B0",
            fg="white",
            font=("Helvetica", 12),
            padx=15,
            pady=10
        )
        animate_button.pack(side='left', padx=10)
        
        # Separator
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=20, pady=10)
        
        # Status frame
        status_frame = ttk.LabelFrame(self.root, text="📈 Status", padding=15)
        status_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Status label
        self.status_label = tk.Label(
            status_frame,
            text="Ready to simulate",
            font=("Helvetica", 11),
            fg="gray",
            pady=10
        )
        self.status_label.pack()
        
        # Results text
        self.results_text = tk.Text(status_frame, height=8, width=80, font=("Courier", 10))
        self.results_text.pack(pady=10, padx=5)
        
        # Particle types info
        types_frame = ttk.LabelFrame(self.root, text="🔬 Particle Types", padding=10)
        types_frame.pack(fill='x', padx=20, pady=10)
        
        # Display particle types
        types_info = ""
        for ptype, props in PARTICLE_TYPES.items():
            types_info += f"{props['label']} ({ptype}): charge={props['charge']}, mass={props['mass']}, color={props['color']}\n"
        
        types_label = tk.Label(
            types_frame,
            text=types_info,
            font=("Courier", 10),
            justify='left',
            anchor='w'
        )
        types_label.pack()
        
    def run_simulation(self):
        """
        Run the particle simulation
        """
        
        try:
            # Parse detector positions
            detector_positions = [float(x.strip()) for x in self.detector_positions.get().split(',')]
            
            # Update status
            self.status_label.config(text="Running simulation...", fg="blue")
            self.root.update()
            
            # Run simulation
            self.trajectories, self.particle_info = simulate_particles(
                num_particles=self.num_particles.get(),
                max_time=self.max_time.get(),
                time_steps=self.time_steps.get(),
                magnetic_field=self.magnetic_field.get()
            )
            
            # Detect hits
            self.hits = detect_hits(self.trajectories, detector_positions)
            
            # Calculate statistics
            self.stats = calculate_statistics(self.hits)
            
            # Save data
            save_data_to_csv(self.trajectories, self.hits, self.stats)
            
            # Display results
            self.display_results(detector_positions)
            
            # Update status
            self.status_label.config(text="✓ Simulation complete!", fg="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed:\n{str(e)}")
            self.status_label.config(text="✗ Error occurred", fg="red")
    
    def display_results(self, detector_positions):
        """
        Display simulation results in text box
        """
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Write results
        results = f"=== SIMULATION RESULTS ===\n"
        results += f"Particles: {self.num_particles.get()}\n"
        results += f"Magnetic Field: {self.magnetic_field.get()}\n"
        results += f"Detectors at X: {detector_positions}\n\n"
        
        results += f"=== DETECTOR HITS ===\n"
        for detector_key, detector_data in self.hits.items():
            num_hits = len(detector_data['y_hits'])
            results += f"{detector_key}: {num_hits} hits\n"
        
        results += f"\n=== STATISTICS ===\n"
        for detector_key, detector_stats in self.stats.items():
            if detector_stats['num_hits'] > 0:
                results += f"{detector_key}: mean Y = {detector_stats['mean_y']:.2f}, std = {detector_stats['std_y']:.2f}\n"
        
        self.results_text.insert(tk.END, results)
    
    def plot_2d(self):
        """
        Plot 2D trajectories
        """
        
        try:
            if not hasattr(self, 'trajectories'):
                messagebox.showwarning("Warning", "Run simulation first!")
                return
            
            detector_positions = [float(x.strip()) for x in self.detector_positions.get().split(',')]
            
            self.status_label.config(text="Plotting 2D...", fg="blue")
            self.root.update()
            
            plot_trajectories(self.trajectories, self.particle_info, detector_positions, show_legend=True)
            
            self.status_label.config(text="✓ 2D plot saved!", fg="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Plot failed:\n{str(e)}")
            self.status_label.config(text="✗ Error occurred", fg="red")
    
    def plot_3d(self):
        """
        Plot 3D trajectories
        """
        
        try:
            if not hasattr(self, 'trajectories'):
                messagebox.showwarning("Warning", "Run simulation first!")
                return
            
            detector_positions = [float(x.strip()) for x in self.detector_positions.get().split(',')]
            
            self.status_label.config(text="Plotting 3D...", fg="blue")
            self.root.update()
            
            plot_trajectories_3d(self.trajectories, detector_positions)
            
            self.status_label.config(text="✓ 3D plot saved!", fg="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Plot failed:\n{str(e)}")
            self.status_label.config(text="✗ Error occurred", fg="red")
    
    def animate(self):
        """
        Create animation
        """
        
        try:
            if not hasattr(self, 'trajectories'):
                messagebox.showwarning("Warning", "Run simulation first!")
                return
            
            detector_positions = [float(x.strip()) for x in self.detector_positions.get().split(',')]
            
            self.status_label.config(text="Creating animation...", fg="blue")
            self.root.update()
            
            animate_trajectories(self.trajectories, self.particle_info, detector_positions, num_frames=50)
            
            self.status_label.config(text="✓ Animation saved!", fg="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Animation failed:\n{str(e)}")
            self.status_label.config(text="✗ Error occurred", fg="red")


# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """
    Main function to run the GUI
    """
    
    # Create main window
    root = tk.Tk()
    
    # Create application
    app = ParticleSimulatorGUI(root)
    
    # Run main loop
    root.mainloop()


# ============================================
# RUN THE APPLICATION
# ============================================

if __name__ == "__main__":
    main()
