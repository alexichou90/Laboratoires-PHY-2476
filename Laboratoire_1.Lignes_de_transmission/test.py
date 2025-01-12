import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

def calculTension(V_1, V_2, z, t, alpha, beta, omega):
    return V_1 * np.exp(alpha * z) * np.exp(1j * omega * t + beta * z) + V_2 * np.exp(-alpha * z) * np.exp(1j * omega * t - beta * z)

def calculCourant(V_1, V_2, Z, Y, z, t, alpha, beta, omega):
    return (-V_1 / np.sqrt(Z / Y)) * np.exp(alpha * z) * np.exp(1j * omega * t + beta * z) + (V_2 / np.sqrt(Z / Y)) * np.exp(-alpha * z) * np.exp(1j * omega * t - beta * z)

# Constants and parameters
V_1 = 1.0  # Example voltage 1
V_2 = 1  # Example voltage 2
Z = 1.0    # Impedance
Y = 1.0    # Admittance
alpha = 0.1
beta = 0.2
omega = 1.0
t_values = np.linspace(0, 10, 100)  # Time from 0 to 10
z_values = np.linspace(0, 5, 5)    # Different z values

# Create plots
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Plot V(z,t) against t for different values of z
for z in z_values:
    V_values = np.real([calculTension(V_1, V_2, z, t, alpha, beta, omega) for t in t_values])
    axs[0].plot(t_values, V_values, label=f'z = {z}')
axs[0].set_title("V(z,t) vs t for different z values")
axs[0].set_xlabel("Time (t)")
axs[0].set_ylabel("Voltage V(z,t)")
axs[0].legend()

# Plot i(z,t) against t for different values of z
for z in z_values:
    i_values = np.real([calculCourant(V_1, V_2, Z, Y, z, t, alpha, beta, omega) for t in t_values])
    axs[1].plot(t_values, i_values, label=f'z = {z}')
axs[1].set_title("i(z,t) vs t for different z values")
axs[1].set_xlabel("Time (t)")
axs[1].set_ylabel("Current i(z,t)")
axs[1].legend()

plt.tight_layout()
plt.show()

# 3D plots
fig = plt.figure(figsize=(10, 8))

# Plot V(z,t) against t and z
ax1 = fig.add_subplot(121, projection='3d')
T, Z_vals = np.meshgrid(t_values, z_values)
V_vals = np.real(calculTension(V_1, V_2, Z_vals, T, alpha, beta, omega))
ax1.plot_surface(Z_vals, T, V_vals, cmap='viridis')
ax1.set_title("V(z,t) vs t and z")
ax1.set_xlabel("z (Length of wire)")
ax1.set_ylabel("t (Time)")
ax1.set_zlabel("Voltage V(z,t)")

# Plot i(z,t) against t and z
ax2 = fig.add_subplot(122, projection='3d')
i_vals = np.real(calculCourant(V_1, V_2, Z, Y, Z_vals, T, alpha, beta, omega))
ax2.plot_surface(Z_vals, T, i_vals, cmap='viridis')
ax2.set_title("i(z,t) vs t and z")
ax2.set_xlabel("z (Length of wire)")
ax2.set_ylabel("t (Time)")
ax2.set_zlabel("Current i(z,t)")

plt.tight_layout()
plt.show()
