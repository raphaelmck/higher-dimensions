from manim import *
import numpy as np
import sys
sys.path.insert(0, "/Users/raphaelmichnik/projects/youtube/higher-dimensions/src")
from style import BACKGROUND, ACCENT

# ── palette ──────────────────────────────────────────────────────────────────
BG          = BACKGROUND          # "#0F0F0F"
GLOW_CORE   = "#AAEEFF"           # bright ice-blue center
GLOW_MID    = ACCENT              # "#58C4DD"
GLOW_EDGE   = "#1A3A50"           # deep teal fade
DOT_COL     = "#FFFFFF"
EQ_COL      = "#2A5A70"           # very dim teal for the equation ghost
TITLE_COL   = "#FFFFFF"


class Thumbnail(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG

        # ── Swiss-roll manifold ───────────────────────────────────────────────
        def swiss_roll(u, v):
            t = u * 3 * PI + 1.5 * PI        # t ∈ [1.5π, 4.5π]
            x = t * np.cos(t) * 0.13
            z = t * np.sin(t) * 0.13
            y = (v - 0.5) * 2.2
            return np.array([x, y, z])

        surf = Surface(
            swiss_roll,
            u_range=[0, 1],
            v_range=[0, 1],
            resolution=(60, 20),
            fill_opacity=0.85,
            stroke_opacity=0.0,
        )
        surf.set_color_by_rgba_func(
            lambda p: color_to_rgba(
                interpolate_color(GLOW_EDGE, GLOW_MID, 0.5 + 0.5 * np.sin(p[0] * 1.5 + p[2] * 1.5)),
                alpha=0.90,
            )
        )

        # ── Ambient points on the surface ─────────────────────────────────────
        rng = np.random.default_rng(42)
        n_pts = 180
        us = rng.uniform(0, 1, n_pts)
        vs = rng.uniform(0, 1, n_pts)
        dots = VGroup()
        for u_val, v_val in zip(us, vs):
            p = swiss_roll(u_val, v_val)
            # vary brightness: inner coil brighter
            t_val = u_val * 3 * PI + 1.5 * PI
            bright = np.clip(t_val / (4.5 * PI), 0.3, 1.0)
            col = interpolate_color(ManimColor(GLOW_EDGE), ManimColor(GLOW_CORE), bright)
            d = Dot3D(point=p, radius=0.028, color=col)
            d.set_opacity(rng.uniform(0.55, 1.0))
            dots.add(d)

        # ── Ghost vector equation ─────────────────────────────────────────────
        eq = MathTex(
            r"\mathbf{x} = (x_1,\, x_2,\, \ldots,\, x_n)",
            font_size=52,
            color=EQ_COL,
        )
        eq.set_opacity(0.45)
        eq.to_edge(DOWN, buff=1.0)

        # ── Main title ────────────────────────────────────────────────────────
        title = Text(
            "INFORMATION HAS SHAPE",
            font="SF Pro Display",
            weight=BOLD,
            font_size=64,
            color=TITLE_COL,
        )
        title.to_edge(UP, buff=0.45)

        # subtle underline accent
        line = Line(
            title.get_left() + DOWN * 0.18,
            title.get_right() + DOWN * 0.18,
            stroke_width=2.5,
            color=GLOW_MID,
        ).set_opacity(0.6)

        # ── Camera ────────────────────────────────────────────────────────────
        self.set_camera_orientation(
            phi=72 * DEGREES,
            theta=-55 * DEGREES,
            zoom=1.15,
        )

        # ── Add everything ────────────────────────────────────────────────────
        self.add(surf, dots)
        self.add_fixed_in_frame_mobjects(eq, title, line)

        self.wait(0.01)
