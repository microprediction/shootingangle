# demo3_equal_time_slide_3d.py
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# --------------------------
# Geometry and helpers
# --------------------------
GOAL_WIDTH = 40.0
FIELD_W    = 105.0
FIELD_H    = 68.0

A = np.array([-GOAL_WIDTH/2, 0.0])  # left post (x,y)
B = np.array([ GOAL_WIDTH/2, 0.0])  # right post (x,y)

# Choose a walk line x = x0 outside the posts (to the right)
x0 = GOAL_WIDTH/2 + 12.0

def tangent_point(x0: float) -> np.ndarray:
    """
    Tangent point P* on x=x0 for the unique circle through A,B tangent to that line.
    Center is (0, cy), with (W/2)^2 + cy^2 = x0^2 => cy = sqrt(x0^2 - (W/2)^2).
    Tangency point is (x0, cy).
    """
    W = GOAL_WIDTH
    cy_sq = x0**2 - (W/2)**2
    if cy_sq <= 0:
        raise ValueError("x0 must be strictly outside the posts.")
    cy = math.sqrt(cy_sq)
    return np.array([x0, cy])

def solve_equal_time_tilt(P: np.ndarray, A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Find in-plane direction ghat (unit vector) such that frictionless slide times from rest
    along straight rails P->A and P->B are equal.
    Time t = sqrt(2 s / (g * (ghat·u))). Equality requires sA/(ghat·uA) = sB/(ghat·uB).
    Solve for direction g (2D) via linear system, then normalize.
    """
    EPS = 1e-12
    vA = A - P; sA = np.linalg.norm(vA); uA = vA / max(sA, EPS)
    vB = B - P; sB = np.linalg.norm(vB); uB = vB / max(sB, EPS)
    M   = np.stack([uA, uB], axis=0)  # 2x2
    rhs = np.array([sA, sB])
    try:
        g = np.linalg.solve(M, rhs)   # Any scalar multiple works; normalize next
    except np.linalg.LinAlgError:
        g = uA.copy()
    n = np.linalg.norm(g)
    return g / n if n > 0 else uA

def plane_height(x, y, ghat, scale=0.15):
    """
    Tilted plane: z = -scale * (ghat_x * x + ghat_y * y)
    IMPORTANT: minus sign makes z decrease along +ghat (i.e., ghat points DOWNHILL).
    """
    return -scale * (ghat[0]*x + ghat[1]*y)

# --------------------------
# Build scene
# --------------------------
Pstar = tangent_point(x0)
ghat  = solve_equal_time_tilt(Pstar, A, B)  # equal-time DOWNHILL direction (in-plane)
tilt_scale = 0.15                           # purely visual

# Rails (2D vectors), lengths and unit directions
vA = A - Pstar; sA = np.linalg.norm(vA); uA = vA / sA
vB = B - Pstar; sB = np.linalg.norm(vB); uB = vB / sB

# Accelerations along rails (proportional to downhill component)
# With z defined above, a_i ∝ ghat·u_i is positive when the rail points somewhat downhill.
aA = max(np.dot(ghat, uA), 1e-9)
aB = max(np.dot(ghat, uB), 1e-9)

# Common arrival time T (g cancels; work up to common factor)
T = math.sqrt(2.0 * sA / aA)  # equals sqrt(2 sB / aB) by construction

# Kinematics from rest under constant acceleration along each rail:
# s_i(t) = 0.5 a_i t^2. Using t = tau * T -> s_i(t) = s_i * tau^2 (same fraction for both).
def puck_position(tau, P, target):
    f = tau**2
    xy = P + f * (target - P)
    z  = plane_height(xy[0], xy[1], ghat, scale=tilt_scale)
    return xy[0], xy[1], z

# --------------------------
# Animation
# --------------------------
fig = plt.figure(figsize=(9.5, 7.0))
ax  = fig.add_subplot(111, projection='3d')
ax.set_title("Equal-time slide to the posts on a tilted field (3D)")

# Axes limits
pad = 10
x_lo, x_hi = -FIELD_W/2, FIELD_W/2
y_lo, y_hi = -5, FIELD_H
ax.set_xlim(x_lo, x_hi)
ax.set_ylim(y_lo, y_hi)

# Choose z range to fit the plane nicely
corners = np.array([
    [x_lo, y_lo],
    [x_lo, y_hi],
    [x_hi, y_lo],
    [x_hi, y_hi]
])
z_corners = [plane_height(x, y, ghat, tilt_scale) for x, y in corners]
z_min = min(z_corners) - 5
z_max = max(z_corners) + 20
ax.set_zlim(z_min, z_max)

# Plot a mesh for the tilted plane (local patch around the action)
X = np.linspace(-GOAL_WIDTH, GOAL_WIDTH, 50)
Y = np.linspace(0, 80, 50)
XX, YY = np.meshgrid(X, Y)
ZZ = plane_height(XX, YY, ghat, tilt_scale)
ax.plot_surface(XX, YY, ZZ, cmap="Greens", alpha=0.35, linewidth=0, antialiased=True)

# Draw goal line & posts as 3D objects (uprights)
def post_upright(x, y0=0.0, height=8.0, color='k', lw=3):
    z0 = plane_height(x, y0, ghat, tilt_scale)
    z1 = z0 + height
    ax.plot([x, x], [y0, y0], [z0, z1], color=color, lw=lw)

# Goal mouth (crossbar line at z of the plane at y=0)
gx = np.linspace(-GOAL_WIDTH/2, GOAL_WIDTH/2, 30)
gy = np.zeros_like(gx)
gz = plane_height(gx, gy, ghat, tilt_scale)
ax.plot(gx, gy, gz, color='k', lw=5, alpha=0.9)

# Uprights
post_upright(-GOAL_WIDTH/2)
post_upright( GOAL_WIDTH/2)

# Rails (as straight lines on the tilted plane)
rail_samp = np.linspace(0, 1, 50)
PA = np.stack([Pstar + t*(A - Pstar) for t in rail_samp], axis=0)  # (N,2)
PB = np.stack([Pstar + t*(B - Pstar) for t in rail_samp], axis=0)
ZA = plane_height(PA[:,0], PA[:,1], ghat, tilt_scale)
ZB = plane_height(PB[:,0], PB[:,1], ghat, tilt_scale)
ax.plot(PA[:,0], PA[:,1], ZA, color='tab:red',   lw=2, label="rail to left post")
ax.plot(PB[:,0], PB[:,1], ZB, color='tab:orange', lw=2, label="rail to right post")

# Tangent point marker
Pz = plane_height(Pstar[0], Pstar[1], ghat, tilt_scale)
ax.scatter([Pstar[0]], [Pstar[1]], [Pz], color='tab:green', s=60, label="tangent point $P^*$")

# Downhill direction arrow at P*
glen = 25.0
# Vector tip point in-plane (x,y), and its z on the plane
tip_x, tip_y = Pstar[0] + ghat[0]*glen, Pstar[1] + ghat[1]*glen
tip_z        = plane_height(tip_x, tip_y, ghat, tilt_scale)
ax.quiver(
    Pstar[0], Pstar[1], Pz,
    tip_x - Pstar[0], tip_y - Pstar[1], tip_z - Pz,
    color='tab:purple', linewidth=2, arrow_length_ratio=0.15, length=1.0, normalize=False
)
ax.text(tip_x, tip_y, tip_z + 5, "downhill", color='tab:purple')

# Two pucks
puckA, = ax.plot([], [], [], 'o', color='tab:red',   markersize=10)
puckB, = ax.plot([], [], [], 'o', color='tab:orange', markersize=10)

# Info text
txt = ax.text2D(0.02, 0.95, "", transform=ax.transAxes)

ax.legend(loc='upper right')

def init():
    puckA.set_data([], [])
    puckA.set_3d_properties([])
    puckB.set_data([], [])
    puckB.set_3d_properties([])
    txt.set_text("")
    return puckA, puckB, txt

def animate(frame):
    frames = 150
    tau = frame / (frames - 1)  # 0..1
    xA, yA, zA = puck_position(tau, Pstar, A)
    xB, yB, zB = puck_position(tau, Pstar, B)
    puckA.set_data([xA], [yA]); puckA.set_3d_properties([zA])
    puckB.set_data([xB], [yB]); puckB.set_3d_properties([zB])
    txt.set_text(f"equal-time tilt  |  τ = {tau:0.2f}  |  fraction along rail = τ² = {tau**2:0.2f}")
    return puckA, puckB, txt

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=150, interval=35, blit=True)

# Save GIF (Pillow writer, no ffmpeg required)
gif_out = "equal_time_slide_3d.gif"
png_out = "equal_time_slide_3d.png"
anim.save(gif_out, writer="pillow", fps=30)
fig.savefig(png_out, dpi=160, bbox_inches="tight")
print("Saved:", gif_out, "and", png_out)
