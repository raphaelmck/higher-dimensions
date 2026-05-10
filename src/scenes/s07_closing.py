from manim import *
import numpy as np


class ClosingSynthesis(ThreeDScene):
    def construct(self):
        accent = TEAL_C
        highlight = YELLOW_D

        # ── Pre-create all fixed-frame text (opacity=0, positioned, then revealed)
        def fixed(mob):
            mob.set_opacity(0)
            self.add_fixed_in_frame_mobjects(mob)
            return mob

        lbl_spatially = fixed(VGroup(
            Text("Spatially —", font_size=28, weight=BOLD, color=WHITE),
            Text("shapes, slices, and the structure of space itself", font_size=26, color=GRAY_B),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.55))

        lbl_math = fixed(VGroup(
            Text("Mathematically —", font_size=28, weight=BOLD, color=WHITE),
            Text("a language for any number of degrees of freedom", font_size=26, color=GRAY_B),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.55))

        lbl_comp = fixed(VGroup(
            Text("Computationally —", font_size=28, weight=BOLD, color=WHITE),
            Text("turning data into geometry", font_size=26, color=GRAY_B),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.55))

        line_a = fixed(Text(
            "Vectors are not just arrows.",
            font_size=38, weight=BOLD, color=WHITE,
        ).move_to(UP * 0.9))

        line_b = fixed(Text(
            "They are a way of giving shape to information.",
            font_size=32, color=GRAY_B,
        ).move_to(UP * 0.05))

        line_c = fixed(Text(
            "And once information has shape,",
            font_size=28, color=GRAY_C,
        ).move_to(DOWN * 0.7))

        line_d = fixed(Text(
            "we can measure it, project it, compare it, compress it, and learn from it.",
            font_size=26, color=GRAY_C,
        ).move_to(DOWN * 1.25))

        thesis = fixed(Text(
            "Dimensions turn information into geometry.",
            font_size=44, weight=BOLD, color=accent,
        ).move_to(ORIGIN))

        # ── Beat 1: Spatially — axes + sphere ────────────────────────────────
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1], z_range=[-2.5, 2.5, 1],
            x_length=5, y_length=5, z_length=5,
            axis_config={"include_ticks": False},
        )
        axes.get_x_axis().set_color(RED_C)
        axes.get_y_axis().set_color(GREEN_C)
        axes.get_z_axis().set_color(BLUE_C)

        sphere = Surface(
            lambda u, v: np.array([
                2.0 * np.cos(u) * np.cos(v),
                2.0 * np.cos(u) * np.sin(v),
                2.0 * np.sin(u),
            ]),
            u_range=[-PI / 2, PI / 2], v_range=[0, 2 * PI],
            resolution=(20, 40),
            fill_color=BLUE_E, fill_opacity=0.55,
            stroke_color=BLUE_B, stroke_width=0.5,
        )

        self.play(Create(axes), FadeIn(sphere), run_time=1.2)
        self.play(lbl_spatially.animate.set_opacity(1), run_time=0.5)
        self.begin_ambient_camera_rotation(rate=0.14)
        self.wait(4.0)
        self.stop_ambient_camera_rotation()

        # ── Beat 2: Mathematically — R^n formula and sliders ─────────────────
        self.play(
            FadeOut(sphere, axes),
            lbl_spatially.animate.set_opacity(0),
            run_time=0.6,
        )
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=0.8)

        # Vector formula
        vec_eq = MathTex(
            r"(x_1,\; x_2,\; \dots,\; x_n)", r"\;\in\;", r"\mathbb{R}^n",
            font_size=52,
        )
        vec_eq[2].set_color(accent)
        fixed(vec_eq)
        vec_eq.move_to(UP * 1.0)

        # Mini sliders — all in fixed-frame (screen) coordinates
        slider_colors = [RED_C, GREEN_C, BLUE_C, GOLD_C, PURPLE_C, WHITE]
        rng0 = np.random.default_rng(7)
        tracks, knobs = [], []
        sliders_group = VGroup()
        for i in range(6):
            c = slider_colors[i]
            pos = rng0.uniform(0.1, 0.9)
            track = Line(LEFT * 1.1, RIGHT * 1.1, color=c, stroke_width=2, stroke_opacity=0.5)
            knob  = Dot(track.point_from_proportion(pos), color=c, radius=0.085)
            lbl   = MathTex(f"x_{{{i+1}}}", font_size=22, color=c).next_to(track, LEFT, buff=0.14)
            tracks.append(track)
            knobs.append(knob)
            sliders_group.add(VGroup(track, knob, lbl))

        sliders_group.arrange(DOWN, buff=0.26).move_to(DOWN * 0.55)
        fixed(sliders_group)

        self.play(vec_eq.animate.set_opacity(1), run_time=0.7)
        self.play(sliders_group.animate.set_opacity(1), run_time=0.6)
        self.play(lbl_math.animate.set_opacity(1), run_time=0.4)

        def knob_anims(seed):
            rng = np.random.default_rng(seed)
            return [
                knob.animate.move_to(track.point_from_proportion(rng.uniform(0.05, 0.95)))
                for track, knob in zip(tracks, knobs)
            ]

        self.play(*knob_anims(42), run_time=1.2, rate_func=smooth)
        self.play(*knob_anims(99), run_time=1.0, rate_func=smooth)
        self.wait(0.8)

        # ── Beat 3: Computationally — swiss roll + data ───────────────────────
        self.play(
            vec_eq.animate.set_opacity(0),
            sliders_group.animate.set_opacity(0),
            lbl_math.animate.set_opacity(0),
            run_time=0.5,
        )
        self.move_camera(phi=65 * DEGREES, theta=-50 * DEGREES, run_time=1.0)

        def swiss_roll(u, v):
            t = 1.5 * PI + 3.0 * PI * u
            return np.array([t * np.cos(t) * 0.13, 2.0 * v - 1.0, t * np.sin(t) * 0.13])

        roll = Surface(
            swiss_roll,
            u_range=[0, 1], v_range=[0, 1],
            resolution=(30, 10),
            fill_color=BLUE_E, fill_opacity=0.65,
            stroke_color=BLUE_B, stroke_width=0.8,
        )

        rng2 = np.random.default_rng(42)
        pts_on = VGroup(*[
            Dot3D(
                swiss_roll(rng2.uniform(0.05, 0.95), rng2.uniform(0.05, 0.95))
                + rng2.normal(0, 0.035, 3),
                radius=0.038, color=accent,
            )
            for _ in range(65)
        ])
        pts_off = VGroup(*[
            Dot3D(
                swiss_roll(rng2.uniform(0.05, 0.95), rng2.uniform(0.05, 0.95))
                + rng2.normal(0, 0.35, 3),
                radius=0.030, color=GRAY_C,
            )
            for _ in range(22)
        ])
        all_pts = [*pts_off, *pts_on]

        self.play(
            Create(roll),
            LaggedStart(*[FadeIn(d) for d in all_pts], lag_ratio=0.014),
            run_time=1.8,
        )
        self.play(lbl_comp.animate.set_opacity(1), run_time=0.4)
        self.begin_ambient_camera_rotation(rate=-0.14)
        self.wait(3.5)
        self.stop_ambient_camera_rotation()

        # ── Final: Poetry then thesis ─────────────────────────────────────────
        self.play(
            FadeOut(roll, pts_on, pts_off),
            lbl_comp.animate.set_opacity(0),
            run_time=0.7,
        )
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=0.8)

        self.play(line_a.animate.set_opacity(1), run_time=0.8)
        self.wait(1.0)
        self.play(line_b.animate.set_opacity(1), run_time=0.8)
        self.wait(0.8)
        self.play(line_c.animate.set_opacity(1), run_time=0.6)
        self.play(line_d.animate.set_opacity(1), run_time=0.6)
        self.wait(2.0)

        self.play(
            line_a.animate.set_opacity(0),
            line_b.animate.set_opacity(0),
            line_c.animate.set_opacity(0),
            line_d.animate.set_opacity(0),
            run_time=0.7,
        )

        self.play(thesis.animate.set_opacity(1), run_time=1.2)
        self.wait(4.0)
