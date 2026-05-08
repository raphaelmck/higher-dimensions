from manim import *
import numpy as np


class FlatlandAnalogy(ThreeDScene):
    def construct(self):
        plane_color = BLUE_E
        sphere_color = TEAL
        intersection_color = YELLOW
        sphere_radius = 2.0
        sphere_z = ValueTracker(3.0)

        # ── BEAT 1: Flatland setup ─────────────────────────────────────────
        # Establish the limitation before the mystery.
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        grid = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1],
            background_line_style={"stroke_opacity": 0.2},
        )
        self.play(FadeIn(grid), run_time=0.8)

        observer = Dot(ORIGIN, color=WHITE, radius=0.12)
        x_arr = Arrow(ORIGIN, RIGHT * 1.8, color=RED_C, buff=0, stroke_width=4)
        y_arr = Arrow(ORIGIN, UP * 1.8, color=GREEN_C, buff=0, stroke_width=4)
        x_lbl = MathTex("x", color=RED_C, font_size=36).next_to(x_arr.get_end(), UP, buff=0.15)
        y_lbl = MathTex("y", color=GREEN_C, font_size=36).next_to(y_arr.get_end(), RIGHT, buff=0.15)

        # z is inaccessible — show it as a faded question
        z_lbl = VGroup(
            MathTex("z", color=GRAY_B, font_size=36),
            Text("?", color=GRAY_B, font_size=32),
        ).arrange(RIGHT, buff=0.05).next_to(observer, UR, buff=0.3).set_opacity(0.4)

        self.play(
            FadeIn(observer),
            GrowArrow(x_arr), FadeIn(x_lbl),
            GrowArrow(y_arr), FadeIn(y_lbl),
            run_time=1.2,
        )
        self.play(FadeIn(z_lbl), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(VGroup(observer, x_arr, y_arr, x_lbl, y_lbl, z_lbl)), run_time=0.6)

        # ── BEAT 2: Mystery — something appears from nowhere ───────────────
        intersection = Circle(radius=0.001, color=intersection_color, stroke_width=4)

        def update_circle(c):
            z = sphere_z.get_value()
            if abs(z) < sphere_radius:
                r = np.sqrt(max(sphere_radius**2 - z**2, 0))
                c.set_opacity(1)
                c.become(Circle(radius=max(r, 0.001), color=intersection_color, stroke_width=4))
            else:
                c.set_opacity(0)

        intersection.add_updater(update_circle)
        self.add(intersection)

        # Drop in segments so the narrative beats land cleanly
        self.play(sphere_z.animate.set_value(sphere_radius * 0.8), run_time=0.8, rate_func=linear)
        self.play(sphere_z.animate.set_value(0.0), run_time=2.0, rate_func=linear)

        # Freeze at maximum — ask the question before the reveal
        self.wait(0.6)
        question = Text("What could cause this?", font_size=32, color=WHITE).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(question), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(question), run_time=0.3)

        self.play(sphere_z.animate.set_value(-sphere_radius * 0.8), run_time=2.0, rate_func=linear)
        self.play(sphere_z.animate.set_value(-3.0), run_time=0.8, rate_func=linear)
        self.wait(0.5)

        # ── BEAT 3: 3D Reveal ─────────────────────────────────────────────
        # Reset and let the camera rotate to show the hidden cause.
        sphere_z.set_value(3.0)
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2.0)

        plane = Rectangle(width=10, height=10, color=plane_color, fill_opacity=0.3)
        sphere = Sphere(radius=sphere_radius, color=sphere_color, fill_opacity=0.15)
        sphere.add_updater(lambda m: m.move_to(OUT * sphere_z.get_value()))

        self.play(FadeIn(plane), FadeIn(sphere), run_time=1.0)
        self.wait(0.5)

        # Formula appears only after the reveal — mystery first, math second
        formula = MathTex(r"r = \sqrt{R^2 - z^2}", font_size=42).to_corner(UR, buff=0.55)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(FadeIn(formula), run_time=0.6)
        self.wait(0.4)

        # Second pass is faster — viewer now sees the cause
        self.play(sphere_z.animate.set_value(-3.0), run_time=3.5, rate_func=linear)
        self.wait(0.8)

        # ── BEAT 4: Generalization ─────────────────────────────────────────
        intersection.clear_updaters()
        sphere.clear_updaters()
        self.play(FadeOut(grid, plane, sphere, intersection, formula), run_time=1.0)

        bridge = Text(
            "Higher dimensions leave lower-dimensional traces.",
            font_size=34, color=WHITE,
        ).to_edge(UP, buff=0.7)
        self.add_fixed_in_frame_mobjects(bridge)
        self.play(Write(bridge), run_time=1.2)
        self.wait(0.8)

        # ── Tesseract projection ───────────────────────────────────────────
        def wireframe_cube(size, color=WHITE):
            verts = [np.array([x, y, z]) * size / 2 for x in [-1, 1] for y in [-1, 1] for z in [-1, 1]]
            lines = VGroup(*[
                Line(verts[i], verts[j], color=color, stroke_width=2)
                for i in range(8) for j in range(i + 1, 8)
                if np.isclose(np.sum(np.abs(verts[i] - verts[j])), size)
            ])
            return lines, verts

        outer_size = ValueTracker(0.01)
        inner_size = ValueTracker(0.01)
        tesseract_group = VGroup()

        def update_tesseract(mob):
            out_lines, out_v = wireframe_cube(outer_size.get_value(), TEAL)
            in_lines, in_v = wireframe_cube(inner_size.get_value(), BLUE)
            conn = VGroup(*[
                Line(out_v[i], in_v[i], color=GRAY_B, stroke_opacity=0.5, stroke_width=2)
                for i in range(8)
            ])
            mob.become(VGroup(out_lines, in_lines, conn).move_to(DOWN * 0.5))

        tesseract_group.add_updater(update_tesseract)
        self.add(tesseract_group)
        self.play(
            outer_size.animate.set_value(4),
            inner_size.animate.set_value(1.5),
            run_time=1.5,
        )

        proj_label = Text(
            "projection — not the object itself", font_size=26, color=GRAY_B,
        ).to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(proj_label)
        self.play(FadeIn(proj_label), run_time=0.5)

        self.play(
            outer_size.animate.set_value(1.5),
            inner_size.animate.set_value(4),
            run_time=3,
            rate_func=there_and_back,
        )
        self.wait(2)
