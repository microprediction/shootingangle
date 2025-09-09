# Shooting Angle and Equal-Time Tilt

This repo demonstrates two elegant facts about maximizing a soccer shot angle and the associated **equal-time tilt** argument.

## Demos

- **Demo 1:** [Tangent circle animation](./demo1_tangent_circle_animation.py)  
  Shows that the best shooting point along a vertical walk line is the tangency point of the unique circle through the posts tangent to that line.

- **Demo 2:** [Equal-time tilt (2D math check)](./demo2_equal_time_tilt.py)  
  Verifies numerically that there exists a tilt direction of the field for which pucks sliding to each post arrive simultaneously.

- **Demo 3:** [Equal-time slide in 3D](./demo3_equal_time_slide_3d.py)  
  Visualizes the tilted field in 3D with two pucks sliding down straight rails to the posts, hitting at the same time.

Each demo saves a `.gif` and `.png` snapshot in the repo folder.

---

## Equal-Time Proof

### Setup

- Goal posts:
  \[
  A=\Big(-\tfrac{W}{2},0\Big),\quad B=\Big(\tfrac{W}{2},0\Big).
  \]
- Starting point \(P\).
- Rails: straight lines \(P\to A\), \(P\to B\).
- Downhill unit vector: \(\hat{\mathbf g}\).

Rail directions and lengths:
\[
\mathbf v_A=A-P,\; s_A=\|\mathbf v_A\|,\; \hat{\mathbf u}_A=\tfrac{\mathbf v_A}{s_A},
\]
\[
\mathbf v_B=B-P,\; s_B=\|\mathbf v_B\|,\; \hat{\mathbf u}_B=\tfrac{\mathbf v_B}{s_B}.
\]

### Times under tilt

Along rail \(i\):
\[
a_i = g(\hat{\mathbf g}\cdot \hat{\mathbf u}_i),\qquad
t_i=\sqrt{\tfrac{2s_i}{a_i}}.
\]

### Equal-time condition

We want \(t_A=t_B\), i.e.
\[
\frac{s_A}{\hat{\mathbf g}\cdot \hat{\mathbf u}_A}
=\frac{s_B}{\hat{\mathbf g}\cdot \hat{\mathbf u}_B}.
\]

Equivalently,
\[
(\hat{\mathbf g}\cdot \hat{\mathbf u}_A):(\hat{\mathbf g}\cdot \hat{\mathbf u}_B)=s_A:s_B.
\]

### Solution

This is a linear system for \(\hat{\mathbf g}\):
\[
\begin{bmatrix}
\hat{\mathbf u}_A^\top\\[2pt]\hat{\mathbf u}_B^\top
\end{bmatrix}\hat{\mathbf g}
=\lambda\begin{bmatrix}s_A\\s_B\end{bmatrix},\;\lambda>0.
\]

Because \(\hat{\mathbf u}_A,\hat{\mathbf u}_B\) are independent, there is a unique solution direction up to sign. Choosing the sign so both dot products are positive yields a downhill direction \(\hat{\mathbf g}\). With this choice:
\[
t_A=t_B.
\]

Thus the “equal-time tilt” always exists. Note that the downhill vector generally has a **sideways component** — it is not purely along the field’s length.

---

## Running

```bash
pip install matplotlib numpy
python demo1_tangent_circle_animation.py
python demo2_equal_time_tilt.py
python demo3_equal_time_slide_3d.py
