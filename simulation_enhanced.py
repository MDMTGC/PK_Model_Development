import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------
# Simulation Parameters
# -----------------------
time_steps = 1000            # Total number of time steps
num_individuals = 500        # Number of individuals in group simulation
coherence_threshold = 0.85   # Target threshold for sustained coherence

# Mean parameters for individual dynamics
decay_rate_mean = 0.01           # Mean natural decay per time step
reinforcement_factor_mean = 0.05 # Mean reinforcement factor from group dynamics

# Standard deviations for individual heterogeneity
decay_rate_std = 0.002           
reinforcement_std = 0.01         

# Model coefficients
k1 = 0.5             # Biophoton feedback coefficient
alpha = 0.2          # Coefficient linking coherence to biophoton emission
B0 = 1.0             # Baseline biophoton emission
kE = 0.1             # Environmental resonance coefficient
k_group = 0.05       # Group synchronization reinforcement coefficient

# -----------------------
# Environmental Resonance Setup
# -----------------------
dt = 1.0                        # Time step in seconds
t = np.arange(0, time_steps * dt, dt)
schumann_amplitude = 0.1        # Amplitude of environmental effect
# Generate a sine wave representing Schumann resonance (scaled to simulation time)
schumann_resonance_effect = schumann_amplitude * np.sin(2 * np.pi * 7.83 * t / time_steps)

# -----------------------
# Initialization
# -----------------------
# Random initial coherence levels for each individual
coherence_levels = np.random.uniform(0.5, 0.7, num_individuals)

# Generate individual heterogeneous parameters
decay_rates = np.random.normal(decay_rate_mean, decay_rate_std, num_individuals)
reinforcement_factors = np.random.normal(reinforcement_factor_mean, reinforcement_std, num_individuals)

# Store average coherence over time
avg_coherence_over_time = []

# -----------------------
# Simulation Loop
# -----------------------
for i in range(time_steps):
    avg_coherence = np.mean(coherence_levels)
    avg_coherence_over_time.append(avg_coherence)
    
    # Compute individual biophoton rates
    biophoton_rates = B0 + alpha * coherence_levels
    
    # Group synchronization: pull individuals toward the group average
    group_reinforcement = k_group * (avg_coherence - coherence_levels)
    
    # Environmental resonance effect for this time step
    env_effect = kE * schumann_resonance_effect[i] * (1 - coherence_levels)
    
    # Stochastic noise
    noise = np.random.normal(0, 0.005, num_individuals)
    
    # Update differential change in coherence
    dC_dt = k1 * biophoton_rates * (1 - coherence_levels) - decay_rates * coherence_levels \
            + group_reinforcement + env_effect + noise
    coherence_levels += dC_dt * dt
    
    # Keep coherence within [0, 1]
    coherence_levels = np.clip(coherence_levels, 0, 1)

# -----------------------
# Visualization
# -----------------------
sns.set_style("whitegrid")

# Plot 1: Average Group Coherence Over Time
plt.figure(figsize=(12, 6))
plt.plot(t, avg_coherence_over_time, label="Average Group Coherence", lw=2)
plt.axhline(y=coherence_threshold, color='r', linestyle='--', label="Coherence Threshold")
plt.xlabel("Time (s)")
plt.ylabel("Coherence Level")
plt.title("Enhanced Simulation of Group Coherence Dynamics")
plt.legend()
plt.show()

# Plot 2: Histogram of Final Individual Coherence Levels
plt.figure(figsize=(8, 5))
sns.histplot(coherence_levels, bins=30, kde=True, color="skyblue")
plt.axvline(x=coherence_threshold, color='r', linestyle='--', label="Coherence Threshold")
plt.xlabel("Coherence Level")
plt.ylabel("Frequency")
plt.title("Distribution of Final Coherence Levels")
plt.legend()
plt.show()
