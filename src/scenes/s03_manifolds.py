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

        # Tangent basis — used for the flat local grid and axes
        e_lon = np.array([-np.sin(lon_v), np.cos(lon_v), 0.0])
        e_lat = np.array([
            -np.sin(lat_u) * np.cos(lon_v),
            -np.sin(lat_u) * np.sin(lon_v),
            np.cos(lat_u),
        ])

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
        self.play(FadeIn(sphere), run_time=1.0)

        # ── PHASE 1: 3D AXES + WHITE TEXT ─────────────────────────────────
        # Show that the sphere lives in a 3D embedding space.
        space_axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
            x_length=6, y_length=6, z_length=6,
            axis_config={"include_ticks": False},
        )
        space_axes.get_x_axis().set_color(RED_C)
        space_axes.get_y_axis().set_color(GREEN_C)
        space_axes.get_z_axis().set_color(BLUE_C)

        embed_text = Text(
            "Embedding dimension: where it lives  (3D)", color=WHITE,
        ).scale(0.55)
        intrinsic_text = Text(
            "Intrinsic dimension: coordinates needed  (2D)", color=highlight_color,
        ).scale(0.55)
        # Position both now so layout is set; reveal independently
        VGroup(embed_text, intrinsic_text).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        embed_text.set_opacity(0)
        intrinsic_text.set_opacity(0)
        self.add_fixed_in_frame_mobjects(embed_text, intrinsic_text)

        self.play(
            Create(space_axes),
            embed_text.animate.set_opacity(1),
            run_time=1.2,
        )
        self.wait(1.0)

        # ── PHASE 2: HIDE AXES, REVEAL INTRINSIC COORDS ───────────────────
        # θ and φ start yellow — they belong to the intrinsic (2D) perspective.
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
        marker = Dot3D(point=point_coords, radius=0.013, color=highlight_color)

        coord_label = MathTex(r"(\theta,\, \phi)", font_size=40).to_corner(UR, buff=0.55)
        coord_label.set_color_by_tex(r"\theta", highlight_color)
        coord_label.set_color_by_tex(r"\phi", highlight_color)
        coord_label.set_opacity(0)
        self.add_fixed_in_frame_mobjects(coord_label)

        self.play(
            FadeOut(space_axes),
            Create(meridian), Create(parallel), FadeIn(marker),
            coord_label.animate.set_opacity(1),
            intrinsic_text.animate.set_opacity(1),
            run_time=1.2,
        )
        self.wait(1.5)

        # Fade all labels before zoom
        self.play(
            embed_text.animate.set_opacity(0),
            intrinsic_text.animate.set_opacity(0),
            coord_label.animate.set_opacity(0),
            run_time=0.5,
        )

        # ── FLAT LOCAL GRID ────────────────────────────────────────────────
        # Straight lines in the tangent plane — flat by construction.
        grid_extent = 0.10
        n_lines = 7
        local_grid = VGroup()
        for t in np.linspace(-grid_extent, grid_extent, n_lines):
            local_grid.add(Line(
                point_coords + t * e_lat - grid_extent * e_lon,
                point_coords + t * e_lat + grid_extent * e_lon,
                color=grid_color, stroke_width=0.8, stroke_opacity=0.7,
            ))
            local_grid.add(Line(
                point_coords + t * e_lon - grid_extent * e_lat,
                point_coords + t * e_lon + grid_extent * e_lat,
                color=grid_color, stroke_width=0.8, stroke_opacity=0.7,
            ))

        # ── ZOOM IN: LOCALLY FLAT ──────────────────────────────────────────
        outward_phi = PI / 2 - lat_u   # 60°
        outward_theta = lon_v           # 45°

        self.move_camera(
            phi=outward_phi,
            theta=outward_theta,
            frame_center=point_coords,
            zoom=14,
            run_time=3.0, rate_func=smooth,
        )

        self.play(
            FadeOut(meridian, parallel),
            FadeIn(local_grid),
            run_time=0.6,
        )
        self.wait(0.3)

        ax_len = 0.07
        lon_axis = Arrow3D(
            start=point_coords, end=point_coords + e_lon * ax_len,
            color=RED_C, thickness=0.003, height=0.015, base_radius=0.006,
        )
        lat_axis = Arrow3D(
            start=point_coords, end=point_coords + e_lat * ax_len,
            color=GREEN_C, thickness=0.003, height=0.015, base_radius=0.006,
        )

        flat_label = Text("locally flat", font_size=28, color=WHITE).to_edge(DOWN, buff=0.5)
        flat_label.set_opacity(0)
        self.add_fixed_in_frame_mobjects(flat_label)

        self.play(
            FadeIn(lon_axis), FadeIn(lat_axis),
            flat_label.animate.set_opacity(1),
            run_time=0.8,
        )
        self.wait(0.4)

        # Point moves freely — the flat grid makes it obvious this is a 2D plane
        self.play(marker.animate.move_to(sp(lat_u + 0.07, lon_v)),          run_time=0.7, rate_func=smooth)
        self.play(marker.animate.move_to(sp(lat_u + 0.07, lon_v + 0.09)),   run_time=0.8, rate_func=smooth)
        self.play(marker.animate.move_to(sp(lat_u,        lon_v + 0.09)),   run_time=0.7, rate_func=smooth)
        self.play(marker.animate.move_to(sp(lat_u - 0.06, lon_v + 0.04)),   run_time=0.7, rate_func=smooth)
        self.play(marker.animate.move_to(sp(lat_u,        lon_v)),          run_time=0.8, rate_func=smooth)
        self.wait(0.6)

        # ── PULL BACK ─────────────────────────────────────────────────────
        self.play(
            FadeOut(lon_axis, lat_axis, local_grid),
            flat_label.animate.set_opacity(0),
            run_time=0.5,
        )
        self.move_camera(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            frame_center=ORIGIN,
            zoom=1,
            run_time=2.5, rate_func=smooth,
        )
        self.wait(1.5)
