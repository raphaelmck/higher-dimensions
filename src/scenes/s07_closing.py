from manim import *
import numpy as np


class ClosingSynthesis(Scene):
    def construct(self):
        accent = TEAL_C

        # ═══ PHASE 1: THREE PANELS — sequential reveal ═══════════════════════

        pw, ph = 4.0, 3.6

        def make_box():
            return RoundedRectangle(
                width=pw, height=ph, corner_radius=0.18,
                color=GRAY_D, fill_color=BLACK, fill_opacity=0.10, stroke_width=1.2,
            )

        box1, box2, box3 = make_box(), make_box(), make_box()
        panel_row = VGroup(box1, box2, box3).arrange(RIGHT, buff=0.38).move_to(UP * 0.85)
        c1, c2, c3 = box1.get_center(), box2.get_center(), box3.get_center()

        lbl1 = Text("Spatially",       font_size=22, weight=BOLD, color=WHITE).next_to(box1, DOWN, buff=0.22)
        lbl2 = Text("Mathematically",  font_size=22, weight=BOLD, color=WHITE).next_to(box2, DOWN, buff=0.22)
        lbl3 = Text("Computationally", font_size=22, weight=BOLD, color=WHITE).next_to(box3, DOWN, buff=0.22)
        sub1 = Text("shapes, slices, and the structure of space", font_size=15, color=GRAY_B).next_to(lbl1, DOWN, buff=0.08)
        sub2 = Text("a language for any degrees of freedom",      font_size=15, color=GRAY_B).next_to(lbl2, DOWN, buff=0.08)
        sub3 = Text("turning data into geometry",                 font_size=15, color=GRAY_B).next_to(lbl3, DOWN, buff=0.08)

        # ── Panel 1 visual: isometric cube ────────────────────────────────────
        s = 0.82
        dir_x = s * np.array([np.sqrt(3) / 2,  -0.5, 0])
        dir_y = s * np.array([-np.sqrt(3) / 2, -0.5, 0])
        dir_z = s * np.array([0, 1.0, 0])
        iso_o = c1 - np.array([0, 0.21, 0])
        vA, vB, vC = iso_o, iso_o + dir_x, iso_o + dir_y
        vD, vE, vF = iso_o + dir_z, iso_o + dir_x + dir_z, iso_o + dir_y + dir_z

        right_face = Polygon(vA, vB, vE, vD, fill_color=RED_C,   fill_opacity=0.14, stroke_color=RED_C,   stroke_width=1.6)
        left_face  = Polygon(vA, vC, vF, vD, fill_color=GREEN_C, fill_opacity=0.14, stroke_color=GREEN_C, stroke_width=1.6)
        top_face   = Polygon(vD, vE, vA, vF, fill_color=BLUE_C,  fill_opacity=0.14, stroke_color=BLUE_C,  stroke_width=1.6)
        cube_ax_x  = Arrow(vA, vB, color=RED_C,   buff=0, stroke_width=3.0, tip_length=0.17, max_tip_length_to_length_ratio=0.35)
        cube_ax_y  = Arrow(vA, vC, color=GREEN_C, buff=0, stroke_width=3.0, tip_length=0.17, max_tip_length_to_length_ratio=0.35)
        cube_ax_z  = Arrow(vA, vD, color=BLUE_C,  buff=0, stroke_width=3.0, tip_length=0.17, max_tip_length_to_length_ratio=0.35)
        p1_visual  = VGroup(right_face, left_face, top_face, cube_ax_x, cube_ax_y, cube_ax_z)

        # ── Panel 2 visual: dimension counter ─────────────────────────────────
        Rn2  = MathTex(r"\mathbb{R}^2",    font_size=58).move_to(c2)
        Rn3  = MathTex(r"\mathbb{R}^3",    font_size=58).move_to(c2)
        Rn10 = MathTex(r"\mathbb{R}^{10}", font_size=58).move_to(c2)
        Rnn  = MathTex(r"\mathbb{R}^n",    font_size=58, color=accent).move_to(c2)

        # ── Panel 3 visual: scatter + manifold curve ──────────────────────────
        rng   = np.random.default_rng(42)
        x_ext = 1.52

        def on_pos():
            x = rng.uniform(-x_ext, x_ext)
            return c3 + np.array([x, 0.55 * np.sin(2.1 * x) + rng.normal(0, 0.07), 0])

        curve_p3 = ParametricFunction(
            lambda t: c3 + np.array([t, 0.55 * np.sin(2.1 * t), 0]),
            t_range=[-x_ext, x_ext], color=accent, stroke_width=2.2,
        )
        on_dots  = VGroup(*[Dot(on_pos(), radius=0.062, color=accent)  for _ in range(42)])
        off_dots = VGroup(*[
            Dot(c3 + np.array([rng.uniform(-x_ext, x_ext), rng.uniform(-1.35, 1.35), 0]),
                radius=0.052, color=GRAY_C)
            for _ in range(16)
        ])

        # ── Reveal Panel 1 ────────────────────────────────────────────────────
        self.play(DrawBorderThenFill(box1), run_time=0.65)
        self.play(
            LaggedStart(
                FadeIn(right_face), FadeIn(left_face), FadeIn(top_face),
                GrowArrow(cube_ax_x), GrowArrow(cube_ax_y), GrowArrow(cube_ax_z),
                lag_ratio=0.18,
            ),
            run_time=1.3,
        )
        self.play(FadeIn(lbl1, sub1, shift=UP * 0.06), run_time=0.45)
        self.wait(0.25)

        # ── Reveal Panel 2 ────────────────────────────────────────────────────
        self.play(DrawBorderThenFill(box2), run_time=0.65)
        self.play(FadeIn(Rn2, scale=0.8), run_time=0.35)
        self.play(FadeOut(Rn2, scale=1.15), FadeIn(Rn3,  scale=0.8), run_time=0.35)
        self.play(FadeOut(Rn3,  scale=1.15), FadeIn(Rn10, scale=0.8), run_time=0.35)
        self.play(FadeOut(Rn10, scale=1.15), FadeIn(Rnn,  scale=0.8), run_time=0.40)
        self.play(FadeIn(lbl2, sub2, shift=UP * 0.06), run_time=0.45)
        self.wait(0.25)

        # ── Reveal Panel 3 ────────────────────────────────────────────────────
        self.play(DrawBorderThenFill(box3), run_time=0.65)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.4) for d in off_dots], lag_ratio=0.045),
            run_time=0.85,
        )
        self.play(Create(curve_p3), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.4) for d in on_dots], lag_ratio=0.016),
            run_time=0.85,
        )
        self.play(FadeIn(lbl3, sub3, shift=UP * 0.06), run_time=0.45)

        self.wait(3.5)

        all_panels = VGroup(
            panel_row, p1_visual, lbl1, sub1,
            Rnn, lbl2, sub2,
            off_dots, on_dots, curve_p3, lbl3, sub3,
        )
        self.play(FadeOut(all_panels), run_time=0.8)

        # ═══ PHASE 2: THESIS — written stroke by stroke ═══════════════════════

        thesis = Text(
            "Dimensions turn information into geometry.",
            font_size=46, weight=BOLD, color=accent,
        ).move_to(ORIGIN)

        self.play(Write(thesis), run_time=2.8)
        self.wait(4.5)
