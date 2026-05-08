from manim import *
import numpy as np


class DimensionEscalation(ThreeDScene):
    def construct(self):
        accent = TEAL_C
        dim = WHITE  # default (unlit) axis color
        x_color = RED_C
        y_color = GREEN_C
        z_color = BLUE_C

        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=8, y_length=6, z_length=6,
        )

        # Get all three axis references up front so we can animate their color.
        x_axis = axes.get_x_axis()
        y_axis = axes.get_y_axis()
        z_axis = axes.get_z_axis()

        def make_fixed(tex, fs=42):
            m = MathTex(tex, font_size=fs).to_corner(UR, buff=0.55)
            m.set_opacity(0)
            self.add_fixed_in_frame_mobjects(m)
            return m

        label_1d = make_fixed(r"x \in \mathbb{R}")
        label_2d = make_fixed(r"(x,\, y) \in \mathbb{R}^2")
        label_3d = make_fixed(r"(x,\, y,\, z) \in \mathbb{R}^3")

        # ── 1D ────────────────────────────────────────────────────────────
        # x axis IS the entire space — create it already colored.
        x_axis.set_color(x_color)
        dot = Dot(axes.c2p(0, 0, 0), color=accent, radius=0.1)

        self.play(Create(x_axis), FadeIn(dot, scale=0.5), run_time=1.0)
        self.wait(0.2)

        self.play(dot.animate.move_to(axes.c2p(3, 0, 0)), run_time=0.7, rate_func=smooth)
        self.play(dot.animate.move_to(axes.c2p(-3, 0, 0)), run_time=1.0, rate_func=smooth)
        self.play(dot.animate.move_to(axes.c2p(2, 0, 0)), run_time=0.6, rate_func=smooth)

        self.play(FadeIn(label_1d), run_time=0.5)
        self.wait(0.5)

        # ── 2D ────────────────────────────────────────────────────────────
        # x_axis returns to neutral as the plane opens up.
        self.play(
            Create(y_axis),
            x_axis.animate.set_color(dim),
            FadeOut(label_1d),
            run_time=0.9,
        )
        self.wait(0.2)

        # Pure y: Δx=0, Δy=+2.5
        self.play(
            y_axis.animate.set_color(y_color),
            dot.animate.move_to(axes.c2p(2, 2.5, 0)),
            run_time=0.6, rate_func=smooth,
        )
        # Pure x: Δx=-4, Δy=0
        self.play(
            y_axis.animate.set_color(dim),
            x_axis.animate.set_color(x_color),
            dot.animate.move_to(axes.c2p(-2, 2.5, 0)),
            run_time=0.7, rate_func=smooth,
        )
        # Pure y: Δx=0, Δy=-4.5
        self.play(
            x_axis.animate.set_color(dim),
            y_axis.animate.set_color(y_color),
            dot.animate.move_to(axes.c2p(-2, -2, 0)),
            run_time=0.6, rate_func=smooth,
        )
        # Diagonal: both Δx and Δy non-zero
        self.play(
            x_axis.animate.set_color(x_color),
            dot.animate.move_to(axes.c2p(1.5, 1.5, 0)),
            run_time=0.7, rate_func=smooth,
        )
        # Reset axes, reveal label
        self.play(
            x_axis.animate.set_color(dim),
            y_axis.animate.set_color(dim),
            FadeIn(label_2d),
            run_time=0.5,
        )
        self.wait(0.5)

        # ── 3D ────────────────────────────────────────────────────────────
        dot_3d = Sphere(radius=0.12, resolution=(16, 16)).set_color(accent)
        dot_3d.move_to(axes.c2p(1.5, 1.5, 0))

        self.play(FadeOut(label_2d), run_time=0.4)
        self.move_camera(phi=70 * DEGREES, theta=-50 * DEGREES, run_time=1.8)
        self.play(
            ReplacementTransform(dot, dot_3d),
            Create(z_axis),
            run_time=1.0,
        )

        # Pure z: Δz=+2.5
        self.play(
            z_axis.animate.set_color(z_color),
            dot_3d.animate.move_to(axes.c2p(1.5, 1.5, 2.5)),
            run_time=0.7, rate_func=smooth,
        )
        # x and y: Δx=-3.5, Δy=-0.5, Δz=0
        self.play(
            z_axis.animate.set_color(dim),
            x_axis.animate.set_color(x_color),
            y_axis.animate.set_color(y_color),
            dot_3d.animate.move_to(axes.c2p(-2, 1, 2.5)),
            run_time=0.7, rate_func=smooth,
        )
        # y and z: Δx=0, Δy=-2.5, Δz=-4
        self.play(
            x_axis.animate.set_color(dim),
            z_axis.animate.set_color(z_color),
            dot_3d.animate.move_to(axes.c2p(-2, -1.5, -1.5)),
            run_time=0.8, rate_func=smooth,
        )
        # All three: Δx=+4, Δy=+3.5, Δz=+3.5
        self.play(
            x_axis.animate.set_color(x_color),
            dot_3d.animate.move_to(axes.c2p(2, 2, 2)),
            run_time=0.7, rate_func=smooth,
        )
        # Reset all, reveal label, hold
        self.play(
            x_axis.animate.set_color(dim),
            y_axis.animate.set_color(dim),
            z_axis.animate.set_color(dim),
            FadeIn(label_3d),
            run_time=0.6,
        )
        self.wait(1.5)

        # ── n-D ────────────────────────────────────────────────────────────
        # Axes dissolve while still in 3D perspective — implying we've stepped
        # beyond what can be drawn.  Label upgrades in the same motion.
        label_nd = MathTex(r"(x_1,\, x_2,\, \dots,\, x_n) \in \mathbb{R}^n", font_size=48)
        label_nd.to_edge(UP, buff=0.6)
        self.add_fixed_in_frame_mobjects(label_nd)
        label_nd.set_opacity(0)

        self.play(
            FadeOut(axes, dot_3d, label_3d),
            label_nd.animate.set_opacity(1),
            run_time=1.4,
        )
        self.wait(0.3)

        # ── Sliders ───────────────────────────────────────────────────────
        # More rows than fit — x_n bleeds off the bottom, implying no fixed limit.
        slider_labels = ["x_1", "x_2", "x_3", "x_4", "x_5", r"\vdots", "x_n"]
        slider_colors = [RED_C, GREEN_C, BLUE_C, GOLD_C, PURPLE_C, WHITE]
        sliders = VGroup()
        knobs = []  # (track, knob) pairs kept for animation rounds

        color_idx = 0
        for text in slider_labels:
            group = VGroup()
            lbl = MathTex(text, font_size=36)
            if text == r"\vdots":
                group.add(lbl)
            else:
                c = slider_colors[color_idx % len(slider_colors)]
                color_idx += 1
                track = Line(LEFT * 2.8, RIGHT * 2.8, color=c, stroke_width=2)
                prop = np.random.uniform(0.15, 0.85)
                knob = Dot(track.point_from_proportion(prop), color=c, radius=0.08)
                lbl.set_color(c)
                lbl.next_to(track, LEFT, buff=0.4)
                group.add(lbl, track, knob)
                knobs.append((track, knob))
            sliders.add(group)

        sliders.arrange(DOWN, buff=0.38)
        sliders.next_to(label_nd, DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(sliders)

        self.play(
            LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in sliders], lag_ratio=0.12),
            run_time=1.6,
        )

        def rand_knob_anims():
            return [
                knob.animate.move_to(track.point_from_proportion(np.random.uniform(0.1, 0.9)))
                for track, knob in knobs
            ]

        # Round 1: all move simultaneously — independent, no sync
        self.play(*rand_knob_anims(), run_time=1.2, rate_func=smooth)
        self.wait(0.15)

        # Round 2: staggered — watch each dimension act on its own schedule
        self.play(
            LaggedStart(
                *[knob.animate.move_to(track.point_from_proportion(np.random.uniform(0.1, 0.9)))
                  for track, knob in knobs],
                lag_ratio=0.3,
            ),
            run_time=2.0,
        )
        self.wait(0.15)

        # Round 3: simultaneous again — n values, all free, all different
        self.play(*rand_knob_anims(), run_time=1.0, rate_func=smooth)
        self.wait(2)
