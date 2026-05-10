from manim import *
import numpy as np


class SpacetimeGeometry(Scene):
    def construct(self):
        time_color = RED_C
        light_color = YELLOW_C
        accent = TEAL_C
        lim = 3.0  # diagram half-extent in data coordinates

        axes = Axes(
            x_range=[-lim, lim, 1], y_range=[-lim, lim, 1],
            x_length=6.2, y_length=6.2,
            axis_config={"include_ticks": False},
        )
        x_lbl  = axes.get_x_axis_label(MathTex("x"),  direction=RIGHT, buff=0.2)
        y_lbl  = axes.get_y_axis_label(MathTex("y"),  direction=UP,    buff=0.2)
        ct_lbl = axes.get_y_axis_label(MathTex("ct"), direction=UP,    buff=0.2)

        # ── Beat 1: A metric is a ruler ───────────────────────────────────────
        # Two points, the distance between them, and the circle of equal distance.
        pt_O = Dot(axes.c2p(0, 0), color=WHITE, radius=0.07)
        pt_A = Dot(axes.c2p(1.6, 1.2), color=accent, radius=0.07)
        dist_line = Line(pt_O.get_center(), pt_A.get_center(), color=GRAY_B, stroke_width=2)
        ds_lbl = MathTex("ds", font_size=28, color=GRAY_B).next_to(dist_line.get_center(), UL, buff=0.08)

        r_screen = np.linalg.norm(np.array(axes.c2p(1.6, 1.2)) - np.array(axes.c2p(0, 0)))
        eq_circle = Circle(radius=r_screen, color=accent, stroke_width=2, stroke_opacity=0.65).move_to(pt_O)

        eq_euclid = MathTex(r"ds^2 = dx^2 + dy^2", font_size=36).to_corner(UL, buff=0.55)

        self.play(Create(axes), FadeIn(x_lbl, y_lbl), run_time=0.8)
        self.play(FadeIn(pt_O), run_time=0.3)
        self.play(FadeIn(pt_A), Create(dist_line), FadeIn(ds_lbl), run_time=0.7)
        self.play(Write(eq_euclid), run_time=0.7)
        self.play(Create(eq_circle), run_time=1.0)
        self.wait(1.2)

        # ── Beat 2: Add time — the minus sign changes everything ──────────────
        # y → ct, equation gains a minus sign in red.
        eq_mink = MathTex(
            r"ds^2 = dx^2 ", r"-", r"\, c^2\, dt^2",
            font_size=36,
        ).to_corner(UL, buff=0.55)
        eq_mink[1].set_color(RED_C)
        eq_mink[2].set_color(time_color)

        self.play(
            FadeOut(eq_circle, pt_A, dist_line, ds_lbl),
            ReplacementTransform(y_lbl, ct_lbl),
            ReplacementTransform(eq_euclid, eq_mink),
            run_time=1.2,
        )
        self.wait(0.3)
        # Flash the minus sign so the viewer registers the key difference
        self.play(Indicate(eq_mink[1], color=RED_C, scale_factor=2.2), run_time=0.7)
        self.wait(0.8)

        # ── Beat 3: Light cone — the payoff ───────────────────────────────────
        # ds² = 0 on the cone. Regions inside and outside have opposite signs.
        light_r = Line(axes.c2p(-lim, -lim), axes.c2p(lim,  lim), color=light_color, stroke_width=2.5)
        light_l = Line(axes.c2p( lim, -lim), axes.c2p(-lim, lim), color=light_color, stroke_width=2.5)

        future  = Polygon(axes.c2p(0,0), axes.c2p( lim, lim), axes.c2p(-lim, lim),
                          fill_color=GREEN_C, fill_opacity=0.18, stroke_width=0)
        past    = Polygon(axes.c2p(0,0), axes.c2p( lim,-lim), axes.c2p(-lim,-lim),
                          fill_color=BLUE_C,  fill_opacity=0.18, stroke_width=0)
        space_r = Polygon(axes.c2p(0,0), axes.c2p( lim, lim), axes.c2p( lim,-lim),
                          fill_color=GRAY,    fill_opacity=0.18, stroke_width=0)
        space_l = Polygon(axes.c2p(0,0), axes.c2p(-lim, lim), axes.c2p(-lim,-lim),
                          fill_color=GRAY,    fill_opacity=0.18, stroke_width=0)

        ds0_lbl    = MathTex(r"ds^2 = 0",  font_size=28, color=light_color).next_to(axes.c2p(lim, lim), UR, buff=0.12)
        future_lbl = MathTex(r"ds^2 < 0",  font_size=26, color=GREEN_C).move_to(axes.c2p( 0,  2.0))
        past_lbl   = MathTex(r"ds^2 < 0",  font_size=26, color=BLUE_C).move_to(axes.c2p( 0, -2.0))
        sr_lbl     = MathTex(r"ds^2 > 0",  font_size=26, color=GRAY_B).move_to(axes.c2p( 2.0, 0))
        sl_lbl     = MathTex(r"ds^2 > 0",  font_size=26, color=GRAY_B).move_to(axes.c2p(-2.0, 0))

        self.play(Create(light_r), Create(light_l), run_time=1.0)
        self.play(FadeIn(ds0_lbl), run_time=0.4)
        self.play(FadeIn(future, past, space_r, space_l), run_time=0.8)
        self.play(FadeIn(future_lbl, past_lbl, sr_lbl, sl_lbl), run_time=0.6)
        self.wait(1.5)

        # ── Beat 4: Causal structure ──────────────────────────────────────────
        # One event inside the cone (timelike), one outside (spacelike).
        self.play(FadeOut(future_lbl, past_lbl, sr_lbl, sl_lbl, ds0_lbl), run_time=0.4)

        ev_t     = Dot(axes.c2p(0.4,  2.0), color=GREEN_C, radius=0.1)
        ev_t_lbl = Text("timelike",  font_size=22, color=GREEN_C).next_to(ev_t, RIGHT, buff=0.12)
        ev_s     = Dot(axes.c2p(2.4,  0.4), color=GRAY_B,  radius=0.1)
        ev_s_lbl = Text("spacelike", font_size=22, color=GRAY_B).next_to(ev_s,  RIGHT, buff=0.12)

        self.play(FadeIn(ev_t), FadeIn(ev_t_lbl), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(ev_s), FadeIn(ev_s_lbl), run_time=0.6)
        self.wait(1.5)

        # ── Beat 5: GR teaser — the metric itself varies ──────────────────────
        # Light cones tilt near a mass: same spacetime diagram, different geometry.
        self.play(
            FadeOut(future, past, space_r, space_l,
                    light_r, light_l,
                    ev_t, ev_t_lbl, ev_s, ev_s_lbl,
                    eq_mink, pt_O),
            run_time=0.8,
        )

        mass_dot  = Dot(axes.c2p(0, 0), color=YELLOW_C, radius=0.14)
        mass_ring = Circle(radius=0.22, color=YELLOW_C, stroke_width=2).move_to(axes.c2p(0, 0))

        def mini_cone(x_data, half_w=0.55, h=0.9):
            tilt  = -x_data * 0.28 * np.exp(-0.6 * x_data ** 2)
            apex  = np.array(axes.c2p(x_data, 0))
            left  = np.array(axes.c2p(x_data - half_w + tilt, h))
            right = np.array(axes.c2p(x_data + half_w + tilt, h))
            return VGroup(
                Line(apex, left,  color=YELLOW_C, stroke_width=1.8),
                Line(apex, right, color=YELLOW_C, stroke_width=1.8),
            )

        cones = VGroup(*[mini_cone(x) for x in [-2.5, -1.5, -0.5, 0, 0.5, 1.5, 2.5]])

        gr_formula = MathTex(r"g_{\mu\nu}(x)", font_size=36).to_corner(UL, buff=0.55)
        gr_lbl = Text(
            "metric varies from point to point", font_size=26, color=GRAY_B,
        ).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(mass_dot, mass_ring), Create(cones), run_time=1.2)
        self.play(Write(gr_formula), FadeIn(gr_lbl), run_time=0.8)
        self.wait(1.8)

        # ── Final: Coordinates + Metric = Geometry ────────────────────────────
        self.play(
            FadeOut(axes, x_lbl, ct_lbl, mass_dot, mass_ring, cones, gr_formula, gr_lbl),
            run_time=0.8,
        )

        top = VGroup(
            Text("Coordinates", font_size=36, weight=BOLD),
            MathTex("+", font_size=42),
            Text("Metric", font_size=36, weight=BOLD, color=time_color),
            MathTex("=", font_size=42),
            Text("Geometry", font_size=36, weight=BOLD, color=light_color),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 1.0)

        divider = Line(LEFT * 5, RIGHT * 5, color=GRAY_D, stroke_width=1).next_to(top, DOWN, buff=0.35)

        sub_coords = MathTex(r"(x,\, t)", font_size=30, color=GRAY_B)
        sub_metric = MathTex(r"ds^2 = dx^2 - c^2\, dt^2", font_size=26, color=time_color)
        sub_geom   = Text("light cone", font_size=28, color=light_color)

        # Align each subtitle under its top-row counterpart
        for sub, label in [(sub_coords, top[0]), (sub_metric, top[2]), (sub_geom, top[4])]:
            sub.move_to(np.array([label.get_center()[0], divider.get_center()[1] - 0.6, 0]))

        self.play(Write(top), run_time=1.5)
        self.play(Create(divider), run_time=0.4)
        self.play(
            LaggedStart(
                FadeIn(sub_coords, shift=UP * 0.1),
                FadeIn(sub_metric, shift=UP * 0.1),
                FadeIn(sub_geom,   shift=UP * 0.1),
                lag_ratio=0.3,
            ),
            run_time=1.2,
        )
        self.wait(2.5)
