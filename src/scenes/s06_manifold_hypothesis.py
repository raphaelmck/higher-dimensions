from manim import *
import numpy as np


class ManifoldHypothesis(ThreeDScene):
    def construct(self):
        accent = TEAL_C
        surface_color = BLUE_E
        grid_color = BLUE_B

        def swiss_roll(u, v):
            t = 1.5 * PI + 3.0 * PI * u
            scale = 0.13
            return np.array([t * np.cos(t) * scale, 2.0 * v - 1.0, t * np.sin(t) * scale])

        # ── Beat 1: Noise wall ─────────────────────────────────────────────
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        def noise_grid(seed):
            rng = np.random.default_rng(seed)
            rs, gs, bs = rng.integers(10, 70, 16), rng.integers(10, 70, 16), rng.integers(10, 70, 16)
            squares = [
                Square(0.27, fill_opacity=1, stroke_width=0.4, stroke_color=BLACK,
                       fill_color=f"#{r:02x}{g:02x}{b:02x}")
                for r, g, b in zip(rs, gs, bs)
            ]
            return VGroup(*squares).arrange_in_grid(4, 4, buff=0)

        noises = VGroup(*[noise_grid(i * 17 + 3) for i in range(15)])
        noises.arrange_in_grid(3, 5, buff=0.35)

        noise_label = Text(
            "random point in pixel space  →  almost always noise",
            font_size=28, color=GRAY_B,
        ).to_edge(DOWN, buff=0.5)

        self.play(
            LaggedStart(*[FadeIn(g, scale=0.9) for g in noises], lag_ratio=0.05),
            run_time=1.4,
        )
        self.play(FadeIn(noise_label), run_time=0.4)
        self.wait(1.0)
        self.play(FadeOut(noises, noise_label, shift=DOWN * 0.1), run_time=0.5)

        # ── Beat 2: Data cloud appears as camera swings to 3D ─────────────
        # Most points near the swiss roll surface (not drawn yet), a handful
        # scattered off it — the cloud has structure but you can't see why yet.
        rng2 = np.random.default_rng(42)

        pts_on = [
            swiss_roll(rng2.uniform(0.05, 0.95), rng2.uniform(0.05, 0.95))
            + rng2.normal(0, 0.03, 3)
            for _ in range(130)
        ]
        pts_off = [
            swiss_roll(rng2.uniform(0.05, 0.95), rng2.uniform(0.05, 0.95))
            + rng2.normal(0, 0.32, 3)
            for _ in range(45)
        ]

        def glowing_dot(pos):
            halo = Sphere(radius=0.10, color=accent)
            halo.move_to(pos)
            halo.set_opacity(0.12)
            core = Dot3D(point=pos, radius=0.04, color=accent)
            return VGroup(halo, core)

        on_roll_pts  = VGroup(*[glowing_dot(p) for p in pts_on])
        off_roll_pts = VGroup(*[Dot3D(point=p, radius=0.035, color=GRAY_C) for p in pts_off])
        data_pts = VGroup(off_roll_pts, on_roll_pts)

        all_dot_list = [*off_roll_pts, *on_roll_pts]

        # Camera and data cloud arrive together — no blank frames
        self.move_camera(
            phi=65 * DEGREES, theta=-50 * DEGREES,
            run_time=2.0,
            added_anims=[LaggedStart(*[FadeIn(d) for d in all_dot_list], lag_ratio=0.012)],
        )
        self.wait(0.5)

        # ── Beat 3: Cube — ambient R^n space ──────────────────────────────
        def box_edges(s, color=GRAY_B, opacity=0.7):
            corners = np.array([
                [-s, -s, -s], [-s, -s,  s], [-s,  s, -s], [-s,  s,  s],
                [ s, -s, -s], [ s, -s,  s], [ s,  s, -s], [ s,  s,  s],
            ])
            lines = VGroup()
            for i in range(8):
                for j in range(i + 1, 8):
                    if np.sum(np.abs(corners[i] - corners[j]) > 0.01) == 1:
                        lines.add(Line(corners[i], corners[j],
                                       color=color, stroke_opacity=opacity, stroke_width=2.0))
            return lines

        rn_label = MathTex(r"\mathbb{R}^n", font_size=36, color=GRAY_B).to_corner(UR, buff=0.55)
        rn_label.set_opacity(0)
        self.add_fixed_in_frame_mobjects(rn_label)

        cube = box_edges(2.2)
        self.play(Create(cube), rn_label.animate.set_opacity(1), run_time=1.0)
        self.wait(0.8)

        # Cube fades, data cloud stays
        self.play(FadeOut(cube), rn_label.animate.set_opacity(0), run_time=0.8)
        self.wait(0.3)

        # ── Beat 4: Swiss roll draws itself through the existing data ──────
        roll = Surface(
            swiss_roll,
            u_range=[0, 1], v_range=[0, 1],
            resolution=(32, 12),
            fill_opacity=0.65,
            fill_color=surface_color,
            stroke_color=grid_color,
            stroke_width=0.8,
        )
        self.play(Create(roll), run_time=1.8)
        self.wait(0.4)

        # ── Beat 5: Label + spin ────────────────────────────────────────────
        manifold_lbl = Text(
            "real data occupies a thin, structured region",
            font_size=28, color=accent,
        ).to_edge(DOWN, buff=0.6)
        manifold_lbl.set_opacity(0)
        self.add_fixed_in_frame_mobjects(manifold_lbl)
        self.play(manifold_lbl.animate.set_opacity(1), run_time=0.6)

        self.begin_ambient_camera_rotation(rate=-0.18)
        self.wait(3.5)
        self.stop_ambient_camera_rotation()

        self.play(manifold_lbl.animate.set_opacity(0), run_time=0.4)

        # ── Beat 6: Dot travels along the manifold ─────────────────────────
        self.play(FadeOut(data_pts), run_time=0.5)

        spiral_path = ParametricFunction(
            lambda t: swiss_roll(0.05 + t * 0.9, 0.08 + t * 0.84),
            t_range=[0, 1],
            color=YELLOW_C,
            stroke_width=3,
        )
        trail_dot = Dot3D(point=swiss_roll(0.05, 0.08), radius=0.07, color=YELLOW)
        self.add(trail_dot)

        self.play(
            Create(spiral_path),
            MoveAlongPath(trail_dot, spiral_path),
            run_time=3.0, rate_func=linear,
        )
        self.wait(0.5)
        self.play(FadeOut(spiral_path, trail_dot), run_time=0.4)

        # ── Beat 7: Unroll — curved outside, simple inside ─────────────────
        def flat_roll(u, v):
            return np.array([u * 4.0 - 2.0, 2.0 * v - 1.0, 0.0])

        beta = ValueTracker(0.0)
        unrolled = always_redraw(lambda: Surface(
            lambda u, v: (1 - beta.get_value()) * swiss_roll(u, v)
                         + beta.get_value() * flat_roll(u, v),
            u_range=[0, 1], v_range=[0, 1],
            resolution=(32, 12),
            fill_opacity=0.65,
            fill_color=surface_color,
            stroke_color=grid_color,
            stroke_width=0.8,
        ))

        self.remove(roll)
        self.add(unrolled)

        self.play(beta.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)

        # ── Final line ─────────────────────────────────────────────────────
        final_text = Text(
            "High-dimensional data can have low-dimensional structure.",
            font_size=31, weight=BOLD, color=WHITE,
        ).to_edge(UP, buff=0.6)
        final_text.set_opacity(0)
        self.add_fixed_in_frame_mobjects(final_text)
        self.play(final_text.animate.set_opacity(1), run_time=0.8)
        self.wait(2.5)
