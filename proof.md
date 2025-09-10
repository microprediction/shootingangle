# Equal-Time Tilt Direction for the Tangent Point

## Setup

- Goal posts at
  \[
  A=\Big(-\tfrac{W}{2},0\Big),\qquad B=\Big(\tfrac{W}{2},0\Big).
  \]
- Starting point \(P\) (e.g. the tangent point on \(x=x_0\)).
- Rails: straight segments \(P\to A\), \(P\to B\).
- Downhill (gravity) direction: unit vector \(\hat{\mathbf g}\in\mathbb{S}^1\).

Let
\[
\mathbf v_A = A-P,\quad s_A=\|\mathbf v_A\|,\quad \hat{\mathbf u}_A=\frac{\mathbf v_A}{s_A},
\]
\[
\mathbf v_B = B-P,\quad s_B=\|\mathbf v_B\|,\quad \hat{\mathbf u}_B=\frac{\mathbf v_B}{s_B}.
\]

## Times under tilt

Along each rail, the downhill acceleration is
\[
a_A = g\,(\hat{\mathbf g}\cdot \hat{\mathbf u}_A),\qquad
a_B = g\,(\hat{\mathbf g}\cdot \hat{\mathbf u}_B).
\]

From rest, time to traverse length \(s\) is
\[
t = \sqrt{\tfrac{2s}{a}}.
\]

So
\[
t_A = \sqrt{\frac{2 s_A}{g(\hat{\mathbf g}\cdot \hat{\mathbf u}_A)}},\qquad
t_B = \sqrt_
