from manim import *
import numpy as np


class IntrinsicDimension(ThreeDScene):
    def construct(self):
        surface_color = BLUE_E
        grid_color = BLUE_B
        highlight_color = YELLOW

        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        # ── PART 1: CURVED SURFACE ─────────────────────────────────────────
        bend_amount = ValueTracker(0.0)

        curved_surface = always_redraw(
            lambda: Surface(
                lambda u, v: np.array([u, v, bend_amount.get_value() * np.sin(u)]),
                u_range=[-3, 3],
                v_range=[-3, 3],
                resolution=(24, 24),
                fill_opacity=0.6,
                fill_color=surface_color,
                stroke_color=grid_color,
                stroke_width=1,
            )
        )

        self.play(Create(curved_surface), run_time=2)
        self.wait(0.5)
        self.play(bend_amount.animate.set_value(1.0), run_time=2, rate_func=smooth)
        self.wait(1)

        # ── PART 2: TANGENT PLANE (LOCAL FLATNESS) ─────────────────────────
        # At x=0: surface z=sin(0)=0, slope cos(0)=1 → tangent plane is z=x.
        dot = Sphere(radius=0.08, color=highlight_color).move_to(ORIGIN)

        tangent_plane = Surface(
            lambda u, v: np.array([u, v, u]),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            fill_opacity=0.75,
            fill_color=highlight_color,
            stroke_width=0,
        )

        self.play(FadeIn(dot), run_time=0.5)
        self.play(Create(tangent_plane), run_time=1.0)
        self.wait(0.5)

        # Camera zoom — objects keep their real sizes so the dot stays a dot.
        # At high zoom the surface and tangent plane are indistinguishable: locally flat.
        self.move_camera(zoom=6, frame_center=ORIGIN, run_time=2.0, rate_func=smooth)
        self.wait(1.5)
        self.move_camera(zoom=1, frame_center=ORIGIN, run_time=1.8, rate_func=smooth)
        self.wait(0.5)

        # Clear always_redraw updater before fading to avoid a redraw/fade conflict.
        curved_surface.clear_updaters()
        self.play(FadeOut(curved_surface, dot, tangent_plane), run_time=1.0)

        # ── PART 3: THE SPHERE (INTRINSIC VS EMBEDDING) ────────────────────
        sphere_radius = 2.0
        sphere = Surface(
            lambda u, v: np.array([
                sphere_radius * np.cos(u) * np.cos(v),
                sphere_radius * np.cos(u) * np.sin(v),
                sphere_radius * np.sin(u),
            ]),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, 2 * PI],
            resolution=(24, 48),
            fill_opacity=0.6,
            fill_color=surface_color,
            stroke_color=grid_color,
            stroke_width=0.5,
        )

        self.play(FadeIn(sphere), run_time=1.0)

        lat_u = PI / 6   # 30° latitude
        lon_v = PI / 4   # 45° longitude

        point_coords = np.array([
            sphere_radius * np.cos(lat_u) * np.cos(lon_v),
            sphere_radius * np.cos(lat_u) * np.sin(lon_v),
            sphere_radius * np.sin(lat_u),
        ])

        dot_sphere = Sphere(radius=0.08, color=highlight_color).move_to(point_coords)

        meridian = ParametricFunction(
            lambda u: np.array([
                sphere_radius * np.cos(u) * np.cos(lon_v),
                sphere_radius * np.cos(u) * np.sin(lon_v),
                sphere_radius * np.sin(u),
            ]),
            t_range=[-PI / 2, PI / 2],
            color=highlight_color,
            stroke_width=4,
        )

        parallel = ParametricFunction(
            lambda v: np.array([
                sphere_radius * np.cos(lat_u) * np.cos(v),
                sphere_radius * np.cos(lat_u) * np.sin(v),
                sphere_radius * np.sin(lat_u),
            ]),
            t_range=[0, 2 * PI],
            color=highlight_color,
            stroke_width=4,
        )

        self.play(Create(meridian), Create(parallel), FadeIn(dot_sphere), run_time=1.5)
        self.wait(1)

        # ── PART 4: EMBEDDING VS INTRINSIC DIMENSION ───────────────────────
        embed_text = Text(
            "Embedding dimension: where it lives  (3D)", color=WHITE,
        ).scale(0.55)
        intrinsic_text = Text(
            "Intrinsic dimension: coordinates needed  (2D)", color=highlight_color,
        ).scale(0.55)

        text_group = VGroup(embed_text, intrinsic_text).arrange(DOWN, aligned_edge=LEFT)
        text_group.to_corner(UL)
        self.add_fixed_in_frame_mobjects(text_group)

        self.play(FadeIn(embed_text, shift=DOWN * 0.2))
        self.wait(1)
        self.play(FadeIn(intrinsic_text, shift=DOWN * 0.2))
        self.wait(1.5)
        self.play(text_group.animate.set_opacity(0), run_time=0.5)

        # ── PART 5: ZOOM INTO SPHERE — GLOBALLY CURVED, LOCALLY FLAT ───────
        # Camera moves to face the surface point from outside (along its outward normal).
        # phi and theta match the outward normal direction at (lat_u, lon_v):
        #   phi = PI/2 - lat_u  (polar angle from z-axis)
        #   theta = lon_v       (azimuth matching the longitude)
        # At zoom=14 the grid lines look straight — the surface is locally flat.
        outward_phi = PI / 2 - lat_u   # 60°
        outward_theta = lon_v          # 45°

        self.move_camera(
            phi=outward_phi,
            theta=outward_theta,
            frame_center=point_coords,
            zoom=14,
            run_time=3.0, rate_func=smooth,
        )
        self.wait(2)

        # Pull back to reveal the global curvature
        self.move_camera(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            frame_center=ORIGIN,
            zoom=1,
            run_time=2.5, rate_func=smooth,
        )
        self.wait(1.5)
