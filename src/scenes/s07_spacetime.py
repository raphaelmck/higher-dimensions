from manim import *
import numpy as np

class SpacetimeGeometry(ThreeDScene):
    def construct(self):
        # -- STYLING & SETUP --
        space_color = BLUE_D
        time_color = RED_C
        mass_color = YELLOW_C
        
        # Angle the camera for a sweeping 3D perspective
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        # --- BEAT 1: EUCLIDEAN SPACE ---
        # Build a dense grid so apply_function bends it smoothly later
        dense_grid = VGroup()
        for x in np.arange(-8, 9, 0.5): # 0.5 spacing creates a high-res mesh
            line = ParametricFunction(
                lambda t: np.array([x, t, 0]), 
                t_range=[-8, 8], 
                color=space_color, 
                stroke_opacity=0.5,
                stroke_width=1.5
            )
            dense_grid.add(line)
            
        for y in np.arange(-8, 9, 0.5):
            line = ParametricFunction(
                lambda t: np.array([t, y, 0]), 
                t_range=[-8, 8], 
                color=space_color, 
                stroke_opacity=0.5,
                stroke_width=1.5
            )
            dense_grid.add(line)
            
        self.play(Create(dense_grid, lag_ratio=0.01), run_time=2)
        
        # Euclidean Formula
        # Breaking the string into parts allows for smooth transforming later
        eq_euclid = MathTex("ds^2", "=", "dx^2 + dy^2 + dz^2")
        eq_euclid.to_corner(UL)
        self.add_fixed_in_frame_mobjects(eq_euclid)
        
        self.play(Write(eq_euclid))
        self.wait(1.5)
        
        # --- BEAT 2: RELATIVITY & THE MINKOWSKI METRIC ---
        # "In relativity, spacetime has a different metric..."
        eq_minkowski = MathTex("ds^2", "=", "-c^2dt^2", "+", "dx^2 + dy^2 + dz^2")
        eq_minkowski[2].set_color(time_color) # Highlight the new time component
        eq_minkowski.to_corner(UL)
        
        # TransformMatchingTex automatically maps identical substrings (ds^2, =) 
        # and gently fades in the new components.
        self.play(
            TransformMatchingTex(eq_euclid, eq_minkowski),
            run_time=1.5
        )
        self.wait(1)
        
        # --- BEAT 3: CURVED SPACETIME (THE GEOMETRY) ---
        # Introduce a "mass" to warp the geometry
        mass = Sphere(radius=0.4, color=mass_color)
        mass.move_to(ORIGIN)
        self.play(FadeIn(mass, shift=DOWN*0.5))
        
        # Animate the grid bending. 
        # A Gaussian curve creates a mathematically accurate gravitational well.
        depth = 2.5
        spread = 0.4
        
        def gravity_well(p):
            r_sq = p[0]**2 + p[1]**2
            z = -depth * np.exp(-spread * r_sq)
            return np.array([p[0], p[1], z])
            
        self.play(
            dense_grid.animate.apply_function(gravity_well),
            mass.animate.move_to(np.array([0, 0, -depth])),
            run_time=3.5,
            rate_func=smooth
        )
        
        # Slowly rotate the camera to let the viewer appreciate the curvature
        self.move_camera(theta=-75 * DEGREES, phi=70 * DEGREES, run_time=4, rate_func=there_and_back)
        self.wait(1)
        
        # --- BEAT 4: FINAL THESIS ---
        self.play(
            FadeOut(dense_grid, mass, eq_minkowski),
            run_time=1.5
        )
        
        # Reset camera to a flat 2D perspective for typography
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=1)
        
        # Use Tex to bold the words, and color "metric" to link back to the time component
        thesis = Tex(r"\textbf{Coordinates} + \textbf{metric} = \textbf{geometry.}")
        thesis.scale(1.2)
        thesis[0][12:18].set_color(time_color) 
        
        self.add_fixed_in_frame_mobjects(thesis)
        self.play(Write(thesis), run_time=2)
        self.wait(3)
