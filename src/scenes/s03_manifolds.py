from manim import *
import numpy as np


class IntrinsicDimension(ThreeDScene):
    def construct(self):
        surface_color = BLUE_E
        grid_color = BLUE_B
        highlight_color = YELLOW
        sphere_radius = 2.0
        lat_u = PI / 6   # 30° latitude
        lon_v = PI / 4   # 45° longitude

        def sp(lat, lon):
            return np.array([
                sphere_radius * np.cos(lat) * np.cos(lon),
                sphere_radius * np.cos(lat) * np.sin(lon),
                sphere_radius * np.sin(lat),
            ])

        point_coords = sp(lat_u, lon_v)

        # ── SPHERE ────────────────────────────────────────────────────────
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        sphere = Surface(
            lambda u, v: sp(u, v),
            u_range=[-PI / 2, PI / 2],
            v_range=[0, 2 * PI],
            resolution=(24, 48),
            fill_opacity=0.6,
            fill_color=surface_color,
            stroke_color=grid_color,
            stroke_width=0.5,
        )

        meridian = ParametricFunction(
            lambda u: sp(u, lon_v),
            t_range=[-PI / 2, PI / 2],
            color=highlight_color,
            stroke_width=4,
        )
        parallel = ParametricFunction(
            lambda v: sp(lat_u, v),
            t_range=[0, 2 * PI],
            color=highlight_color,
            stroke_width=4,
        )
        marker = Dot3D(point=point_coords, radius=0.05, color=highlight_color)

        self.play(FadeIn(sphere), run_time=1.0)
        self.play(Create(meridian), Create(parallel), FadeIn(marker), run_time=1.5)
        self.wait(0.8)

        # ── TEXT: EMBEDDING VS INTRINSIC ──────────────────────────────────
        # Set opacity 0 before adding as fixed frame — FadeIn on fixed-frame
        # mobjects is unreliable; animating opacity is the safe pattern.
        embed_text = Text(
            "Embedding dimension: where it lives  (3D)", color=WHITE,
        ).scale(0.55)
        intrinsic_text = Text(
            "Intrinsic dimension: coordinates needed  (2D)", color=highlight_color,
        ).scale(0.55)
        text_group = VGroup(embed_text, intrinsic_text).arrange(DOWN, aligned_edge=LEFT)
        text_group.to_corner(UL)
        embed_text.set_opacity(0)
        intrinsic_text.set_opacity(0)
        self.add_fixed_in_frame_mobjects(text_group)

        self.play(embed_text.animate.set_opacity(1), run_time=0.6)
        self.wait(0.8)
        self.play(intrinsic_text.animate.set_opacity(1), run_time=0.6)
        self.wait(1.5)
        self.play(text_group.animate.set_opacity(0), run_time=0.5)

        # ── ZOOM IN: LOCALLY FLAT ──────────────────────────────────────────
        # Camera moves along the outward normal at point_coords so we look
        # straight down onto the surface patch — no object scaling, so the
        # marker stays a point and nothing looks distorted.
        outward_phi = PI / 2 - lat_u   # 60° — matches outward normal polar angle
        outward_theta = lon_v           # 45° — matches outward normal azimuth

        self.move_camera(
            phi=outward_phi,
            theta=outward_theta,
            frame_center=point_coords,
            zoom=14,
            run_time=3.0, rate_func=smooth,
        )
        self.wait(0.3)

        # Local tangent basis (unit vectors in the sphere surface at this point)
        e_lon = np.array([-np.sin(lon_v), np.cos(lon_v), 0.0])
        e_lat = np.array([
            -np.sin(lat_u) * np.cos(lon_v),
            -np.sin(lat_u) * np.sin(lon_v),
            np.cos(lat_u),
        ])
        ax_len = 0.18

        lon_axis = Arrow3D(start=point_coords, end=point_coords + e_lon * ax_len, color=RED_C)
        lat_axis = Arrow3D(start=point_coords, end=point_coords + e_lat * ax_len, color=GREEN_C)

        # "locally flat" label in screen space
        flat_label = Text("locally flat", font_size=28, color=WHITE).to_edge(DOWN, buff=0.5)
        flat_label.set_opacity(0)
        self.add_fixed_in_frame_mobjects(flat_label)

        self.play(
            FadeIn(lon_axis), FadeIn(lat_axis),
            flat_label.animate.set_opacity(1),
            run_time=0.8,
        )
        self.wait(0.4)

        # Point moves freely on the surface — at this scale the curvature is
        # invisible, so the movement looks exactly like a flat 2D plane.
        self.play(marker.animate.move_to(sp(lat_u + 0.10, lon_v)),          run_time=0.7, rate_func=smooth)
        self.play(marker.animate.move_to(sp(lat_u + 0.10, lon_v + 0.12)),   run_time=0.8, rate_func=smooth)
        self.play(marker.animate.move_to(sp(lat_u,        lon_v + 0.12)),   run_time=0.7, rate_func=smooth)
        self.play(marker.animate.move_to(sp(lat_u - 0.08, lon_v + 0.05)),   run_time=0.7, rate_func=smooth)
        self.play(marker.animate.move_to(sp(lat_u,        lon_v)),          run_time=0.8, rate_func=smooth)
        self.wait(0.6)

        # ── PULL BACK ─────────────────────────────────────────────────────
        self.play(FadeOut(lon_axis, lat_axis), flat_label.animate.set_opacity(0), run_time=0.5)
        self.move_camera(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            frame_center=ORIGIN,
            zoom=1,
            run_time=2.5, rate_func=smooth,
        )
        self.wait(1.5)
