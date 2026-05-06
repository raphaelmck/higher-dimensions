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

        # ── 1D ────────────────────────────────────────────────────────────
        # "a dimension is one independent direction of change"
        x_axis = axes.get_x_axis()
        dot = Dot(axes.c2p(0, 0, 0), color=accent, radius=0.1)
        label_1d = MathTex(r"x \in \mathbb{R}").next_to(dot, UP, buff=0.4)

        self.play(Create(x_axis), run_time=1.2)
        self.play(FadeIn(dot, scale=0.5), Write(label_1d))
        self.wait(0.3)

        # "On a line, you need one number" — dot slides back and forth, locked to x
        self.play(dot.animate.move_to(axes.c2p(3, 0, 0)), run_time=0.7, rate_func=smooth)
        self.play(dot.animate.move_to(axes.c2p(-3, 0, 0)), run_time=1.0, rate_func=smooth)
        self.play(dot.animate.move_to(axes.c2p(2, 0, 0)), run_time=0.6, rate_func=smooth)
        self.wait(0.4)

        # ── 2D ────────────────────────────────────────────────────────────
        # "In a plane, you need two"
        y_axis = axes.get_y_axis()
        label_2d = MathTex(r"(x, y) \in \mathbb{R}^2").next_to(dot, UR, buff=0.2)

        self.play(Create(y_axis), run_time=0.9)
        self.wait(0.2)

        # Show the new vertical freedom: first move along y only, then x only,
        # then a diagonal — making "two independent directions" visible
        self.play(dot.animate.move_to(axes.c2p(2, 2.5, 0)), run_time=0.6, rate_func=smooth)
        self.play(dot.animate.move_to(axes.c2p(-2, 2.5, 0)), run_time=0.7, rate_func=smooth)
        self.play(dot.animate.move_to(axes.c2p(-2, -2, 0)), run_time=0.6, rate_func=smooth)
        self.play(dot.animate.move_to(axes.c2p(1.5, 1.5, 0)), run_time=0.7, rate_func=smooth)

        self.play(TransformMatchingTex(label_1d, label_2d), run_time=0.6)
        self.wait(0.5)

        # ── 3D ────────────────────────────────────────────────────────────
        # "In space, you need three"
        dot_3d = Sphere(radius=0.12, resolution=(16, 16)).set_color(accent)
        dot_3d.move_to(axes.c2p(1.5, 1.5, 0))

        label_3d = MathTex(r"(x, y, z) \in \mathbb{R}^3")
        label_3d.to_corner(UR, buff=1)
        self.add_fixed_in_frame_mobjects(label_3d)
        label_3d.set_opacity(0)

        # Camera opens into 3D while z-axis grows
        self.move_camera(phi=70 * DEGREES, theta=-50 * DEGREES, run_time=1.8)
        self.play(
            ReplacementTransform(dot, dot_3d),
            Create(axes.get_z_axis()),
            run_time=1.0,
        )

        # "need three" — move through 3D space, showing the new z freedom
        self.play(dot_3d.animate.move_to(axes.c2p(1.5, 1.5, 2.5)), run_time=0.7, rate_func=smooth)
        self.play(dot_3d.animate.move_to(axes.c2p(-2, 1, 2.5)), run_time=0.7, rate_func=smooth)
        self.play(dot_3d.animate.move_to(axes.c2p(-2, -1.5, -1.5)), run_time=0.8, rate_func=smooth)
        self.play(dot_3d.animate.move_to(axes.c2p(2, 2, 2)), run_time=0.7, rate_func=smooth)

        # Slow orbit so the viewer can feel the 3D depth
        self.begin_ambient_camera_rotation(rate=0.25)
        label_3d.set_opacity(1)
        self.play(TransformMatchingTex(label_2d, label_3d), run_time=0.8)
        self.wait(2.0)
        self.stop_ambient_camera_rotation()

        # ── n-D ────────────────────────────────────────────────────────────
        # "the idea does not stop there … lives in an n-dimensional space"
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=1.5)

        label_nd = MathTex(r"(x_1, x_2, \dots, x_n) \in \mathbb{R}^n").scale(1.3)
        label_nd.move_to(UP * 2)
        self.add_fixed_in_frame_mobjects(label_nd)

        self.play(
            FadeOut(axes, dot_3d),
            ReplacementTransform(label_3d, label_nd),
            run_time=1.5,
        )

        # ── Sliders ───────────────────────────────────────────────────────
        # "imagination gets stuck at three. The math does not."
        sliders = VGroup()
        slider_labels = ["x_1", "x_2", "x_3", r"\vdots", "x_n"]

        for text in slider_labels:
            group = VGroup()
            lbl = MathTex(text).scale(0.8)
            if text == r"\vdots":
                group.add(lbl)
            else:
                track = Line(LEFT * 2, RIGHT * 2, color=GRAY_D, stroke_width=2)
                prop = np.random.uniform(0.15, 0.85)
                knob = Dot(track.point_from_proportion(prop), color=accent, radius=0.08)
                lbl.next_to(track, LEFT, buff=0.5)
                group.add(lbl, track, knob)
            sliders.add(group)

        sliders.arrange(DOWN, buff=0.4).next_to(label_nd, DOWN, buff=0.8)
        self.add_fixed_in_frame_mobjects(sliders)

        self.play(
            LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in sliders], lag_ratio=0.15),
            run_time=1.8,
        )

        # Each knob moves independently — illustrating independent dimensions
        knob_anims = []
        for group in sliders:
            if len(group) > 1:
                track, knob = group[1], group[2]
                knob_anims.append(
                    knob.animate.move_to(track.point_from_proportion(np.random.uniform(0.1, 0.9)))
                )
        self.play(*knob_anims, run_time=2.0, rate_func=there_and_back)
        self.wait(2)
