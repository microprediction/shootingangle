# demo1_tangent_circle_animation.py
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# --- Geometry setup ---
GOAL_WIDTH = 40.0     # distance between posts (meters)
FIELD_W    = 105.0    # field width (for drawing)
FIELD_H    = 68.0     # field height (for drawing)

# Place the goal on y=0 centered at x=0
A = np.array([-GOAL_WIDTH/2, 0.0])  # left post
B = np.array([ GOAL_WIDTH/2, 0.0])  # right post

# Choose a walk line x = x0, outside the posts (to the right of the right post)
x0 = GOAL_WIDTH/2 + 12.0
y_min, y_max = 0.5, 60.0

def shot_angle(P):
    """Angle APB at point P."""
    v1 = A - P
    v2 = B - P
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    if n1 == 0 or n2 == 0:
        return 0.0
    c = np.clip(np.dot(v1, v2) / (n1*n2), -1.0, 1.0)
    return math.acos(c)

def tangent_circle_through_posts(x0):
    """
    Circle through A,B tangent to the vertical line x=x0.
    By symmetry, center is on x=0: C=(0,cy), radius R=|x0|.
    From (W/2)^2 + cy^2 = R^2 = x0^2 -> cy = sqrt(x0^2 - (W/2)^2).
    Tangency point is (x0, cy).
    """
    W = GOAL_WIDTH
    cy_sq = x0**2 - (W/2)**2
    if cy_sq <= 0:
        return None, None, None
    cy = math.sqrt(cy_sq)
    C  = np.array([0.0, cy])
    R  = abs(x0)
    Pstar = np.array([x0, cy])
    return C, R, Pstar

# Precompute
C, R, Pstar = tangent_circle_through_posts(x0)
ys = np.linspace(y_min, y_max, 300)
angles = np.array([shot_angle(np.array([x0, y])) for y in ys])

# --- Figure + axes ---
fig, (ax_field, ax_plot) = plt.subplots(
    1, 2, figsize=(11, 4.8), gridspec_kw={"width_ratios": [3, 2]}
)

# Field view
ax_field.set_aspect('equal', adjustable='box')
ax_field.set_xlim(-FIELD_W/2, FIELD_W/2)
ax_field.set_ylim(-5, FIELD_H)
ax_field.set_title("Maximizing shot angle via tangent circle")

# Goal & lines
ax_field.plot([-GOAL_WIDTH/2, GOAL_WIDTH/2], [0, 0], 'k-', lw=4)
ax_field.plot([-FIELD_W/2, FIELD_W/2], [0, 0], color='gray', lw=1, alpha=0.5)
ax_field.plot([x0, x0], [0, FIELD_H], color='tab:blue', ls='--', alpha=0.7, label=f"x = {x0:.1f}")

# Circle through posts, tangent to walk line
if C is not None:
    circ = plt.Circle((C[0], C[1]), R, fill=False, color='tab:green', lw=2, alpha=0.85)
    ax_field.add_patch(circ)
    ax_field.plot([Pstar[0]], [Pstar[1]], 'o', color='tab:green', label="Tangent point $P^*$")

# Moving point + rays
walker, = ax_field.plot([], [], 'o', color='tab:blue')
rayA,   = ax_field.plot([], [], color='tab:red', lw=2)
rayB,   = ax_field.plot([], [], color='tab:red', lw=2)
angle_txt = ax_field.text(0.02, 0.98, "", transform=ax_field.transAxes, va='top', ha='left')

ax_field.legend(loc='upper right')

# Angle vs y plot
ax_plot.set_title("Shot angle vs. distance along walk")
ax_plot.set_xlabel("y (m)")
ax_plot.set_ylabel("angle (deg)")
ax_plot.grid(True, alpha=0.3)
ax_plot.plot(ys, np.degrees(angles), color='tab:purple', label="∠APB")
if Pstar is not None:
    ax_plot.plot([Pstar[1]], [np.degrees(shot_angle(Pstar))], 'o', color='tab:green', label="tangent point")
ax_plot.legend(loc='lower right')

def init():
    walker.set_data([], [])
    rayA.set_data([], [])
    rayB.set_data([], [])
    angle_txt.set_text("")
    return walker, rayA, rayB, angle_txt

def animate(i):
    frames = 120
    t = i / (frames - 1)
    y = y_min + t * (y_max - y_min)
    P = np.array([x0, y])
    walker.set_data([P[0]], [P[1]])
    rayA.set_data([P[0], A[0]], [P[1], A[1]])
    rayB.set_data([P[0], B[0]], [P[1], B[1]])
    angle_txt.set_text(f"y = {y:5.1f} m\n∠APB = {np.degrees(shot_angle(P)):5.2f}°")
    return walker, rayA, rayB, angle_txt

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=120, interval=40, blit=True)

# Save (no ffmpeg needed; use Pillow)
gif_path  = "shot_angle_tangent_circle.gif"
png_path  = "shot_angle_snapshot.png"
anim.save(gif_path, writer="pillow", fps=25)
fig.savefig(png_path, dpi=160, bbox_inches="tight")
print("Saved:", gif_path, "and", png_path)
