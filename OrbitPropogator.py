import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp

# CONSTANTS 
MU = 398600.4418      # earth's gravitational parameter (km^3 / s^2)
R_EARTH = 6378.137    # earth's equatorial radius (km)
J2 = 1.08263e-3       # J2 perturbation coefficient (dimensionless)

def orbital_derivatives_j2(t, state):
    """
    Calculates the derivatives of the state vector including J2 perturbations.
    state = [x, y, z, vx, vy, vz]
    """
    x, y, z, vx, vy, vz = state
    r = np.array([x, y, z])
    r_mag = np.linalg.norm(r)
    
    # 2-body gravity acceleration
    a_2body = -MU * r / (r_mag ** 3)
    
    # J2 perturbation acceleration formulas
    z_sq = z**2
    r_sq = r_mag**2
    
    # common coefficient multiplier
    factor = (1.5 * J2 * MU * R_EARTH**2) / (r_mag**5)
    
    ax_j2 = factor * x * (5 * z_sq / r_sq - 1)
    ay_j2 = factor * y * (5 * z_sq / r_sq - 1)
    az_j2 = factor * z * (5 * z_sq / r_sq - 3)
    
    # total Acceleration = 2-body gravity + J2 perturbation
    ax = a_2body[0] + ax_j2
    ay = a_2body[1] + ay_j2
    az = a_2body[2] + az_j2
    
    return [vx, vy, vz, ax, ay, az]

def main():
    # INITIAL CONDITIONS
    # high inclination orbit (60 degrees) to show J2 nodal precession
    r_0 = np.array([7000.0, 0.0, 0.0])       # Position (km)
    v_0 = np.array([0.0, 3.77, 6.53])        # Velocity (km/s) inclined vector
    
    initial_state = np.concatenate([r_0, v_0])
    
    # propagate for 24 hours (=86,400 seconds) to show orbital drift
    t_start = 0
    t_end = 86400
    t_span = (t_start, t_end)
    
    t_eval = np.linspace(t_start, t_end, 800) # downsample frames slightly for smooth animation
    
    print("Propagating orbit with J2 physics...")
    solution = solve_ivp(
        orbital_derivatives_j2, 
        t_span, 
        initial_state, 
        t_eval=t_eval, 
        rtol=1e-8, 
        atol=1e-8
    )
    
    x_vals = solution.y[0]
    y_vals = solution.y[1]
    z_vals = solution.y[2]
    
    # PLOT 
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    
    # plot earth
    u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
    xs = R_EARTH * np.cos(u) * np.sin(v)
    ys = R_EARTH * np.sin(u) * np.sin(v)
    zs = R_EARTH * np.cos(v)
    ax.plot_wireframe(xs, ys, zs, color="#1f77b4", alpha=0.2, linewidth=0.8)
    
    # ANIMATION
    # active trajectory line
    orbit_line, = ax.plot([], [], [], color="#00FFCC", alpha=0.8, linewidth=1.5, label="Trajectory (with J2)")
    # spacecraft indicator dot
    spacecraft_dot, = ax.plot([], [], [], color="#FF3366", marker="o", markersize=6, label="Satellite")
    
    # legend and axis Labels
    ax.legend(loc="upper right")
    ax.set_title("24-Hour Propagation with J2 Equatorial Drift", color="white", fontsize=14, pad=20)
    ax.set_xlabel("X (km)", color="gray")
    ax.set_ylabel("Y (km)", color="gray")
    ax.set_zlabel("Z (km)", color="gray")
    
    # fix axes limits for uniform scaling
    max_range = np.array([x_vals.max()-x_vals.min(), y_vals.max()-y_vals.min(), z_vals.max()-z_vals.min()]).max() / 1.8
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)
    
    # grid lines faint
    ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0.05)
    ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0.05)
    ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0.05)

    # ANIMATION FUNCTIONS
    def init():
        orbit_line.set_data([], [])
        orbit_line.set_3d_properties([])
        spacecraft_dot.set_data([], [])
        spacecraft_dot.set_3d_properties([])
        return orbit_line, spacecraft_dot

    def update(frame):
        # update trailing orbit line
        orbit_line.set_data(x_vals[:frame], y_vals[:frame])
        orbit_line.set_3d_properties(z_vals[:frame])
        
        # update current spacecraft position
        spacecraft_dot.set_data([x_vals[frame]], [y_vals[frame]])
        spacecraft_dot.set_3d_properties([z_vals[frame]])
        
        # rotate camera viewpoint
        ax.view_init(elev=20, azim=frame * 0.2)
        
        return orbit_line, spacecraft_dot

    print("Running interactive animation...")
    # blit = False because rotating the camera requires redrawing the background axes
    ani = FuncAnimation(
        fig, 
        update, 
        frames=len(x_vals), 
        init_func=init, 
        interval=25, 
        repeat=True
    )
    
    plt.show()

if __name__ == "__main__":
    main()