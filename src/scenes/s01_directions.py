from manim import *
import numpy as np


class DimensionEscalation(ThreeDScene):
    def construct(self):
        accent = TEAL_C

        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=8, y_length=6, z_length=6,
        )

        # All coordinate labels are fixed to screen space so the 3D camera
        # never rotates or clips them.  Start hidden; reveal with FadeIn.
        def make_fixed(tex, fs=42):
            m = MathTex(tex, font_size=fs).to_corner(UR, buff=0.55)
            m.set_opacity(0)
            self.add_fixed_in_frame_mobjects(m)
            return m

        label_1d = make_fixed(r"x \in \mathbb{R}")
        label_2d = make_fixed(r"(x,\, y) \in \mathbb{R}^2")
        label_3d = make_fixed(r"(x,\, y,\, z) \in \mathbb{R}^3")

        # ── 1D ────────────────────────────────────────────────────────────
        x_axis = axes.get_x_axis()
        dot = Dot(axes.c2p(0, 0, 0), color=accent, radius=0.1)

        self.play(Create(x_axis), FadeIn(dot, scale=0.5), run_time=1.0)
        self.wait(0.2)

        # Dot slides back and forth — only one degree of freedom
        self.play(dot.animate.move_to(axes.c2p(3, 0, 0)), run_time=0.7, rate_func=smooth)
        self.play(dot.animate.move_to(axes.c2p(-3, 0, 0)), run_time=1.0, rate_func=smooth)
        self.play(dot.animate.move_to(axes.c2p(2, 0, 0)), run_time=0.6, rate_func=smooth)

        self.play(FadeIn(label_1d), run_time=0.5)
        self.wait(0.5)

        # ── 2D ────────────────────────────────────────────────────────────
        y_axis = axes.get_y_axis()
        # Fade the 1D label out as the new axis appears
        self.play(Create(y_axis), FadeOut(label_1d), run_time=0.9)
        self.wait(0.2)

        # Show the new vertical freedom: y-move, x-move, diagonal
        self.play(dot.animate.move_to(axes.c2p(2, 2.5, 0)), run_time=0.6, rate_func=smooth)
        self.play(dot.animate.move_to(axes.c2p(-2, 2.5, 0)), run_time=0.7, rate_func=smooth)
        self.play(dot.animate.move_to(axes.c2p(-2, -2, 0)), run_time=0.6, rate_func=smooth)
        self.play(dot.animate.move_to(axes.c2p(1.5, 1.5, 0)), run_time=0.7, rate_func=smooth)

        self.play(FadeIn(label_2d), run_time=0.5)
        self.wait(0.5)

        # ── 3D ────────────────────────────────────────────────────────────
        dot_3d = Sphere(radius=0.12, resolution=(16, 16)).set_color(accent)
        dot_3d.move_to(axes.c2p(1.5, 1.5, 0))

        # Label out before camera rotates — avoids label fighting the 3D view
        self.play(FadeOut(label_2d), run_time=0.4)
        self.move_camera(phi=70 * DEGREES, theta=-50 * DEGREES, run_time=1.8)
        self.play(
            ReplacementTransform(dot, dot_3d),
            Create(axes.get_z_axis()),
            run_time=1.0,
        )

        # Move through 3D space to show the z freedom
        self.play(dot_3d.animate.move_to(axes.c2p(1.5, 1.5, 2.5)), run_time=0.7, rate_func=smooth)
        self.play(dot_3d.animate.move_to(axes.c2p(-2, 1, 2.5)), run_time=0.7, rate_func=smooth)
        self.play(dot_3d.animate.move_to(axes.c2p(-2, -1.5, -1.5)), run_time=0.8, rate_func=smooth)
        self.play(dot_3d.animate.move_to(axes.c2p(2, 2, 2)), run_time=0.7, rate_func=smooth)

        # Label in, then a brief orbit so the viewer feels the depth
        self.play(FadeIn(label_3d), run_time=0.6)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(1.5)
        self.stop_ambient_camera_rotation()

        # ── n-D ────────────────────────────────────────────────────────────
        # The 3D world fades while we stay in the 3D perspective — the axes
        # don't reset to flat, they simply dissolve, implying we've stepped
        # beyond what can be drawn.  The label upgrades in the same motion.
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
        # More rows than fit on screen — x_n disappears off the bottom edge,
        # making it visceral that there is no fixed upper limit.
        slider_labels = ["x_1", "x_2", "x_3", "x_4", "x_5", r"\vdots", "x_n"]
        sliders = VGroup()

        for text in slider_labels:
            group = VGroup()
            lbl = MathTex(text, font_size=36)
            if text == r"\vdots":
                group.add(lbl)
            else:
                track = Line(LEFT * 2.8, RIGHT * 2.8, color=GRAY_D, stroke_width=2)
                prop = np.random.uniform(0.15, 0.85)
                knob = Dot(track.point_from_proportion(prop), color=accent, radius=0.08)
                lbl.next_to(track, LEFT, buff=0.4)
                group.add(lbl, track, knob)
            sliders.add(group)

        sliders.arrange(DOWN, buff=0.38)
        sliders.next_to(label_nd, DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(sliders)

        self.play(
            LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in sliders], lag_ratio=0.12),
            run_time=1.6,
        )

        # Each knob moves to a new position and stays there — n independent
        # coordinates, each free to be anything, none affecting the others.
        knob_anims = []
        for group in sliders:
            if len(group) > 1:
                track, knob = group[1], group[2]
                knob_anims.append(
                    knob.animate.move_to(track.point_from_proportion(np.random.uniform(0.1, 0.9)))
                )
        self.play(*knob_anims, run_time=1.4, rate_func=smooth)
        self.wait(2)
