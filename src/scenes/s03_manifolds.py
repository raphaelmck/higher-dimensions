from manim import *
import numpy as np

class IntrinsicDimension(ThreeDScene):
    def construct(self):
        # -- STYLING & SETUP --
        surface_color = BLUE_E
        grid_color = BLUE_B
        highlight_color = YELLOW

        # Set the optimal viewing angle
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        # --- PART 1: THE CURVED SURFACE ---
        # We use a ValueTracker to smoothly animate the "bend"
        bend_amount = ValueTracker(0.0)

        # always_redraw ensures the 3D normals and geometry recalculate every frame
        curved_surface = always_redraw(
            lambda: Surface(
                # Parametric equation: z = bend * sin(x)
                lambda u, v: np.array([u, v, bend_amount.get_value() * np.sin(u)]),
                u_range=[-3, 3],
                v_range=[-3, 3],
                resolution=(24, 24),
                fill_opacity=0.6,
                fill_color=surface_color,
                stroke_color=grid_color,
                stroke_width=1
            )
        )

        self.play(Create(curved_surface), run_time=2)
        self.wait(0.5)

        # Bend the flat grid into a curved manifold
        self.play(bend_amount.animate.set_value(1.0), run_time=2, rate_func=smooth)
        self.wait(1)

        # --- PART 2: TANGENT PLANE (LOCAL FLATNESS) ---
        # The surface is z = sin(x). At x=0, the slope is cos(0) = 1.
        # Therefore, the tangent plane at the origin is exactly z = x.
        dot = Sphere(radius=0.08, color=highlight_color).move_to(ORIGIN)
        
        tangent_plane = Surface(
            lambda u, v: np.array([u, v, u]), # The mathematically exact tangent plane
            u_range=[-0.8, 0.8],
            v_range=[-0.8, 0.8],
            fill_opacity=0.8,
            fill_color=highlight_color,
            stroke_width=0
        )

        self.play(FadeIn(dot))
        self.play(Create(tangent_plane))
        self.wait(1)

        # CRITICAL MANIM FIX: Clear the updater before scaling, 
        # otherwise the scaling animation will glitch against the redraw loop.
        curved_surface.clear_updaters()

        # Small zoom to emphasize the "looks flat" narration
        surface_group = VGroup(curved_surface, dot, tangent_plane)
        self.play(
            surface_group.animate.scale(3.5, about_point=ORIGIN),
            run_time=3,
            rate_func=there_and_back # Zooms in closely, then seamlessly returns
        )
        self.wait(1)

        # Clear the stage
        self.play(FadeOut(surface_group))


        # --- PART 3: THE SPHERE (INTRINSIC VS EMBEDDING) ---
        sphere_radius = 2.0
        sphere = Surface(
            lambda u, v: np.array([
                sphere_radius * np.cos(u) * np.cos(v),
                sphere_radius * np.cos(u) * np.sin(v),
                sphere_radius * np.sin(u)
            ]),
            u_range=[-PI/2, PI/2],
            v_range=[0, 2*PI],
            resolution=(24, 48), # Higher horizontal resolution for smooth equator
            fill_opacity=0.6,
            fill_color=surface_color,
            stroke_color=grid_color,
            stroke_width=0.5
        )

        self.play(FadeIn(sphere))
        
        # Define a specific coordinate: Latitude (u) and Longitude (v)
        lat_u = PI / 6
        lon_v = PI / 4

        # Convert spherical to Cartesian for the dot placement
        point_coords = np.array([
            sphere_radius * np.cos(lat_u) * np.cos(lon_v),
            sphere_radius * np.cos(lat_u) * np.sin(lon_v),
            sphere_radius * np.sin(lat_u)
        ])

        dot_sphere = Sphere(radius=0.08, color=highlight_color).move_to(point_coords)

        # Parametric curves to draw the exact meridian and parallel
        meridian = ParametricFunction(
            lambda u: np.array([
                sphere_radius * np.cos(u) * np.cos(lon_v),
                sphere_radius * np.cos(u) * np.sin(lon_v),
                sphere_radius * np.sin(u)
            ]),
            t_range=[-PI/2, PI/2],
            color=highlight_color,
            stroke_width=4
        )

        parallel = ParametricFunction(
            lambda v: np.array([
                sphere_radius * np.cos(lat_u) * np.cos(v),
                sphere_radius * np.cos(lat_u) * np.sin(v),
                sphere_radius * np.sin(lat_u)
            ]),
            t_range=[0, 2*PI],
            color=highlight_color,
            stroke_width=4
        )

        self.play(Create(meridian), Create(parallel), FadeIn(dot_sphere), run_time=1.5)
        
        # Math Label
        math_label = MathTex(r"(\theta, \phi)").scale(1.2).move_to(point_coords + OUT*0.5 + RIGHT*0.5)
        math_label.rotate(PI/2, axis=RIGHT) # Stand it vertically
        math_label.rotate(PI/4, axis=OUT)   # Twist to face the camera angle
        self.play(Write(math_label))
        self.wait(1)


        # --- PART 4: ON-SCREEN TEXT ---
        # Using add_fixed_in_frame_mobjects ensures the text acts like a UI overlay
        embed_text = Text("Embedding dimension: where it lives (3D)", color=WHITE).scale(0.55)
        intrinsic_text = Text("Intrinsic dimension: how many coordinates it needs (2D)", color=highlight_color).scale(0.55)
        
        text_group = VGroup(embed_text, intrinsic_text).arrange(DOWN, aligned_edge=LEFT)
        text_group.to_corner(UL)
        self.add_fixed_in_frame_mobjects(text_group)

        self.play(FadeIn(embed_text, shift=DOWN*0.2))
        self.wait(1)
        self.play(FadeIn(intrinsic_text, shift=DOWN*0.2))
        self.wait(2)


        # --- PART 5: THE VISUAL BEAT (GLOBALLY CURVED, LOCALLY FLAT) ---
        self.play(FadeOut(math_label))
        
        sphere_group = VGroup(sphere, meridian, parallel, dot_sphere)
        
        # Scaling massively around the *exact coordinate* forces the camera's 
        # perspective directly into the surface, naturally flattening the grid lines.
        self.play(
            sphere_group.animate.scale(40, about_point=point_coords),
            run_time=4,
            rate_func=ease_in_out_sine
        )
        self.wait(2)
